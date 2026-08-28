#!/usr/bin/env python3
"""Diagnose the historical EXCELS G395M identity from independent keys.

Diagnostic only. We intentionally do not widen a spatial match until something
fits. Instead we compare four archive witnesses against the pinned MoM PRISM
product: source ID tokens, exact source coordinates, EXCELS/G395M membership,
and the published redshift. No candidate is accepted automatically.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from acquire import (
    angular_sep_arcsec,
    download_limited,
    extract_coords,
    hrefs,
    normalize_dja_payload,
    strip_markup,
)


def numeric(value):
    text = strip_markup(value)
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def summarize(row, target_ra=None, target_dec=None):
    ra = numeric(row.get("ra"))
    dec = numeric(row.get("dec"))
    sep = None
    if None not in (ra, dec, target_ra, target_dec):
        sep = angular_sep_arcsec(float(target_ra), float(target_dec), ra, dec)
    return {
        "jname": strip_markup(row.get("jname")),
        "root": strip_markup(row.get("root")),
        "file": strip_markup(row.get("file")),
        "srcid": strip_markup(row.get("srcid")),
        "ra": ra,
        "dec": dec,
        "sep_arcsec": sep,
        "grade": strip_markup(row.get("grade")),
        "z": numeric(row.get("z")),
        "zfit": numeric(row.get("zfit")),
        "grating_cell": strip_markup(row.get("grating")),
        "fits_hrefs": hrefs(row.get("fits")),
    }


def main() -> None:
    manifest = yaml.safe_load(Path("provenance/mom_bh1.yaml").read_text())
    target = manifest["target"]
    upstream = manifest["upstream"]
    acquisition = manifest["acquisition"]
    z0 = float(target["redshift"])
    source_id = str(target["source_id"])
    grating = str(target["excels_grating"]).lower()

    prism = Path("run/raw/mom_prism.fits")
    if not prism.exists():
        raise RuntimeError(f"Missing selected MoM spectrum: {prism}")
    coords = extract_coords(prism)
    if coords is None:
        raise RuntimeError("Could not recover SRCRA/SRCDEC from selected MoM spectrum")
    target_ra, target_dec = coords

    out = Path("run/provenance")
    raw = Path("run/raw")
    out.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)

    catalog = raw / "nirspec_graded_v3.identity.json"
    cap = int(acquisition["max_total_mb"]) * 1024 * 1024
    receipt = download_limited(upstream["dja_v3_catalog_json"], catalog, cap)
    if not receipt.get("downloaded"):
        raise RuntimeError(f"Could not download frozen v3 JSON: {receipt}")

    try:
        payload = json.loads(catalog.read_text(encoding="utf-8"))
        rows = normalize_dja_payload(payload)

        source_token_rows = []
        spatial_rows = []
        excels_spatial_rows = []
        redshift_rows = []
        excels_rows = 0
        excels_g395m_rows = 0

        for row in rows:
            item = summarize(row, target_ra, target_dec)
            root_lower = item["root"].lower()
            file_lower = item["file"].lower()
            is_excels = root_lower.startswith("excels-")
            is_g395m = grating in file_lower

            if is_excels:
                excels_rows += 1
            if is_excels and is_g395m:
                excels_g395m_rows += 1

            if item["srcid"] == source_id or f"_{source_id}.spec.fits" in file_lower:
                source_token_rows.append(item)

            if item["sep_arcsec"] is not None and item["sep_arcsec"] <= 10.0:
                spatial_rows.append(item)
            if is_excels and item["sep_arcsec"] is not None and item["sep_arcsec"] <= 30.0:
                excels_spatial_rows.append(item)

            if is_excels and is_g395m:
                z_values = [v for v in (item["z"], item["zfit"]) if v is not None]
                dz = min((abs(v - z0) for v in z_values), default=None)
                if dz is not None and dz <= 0.15:
                    item = {**item, "delta_z": dz}
                    redshift_rows.append(item)

        source_token_rows.sort(key=lambda x: (x["sep_arcsec"] is None, x["sep_arcsec"] or 1e99))
        spatial_rows.sort(key=lambda x: x["sep_arcsec"] or 1e99)
        excels_spatial_rows.sort(key=lambda x: x["sep_arcsec"] or 1e99)
        redshift_rows.sort(key=lambda x: x["delta_z"])

        result = {
            "target": {
                "name": target["name"],
                "mom_source_id": source_id,
                "redshift": z0,
                "mom_source_ra": target_ra,
                "mom_source_dec": target_dec,
            },
            "catalog": {**receipt, "rows": len(rows)},
            "excels_rows": excels_rows,
            "excels_g395m_rows": excels_g395m_rows,
            "witnesses": {
                "same_source_id_or_filename_token": source_token_rows[:50],
                "all_archive_rows_within_10_arcsec": spatial_rows[:100],
                "excels_rows_within_30_arcsec": excels_spatial_rows[:100],
                "excels_g395m_within_delta_z_0_15": redshift_rows[:50],
            },
            "warning": (
                "No row is accepted by this diagnostic. Pin an EXCELS product only after "
                "its archive identity, source position, spectral coverage, and association "
                "with the published MoM-BH*-1 observation agree independently."
            ),
        }
        (out / "dja-v3-identity-diagnostic.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        catalog.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
