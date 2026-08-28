#!/usr/bin/env python3
"""Record how DJA's frozen v3 HTML shell locates its row data.

This is intentionally a discovery receipt, not part of the scientific model.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

PAGE = "https://s3.amazonaws.com/msaexp-nirspec/extractions/nirspec_graded_v3.html"


def main() -> None:
    out = Path("run/provenance")
    out.mkdir(parents=True, exist_ok=True)
    response = requests.get(PAGE, timeout=60)
    response.raise_for_status()
    text = response.text

    script_src = re.findall(r'<script[^>]+src=["\']([^"\']+)', text, flags=re.I)
    link_href = re.findall(r'<link[^>]+href=["\']([^"\']+)', text, flags=re.I)
    asset_strings = re.findall(
        r'["\']([^"\']+\.(?:json|csv|ecsv|js)(?:\?[^"\']*)?)["\']',
        text,
        flags=re.I,
    )
    ajax_urls = re.findall(
        r'(?:ajax|url|data)\s*[:=]\s*["\']([^"\']+)["\']',
        text,
        flags=re.I,
    )

    raw_refs = []
    for ref in script_src + link_href + asset_strings + ajax_urls:
        absolute = urljoin(PAGE, ref)
        if absolute not in raw_refs:
            raw_refs.append(absolute)

    probes = []
    for url in raw_refs:
        try:
            r = requests.get(url, timeout=30, stream=True)
            probes.append(
                {
                    "url": url,
                    "status": r.status_code,
                    "content_type": r.headers.get("content-type"),
                    "content_length": r.headers.get("content-length"),
                }
            )
            r.close()
        except Exception as exc:
            probes.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})

    # Also test conservative sibling names suggested by DJA's documented
    # interactive-table + machine-readable-catalog convention. These are only
    # diagnostics and are never treated as provenance without HTTP 200.
    for suffix in ("csv", "ecsv", "json"):
        url = PAGE.rsplit(".", 1)[0] + "." + suffix
        if any(p.get("url") == url for p in probes):
            continue
        try:
            r = requests.get(url, timeout=30, stream=True)
            probes.append(
                {
                    "url": url,
                    "status": r.status_code,
                    "content_type": r.headers.get("content-type"),
                    "content_length": r.headers.get("content-length"),
                    "diagnostic_sibling": True,
                }
            )
            r.close()
        except Exception as exc:
            probes.append(
                {
                    "url": url,
                    "error": f"{type(exc).__name__}: {exc}",
                    "diagnostic_sibling": True,
                }
            )

    receipt = {
        "page": PAGE,
        "page_status": response.status_code,
        "page_bytes": len(response.content),
        "page_sha256": hashlib.sha256(response.content).hexdigest(),
        "script_src": script_src,
        "link_href": link_href,
        "asset_strings": asset_strings,
        "ajax_urls": ajax_urls,
        "resolved_assets": raw_refs,
        "asset_probes": probes,
    }
    (out / "dja-v3-shell-assets.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
