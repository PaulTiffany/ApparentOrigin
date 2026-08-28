#!/usr/bin/env python3
"""Resolve the historical EXCELS G395M identity independently of MoM coordinates.

This is a diagnostic, not a scientific inference. It asks the frozen DJA v3
catalog for EXCELS G395M rows near the published redshift of MoM-BH*-1, then
records their archive identities and sky positions. That lets us cross-check
which FITS coordinate field in the MoM PRISM product is the actual source
position without widening a spatial match until something happens to fit.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from acquire import download_limited, normalize_dja_payload, strip_markup, hrefs


def numeric(value):
    text = strip_markup(value)
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def main() -> None:
    manifest = yaml.safe_load(Path("provenance/mom_bh1.yaml").read_text())
    target = manifest["target"]
    upstream = manifest["upstream"]
    acquisition = manifest["acquisition"]
    z0 = float(target["redshift"])
    grating = str(target["excels_grating"]).lower()

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

        candidates = []
        g395m_rows = 0
        excels_rows = 0
        for row in rows:
            root = strip_markup(row.get("root"))
            if not root.lower().startswith("excels-"):
                continue
            excels_rows += 1

            file_name = strip_markup(row.get("file"))
            # The frozen table's explicit grating cell can be blank; the archive
            # filename is authoritative enough for this diagnostic and encodes it.
            if grating not in file_name.lower():
                continue
            g395m_rows += 1

            z = numeric(row.get("z"))
            zfit = numeric(row.get("zfit"))
            z_values = [v for v in (z, zfit) if v is not None]
            dz = min((abs(v - z0) for v in z_values), default=None)
            if dz is None or dz > 0.15:
                continue

            candidates.append(
                {
                    "root": root,
                    "file": file_name,
                    "srcid": strip_markup(row.get("srcid")),
                    "ra": numeric(row.get("ra")),
                    "dec": numeric(row.get("dec")),
                    "z": z,
                    "zfit": zfit,
                    "delta_z": dz,
                    "grade": strip_markup(row.get("grade")),
                    "jname": strip_markup(row.get("jname")),
                    "fits_hrefs": hrefs(row.get("fits")),
                }
            )

        candidates.sort(key=lambda x: x["delta_z"])
        result = {
            "target": {"name": target["name"], "redshift": z0},
            "catalog": {**receipt, "rows": len(rows)},
            "excels_rows": excels_rows,
            "excels_g395m_rows": g395m_rows,
            "selection_rule": "EXCELS root + G395M encoded in filename + |z or zfit - 7.7569| <= 0.15",
            "candidates": candidates[:50],
            "candidate_count": len(candidates),
            "warning": "Identity is not accepted until archive redshift, spectrum coverage, and MoM sky position are independently reconciled.",
        }
        (out / "dja-v3-redshift-identity.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        catalog.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
