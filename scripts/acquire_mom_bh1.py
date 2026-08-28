#!/usr/bin/env python3
"""Fetch only the public MoM-BH*-1 products needed for the first experiment.

Raw upstream data are never committed. This script records immutable-ish upstream
identifiers, returned metadata, byte sizes and SHA-256 hashes for every file it
retrieves so a workflow run can act as a reproducibility receipt.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.parse
import urllib.request

import yaml

USER_AGENT = "ApparentOrigin/0.1 (+https://github.com/PaulTiffany/ApparentOrigin)"


def get_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_product(dest: Path, data: bytes, source: dict) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {
        **source,
        "local_name": dest.name,
        "bytes": len(data),
        "sha256": sha256(data),
    }


def load_manifest(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def fetch_zenodo_prism(manifest: dict, outdir: Path) -> tuple[list[dict], dict]:
    api = manifest["upstream"]["zenodo_api"]
    metadata_raw = get_bytes(api)
    metadata = json.loads(metadata_raw)
    inventory = []
    for item in metadata.get("files", []):
        inventory.append(
            {
                "key": item.get("key"),
                "size": item.get("size"),
                "checksum": item.get("checksum"),
                "url": (item.get("links") or {}).get("self"),
            }
        )

    # Prefer small, analysis-ready spectral products; never bulk-download a deposit.
    candidates = []
    for item in metadata.get("files", []):
        key = (item.get("key") or "").lower()
        size = int(item.get("size") or 0)
        if size > 100 * 1024 * 1024:
            continue
        if any(token in key for token in ("spec", "prism", "1d")) and key.endswith(
            (".fits", ".fits.gz", ".csv", ".ecsv", ".txt", ".dat")
        ):
            candidates.append(item)

    if not candidates:
        # Do not guess or download large arbitrary blobs. The inventory is still a
        # useful CI artifact and tells us exactly what upstream exposes.
        return [], {"record": metadata.get("id"), "doi": metadata.get("doi"), "files": inventory}

    receipts = []
    for item in candidates:
        url = (item.get("links") or {}).get("self")
        if not url:
            continue
        data = get_bytes(url)
        receipts.append(
            save_product(
                outdir / "zenodo" / Path(item["key"]).name,
                data,
                {
                    "provider": "zenodo",
                    "record": metadata.get("id"),
                    "doi": metadata.get("doi"),
                    "upstream_key": item.get("key"),
                    "upstream_checksum": item.get("checksum"),
                    "url": url,
                },
            )
        )
    return receipts, {"record": metadata.get("id"), "doi": metadata.get("doi"), "files": inventory}


def fetch_dja_g395m(manifest: dict, outdir: Path) -> tuple[list[dict], list[dict]]:
    obj = manifest["object"]
    query = manifest["upstream"]["dja_query"]
    params = urllib.parse.urlencode(
        {
            "coords": f"{obj['ra_deg']},{obj['dec_deg']}",
            "size": "1.0",
            "output": "csv",
        }
    )
    query_url = f"{query}?{params}"
    raw = get_bytes(query_url)
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))

    g395m = [r for r in rows if "G395M" in (r.get("grating") or "").upper()]
    if not g395m:
        raise RuntimeError(
            f"DJA returned {len(rows)} extraction(s) near the target but no G395M product. "
            f"Query: {query_url}"
        )

    # Prefer EXCELS and the v3 reduction cited by Naidu et al.; fall back to the
    # nearest public G395M extraction if the archive now exposes only a later release.
    def rank(row: dict) -> tuple[int, int]:
        root = (row.get("root") or "").lower()
        file = (row.get("file") or "").lower()
        is_excels = int("excels" in root or "excels" in file or "3543" in file)
        is_v3 = int("-v3" in root or "-v3" in file)
        return (is_excels, is_v3)

    chosen = sorted(g395m, key=rank, reverse=True)[0]
    root, filename = chosen["root"], chosen["file"]
    file_url = manifest["upstream"]["dja_s3_template"].format(root=root, file=filename)
    data = get_bytes(file_url)
    receipt = save_product(
        outdir / "dja" / Path(filename).name,
        data,
        {
            "provider": "dja",
            "query_url": query_url,
            "url": file_url,
            "root": root,
            "file": filename,
            "grating": chosen.get("grating"),
            "version": chosen.get("version"),
            "ra": chosen.get("ra"),
            "dec": chosen.get("dec"),
            "srcid": chosen.get("srcid"),
            "exptime": chosen.get("exptime"),
        },
    )
    return [receipt], rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="provenance/mom-bh1.yaml")
    parser.add_argument("--out", default="data/raw")
    parser.add_argument("--receipt", default="results/acquisition_receipt.json")
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    outdir = Path(args.out)
    receipts = []

    zenodo_receipts, zenodo_inventory = fetch_zenodo_prism(manifest, outdir)
    receipts.extend(zenodo_receipts)
    dja_receipts, dja_rows = fetch_dja_g395m(manifest, outdir)
    receipts.extend(dja_receipts)

    result = {
        "object": manifest["object"],
        "paper": manifest["paper"],
        "products": receipts,
        "zenodo_inventory": zenodo_inventory,
        "dja_query_rows": dja_rows,
    }
    receipt = Path(args.receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"downloaded": len(receipts), "receipt": str(receipt)}, indent=2))


if __name__ == "__main__":
    main()
