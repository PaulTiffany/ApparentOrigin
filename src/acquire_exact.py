#!/usr/bin/env python3
"""Acquire MoM-BH*-1 spectra without mirroring a catalog.

Identity chain:
1. select the pinned MoM/Zenodo source 150135;
2. read its explicit SRCRA/SRCDEC FITS metadata;
3. query DJA at that sky position;
4. require exactly one EXCELS GO-3543 G395M row within a tight radius;
5. probe the corresponding frozen-v3 path for the same EXCELS source ID;
6. use v3 only if its own FITS coordinates and H-beta coverage agree;
   otherwise use the exact current DJA reduction and label it as such.

Only the two small spectra are retained on the ephemeral runner. Every selected
product is hashed in the acquisition receipt.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import requests
import yaml

from acquire import (
    angular_sep_arcsec,
    choose_prism,
    download_limited,
    extract_coords,
    read_spec1d,
    sha256,
)


def parse_dja_csv(text: str) -> list[dict[str, str]]:
    if not text.strip() or text.lstrip().lower().startswith("nothing found"):
        return []
    return list(csv.DictReader(io.StringIO(text)))


def row_sep(row: dict[str, str], ra: float, dec: float) -> float:
    return angular_sep_arcsec(ra, dec, float(row["ra"]), float(row["dec"]))


def validate_spectrum(path: Path, ra: float, dec: float, redshift: float, radius_arcsec: float) -> dict[str, Any]:
    coords = extract_coords(path)
    if coords is None:
        raise RuntimeError(f"{path.name}: no explicit source coordinates in FITS")
    sep = angular_sep_arcsec(ra, dec, coords[0], coords[1])
    if sep > radius_arcsec:
        raise RuntimeError(
            f"{path.name}: FITS source position is {sep:.3f} arcsec from MoM-BH*-1, "
            f"above {radius_arcsec:.3f} arcsec"
        )

    wave, _, _, valid = read_spec1d(path)
    wave = np.asarray(wave, dtype=float)
    valid = np.asarray(valid, dtype=bool) & np.isfinite(wave)
    if valid.sum() < 20:
        raise RuntimeError(f"{path.name}: too few valid spectral samples")
    hbeta = 0.4861333 * (1.0 + redshift)
    wmin = float(np.nanmin(wave[valid]))
    wmax = float(np.nanmax(wave[valid]))
    if not (wmin <= hbeta <= wmax):
        raise RuntimeError(
            f"{path.name}: wavelength range {wmin:.4f}-{wmax:.4f} um does not cover "
            f"observed H-beta at {hbeta:.4f} um"
        )
    return {
        "source_ra": coords[0],
        "source_dec": coords[1],
        "sep_arcsec": sep,
        "wmin_um": wmin,
        "wmax_um": wmax,
        "hbeta_um": hbeta,
    }


def historical_v3_identity(row: dict[str, str]) -> tuple[str, str] | None:
    root = row["root"]
    file_name = row["file"]
    if "-v4" not in root or root not in file_name:
        return None
    v3_root = root.replace("-v4", "-v3")
    v3_file = file_name.replace(root, v3_root, 1)
    return v3_root, v3_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    target = manifest["target"]
    upstream = manifest["upstream"]
    acquisition = manifest["acquisition"]

    out = Path(args.out)
    raw = out / "raw"
    provenance = out / "provenance"
    raw.mkdir(parents=True, exist_ok=True)
    provenance.mkdir(parents=True, exist_ok=True)

    source_id = str(target["source_id"])
    redshift = float(target["redshift"])
    program = str(target["excels_program"])
    grating = str(target["excels_grating"]).lower()
    max_each = int(acquisition["max_file_mb"]) * 1024 * 1024
    max_total = int(acquisition["max_total_mb"]) * 1024 * 1024
    query_radius = float(acquisition.get("dja_radius_arcsec", 0.6))
    identity_radius = float(acquisition.get("identity_radius_arcsec", 0.2))
    receipts: list[dict[str, Any]] = []

    # 1. Authors' public MoM release: select the explicitly pinned source 150135.
    response = requests.get(upstream["zenodo_api"], timeout=60)
    response.raise_for_status()
    record = response.json()
    (provenance / "zenodo-record.json").write_text(json.dumps(record, indent=2, sort_keys=True))

    zenodo_candidates: list[Path] = []
    total = 0
    for item in record.get("files", []):
        key = str(item.get("key", ""))
        size = int(item.get("size") or 0)
        if not key.lower().endswith((".fits", ".fits.gz")):
            continue
        if size > max_each or total + size > max_total:
            continue
        url = item.get("links", {}).get("content") or item.get("links", {}).get("self")
        if not url:
            continue
        dest = raw / "zenodo" / Path(key).name
        receipt = download_limited(url, dest, max_each)
        receipt.update({"role": "zenodo_prism_candidate", "key": key})
        receipts.append(receipt)
        if receipt.get("downloaded"):
            total += dest.stat().st_size
            zenodo_candidates.append(dest)

    prism_source = choose_prism(zenodo_candidates, z=redshift, source_id=source_id)
    prism_path = raw / "mom_prism.fits"
    shutil.copyfile(prism_source, prism_path)
    coords = extract_coords(prism_source)
    if coords is None:
        raise RuntimeError(f"Could not recover source coordinates from {prism_source.name}")
    ra, dec = coords
    prism_validation = validate_spectrum(prism_path, ra, dec, redshift, identity_radius)
    receipts.append(
        {
            "role": "mom_prism_selected",
            "source_id": source_id,
            "source_file": prism_source.name,
            "bytes": prism_path.stat().st_size,
            "sha256": sha256(prism_path),
            "validation": prism_validation,
        }
    )

    # 2. DJA current coordinate service is the cross-survey identity witness.
    query_url = upstream["dja_query"].format(ra=f"{ra:.10f}", dec=f"{dec:.10f}", size=query_radius)
    current = requests.get(query_url, timeout=60)
    current.raise_for_status()
    (provenance / "dja-current-query.csv").write_text(current.text)
    rows = parse_dja_csv(current.text)

    candidates: list[dict[str, Any]] = []
    for row in rows:
        file_lower = (row.get("file") or "").lower()
        root_lower = (row.get("root") or "").lower()
        grating_value = (row.get("grating") or "").lower()
        try:
            sep = row_sep(row, ra, dec)
        except (KeyError, TypeError, ValueError):
            continue
        if not root_lower.startswith("excels-"):
            continue
        if f"_{program}_" not in file_lower:
            continue
        if grating not in file_lower and grating not in grating_value:
            continue
        if sep > identity_radius:
            continue
        candidates.append({**row, "sep_arcsec": sep})

    candidates.sort(key=lambda row: float(row["sep_arcsec"]))
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one EXCELS GO-{program} {grating.upper()} row within "
            f"{identity_radius:.3f} arcsec of MoM-BH*-1; found {candidates}"
        )
    exact = candidates[0]

    # 3. Prefer the historical v3 reduction used by Naidu et al. if the same
    # source ID exists at the conventional frozen-v3 path and validates itself.
    selected_path: Path | None = None
    selected_meta: dict[str, Any] | None = None
    historical = historical_v3_identity(exact)
    if historical is not None:
        v3_root, v3_file = historical
        v3_url = upstream["dja_file"].format(root=v3_root, file=v3_file)
        v3_tmp = raw / "excels_g395m_v3_candidate.fits"
        receipt = download_limited(v3_url, v3_tmp, max_each)
        receipt.update({"role": "excels_g395m_v3_probe", "root": v3_root, "file": v3_file})
        if receipt.get("downloaded"):
            try:
                validation = validate_spectrum(v3_tmp, ra, dec, redshift, identity_radius)
                receipt["validation"] = validation
                selected_path = v3_tmp
                selected_meta = {
                    "reduction": "DJA frozen v3 direct product",
                    "root": v3_root,
                    "file": v3_file,
                    "url": v3_url,
                    "cross_survey_srcid": exact.get("srcid"),
                    "discovered_from_current_row": exact,
                    "validation": validation,
                }
            except Exception as exc:
                receipt["validation_error"] = f"{type(exc).__name__}: {exc}"
        receipts.append(receipt)

    # 4. If v3 is absent or fails self-validation, use the exact current public
    # reduction returned by DJA. This is an honest Phase-0 preflight, not a claim
    # to reproduce the paper's exact reduction version.
    if selected_path is None:
        current_url = upstream["dja_file"].format(root=exact["root"], file=exact["file"])
        current_tmp = raw / "excels_g395m_current.fits"
        receipt = download_limited(current_url, current_tmp, max_each)
        receipt.update({"role": "excels_g395m_current", "root": exact["root"], "file": exact["file"]})
        if not receipt.get("downloaded"):
            receipts.append(receipt)
            raise RuntimeError(f"Exact DJA EXCELS product failed to download: {receipt}")
        validation = validate_spectrum(current_tmp, ra, dec, redshift, identity_radius)
        receipt["validation"] = validation
        receipts.append(receipt)
        selected_path = current_tmp
        selected_meta = {
            "reduction": "DJA current public reduction",
            "root": exact["root"],
            "file": exact["file"],
            "url": current_url,
            "cross_survey_srcid": exact.get("srcid"),
            "discovered_from_current_row": exact,
            "validation": validation,
        }

    final_path = raw / "excels_g395m.fits"
    shutil.copyfile(selected_path, final_path)
    selected_meta = dict(selected_meta or {})
    selected_meta.update({"bytes": final_path.stat().st_size, "sha256": sha256(final_path)})

    result = {
        "target": {
            "name": target["name"],
            "mom_source_id": source_id,
            "redshift": redshift,
            "source_ra": ra,
            "source_dec": dec,
        },
        "identity_rule": {
            "query_radius_arcsec": query_radius,
            "accept_radius_arcsec": identity_radius,
            "required_program": program,
            "required_grating": grating,
            "candidate_count": len(candidates),
        },
        "current_dja_rows": rows,
        "cross_survey_match": exact,
        "selected_excels": selected_meta,
        "sources": receipts,
    }
    (provenance / "acquisition-receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    )
    print(json.dumps(result["selected_excels"], indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
