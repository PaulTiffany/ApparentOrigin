#!/usr/bin/env python3
"""One-shot diagnostic for resolving MoM-BH*-1's EXCELS identity.

This intentionally downloads the official DJA v4.4 merged *metadata* catalog
only after normal bounded acquisition has failed. The file is deleted after
coordinate cross-matching and is never uploaded as an artifact. Once the exact
EXCELS identity is known, remove this diagnostic and pin the small spectrum
product directly in provenance/mom_bh1.yaml.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import requests

CATALOG_URL = (
    "https://zenodo.org/records/15472354/files/"
    "dja_msaexp_emission_lines_v4.4.csv.gz"
)
TMP = Path("run/dja_msaexp_emission_lines_v4.4.csv.gz")
OUT = Path("run/provenance/dja-v4.4-coordinate-match.json")
DIAG = Path("run/provenance/dja-v3-discovery.json")


def angular_sep_arcsec(ra1: np.ndarray, dec1: np.ndarray, ra2: float, dec2: float) -> np.ndarray:
    dra = (ra1 - ra2) * np.cos(np.radians((dec1 + dec2) / 2.0))
    ddec = dec1 - dec2
    return np.hypot(dra, ddec) * 3600.0


def jsonable(value):
    if value is None:
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, float):
        return None if not math.isfinite(value) else value
    if pd.isna(value):
        return None
    return str(value) if not isinstance(value, (str, int, bool)) else value


def main() -> None:
    if not DIAG.exists():
        raise RuntimeError(f"Missing acquisition diagnostic {DIAG}")
    diagnostic = json.loads(DIAG.read_text())
    target = diagnostic["target"]
    ra0 = float(target["ra"])
    dec0 = float(target["dec"])

    TMP.parent.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(CATALOG_URL, stream=True, timeout=180) as response:
        response.raise_for_status()
        with TMP.open("wb") as handle:
            for block in response.iter_content(chunk_size=4 * 1024 * 1024):
                if block:
                    handle.write(block)

    closest: list[dict] = []
    try:
        for chunk in pd.read_csv(TMP, compression="gzip", chunksize=10000, low_memory=False):
            required = {"root", "ra", "dec", "grating"}
            if not required.issubset(chunk.columns):
                raise RuntimeError(f"DJA catalog missing required columns: {required - set(chunk.columns)}")

            root = chunk["root"].astype(str).str.lower()
            grating = chunk["grating"].astype(str).str.lower()
            mask = root.str.startswith("excels-") & grating.str.contains("g395m", na=False)
            if not mask.any():
                continue

            sub = chunk.loc[mask].copy()
            ra = pd.to_numeric(sub["ra"], errors="coerce").to_numpy(float)
            dec = pd.to_numeric(sub["dec"], errors="coerce").to_numpy(float)
            sep = angular_sep_arcsec(ra, dec, ra0, dec0)
            sub["sep_arcsec"] = sep
            sub = sub[np.isfinite(sub["sep_arcsec"]) & (sub["sep_arcsec"] <= 10.0)]
            if sub.empty:
                continue

            preferred = [
                "root", "file", "ra", "dec", "srcid", "slitid", "grating",
                "exptime", "wmin", "wmax", "sn50", "version", "zfit", "z",
                "grade", "has_v3", "flam_v3", "fnu", "flam", "sep_arcsec",
            ]
            columns = [c for c in preferred if c in sub.columns]
            for _, row in sub[columns].iterrows():
                closest.append({key: jsonable(value) for key, value in row.items()})
    finally:
        TMP.unlink(missing_ok=True)

    closest.sort(key=lambda row: float(row["sep_arcsec"]))
    payload = {
        "catalog_url": CATALOG_URL,
        "target": {"ra": ra0, "dec": dec0},
        "matches_within_10_arcsec": closest[:30],
        "note": (
            "Diagnostic only. Do not accept a row as MoM-BH*-1 solely because it is nearest; "
            "verify program/grating, coordinate agreement, and redshift/line identity before pinning."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
