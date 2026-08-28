#!/usr/bin/env python3
"""Record how DJA's frozen v3 HTML shell locates and describes its row data.

This is intentionally a discovery receipt, not part of the scientific model.
Only tiny schema/header samples are retained; the large DJA catalog itself stays
upstream and, when needed, is fetched ephemerally by the acquisition step.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

PAGE = "https://s3.amazonaws.com/msaexp-nirspec/extractions/nirspec_graded_v3.html"
RANGE_BYTES = 16 * 1024


def probe(url: str) -> dict:
    try:
        response = requests.get(url, timeout=30, stream=True)
        receipt = {
            "url": url,
            "status": response.status_code,
            "content_type": response.headers.get("content-type"),
            "content_length": response.headers.get("content-length"),
        }
        response.close()
        return receipt
    except Exception as exc:
        return {"url": url, "error": f"{type(exc).__name__}: {exc}"}


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

    raw_refs: list[str] = []
    for ref in script_src + link_href + asset_strings + ajax_urls:
        absolute = urljoin(PAGE, ref)
        if absolute not in raw_refs:
            raw_refs.append(absolute)

    probes = [probe(url) for url in raw_refs]

    for suffix in ("csv", "ecsv", "json"):
        url = PAGE.rsplit(".", 1)[0] + "." + suffix
        if any(item.get("url") == url for item in probes):
            continue
        item = probe(url)
        item["diagnostic_sibling"] = True
        probes.append(item)

    marker = "nirspec_graded_v3.json"
    marker_index = text.find(marker)
    if marker_index >= 0:
        start = max(0, marker_index - 5000)
        end = min(len(text), marker_index + len(marker) + 5000)
        table_context = text[start:end]
    else:
        table_context = ""
    (out / "dja-v3-table-config.txt").write_text(table_context)

    json_urls = [
        urljoin(PAGE, ref)
        for ref in asset_strings
        if ref.lower().endswith(".json") and "nirspec_graded_v3" in ref
    ]
    range_receipt = None
    if json_urls:
        json_url = json_urls[0]
        try:
            ranged = requests.get(
                json_url,
                headers={"Range": f"bytes=0-{RANGE_BYTES - 1}"},
                timeout=60,
            )
            raw = ranged.content[:RANGE_BYTES]
            prefix = raw.decode("utf-8", errors="replace")
            (out / "dja-v3-json-prefix.txt").write_text(prefix)
            range_receipt = {
                "url": json_url,
                "status": ranged.status_code,
                "requested_range": f"bytes=0-{RANGE_BYTES - 1}",
                "content_range": ranged.headers.get("content-range"),
                "content_length": ranged.headers.get("content-length"),
                "content_type": ranged.headers.get("content-type"),
                "retained_bytes": len(raw),
                "retained_sha256": hashlib.sha256(raw).hexdigest(),
            }
        except Exception as exc:
            range_receipt = {"url": json_url, "error": f"{type(exc).__name__}: {exc}"}

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
        "table_config_marker_found": marker_index >= 0,
        "table_config_retained_chars": len(table_context),
        "json_prefix_range": range_receipt,
    }
    (out / "dja-v3-shell-assets.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
