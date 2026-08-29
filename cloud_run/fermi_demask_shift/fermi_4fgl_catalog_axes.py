"""Build a Fermi-derived catalog axis table from 4FGL-DR4.

This is a passive archival-data extractor. It downloads/reads the public
Fermi-LAT 14-year Source Catalog (4FGL-DR4), computes low-order directional
axes for declared catalog voices and mask states, and writes the generic
SharedShift `axes.csv` format:

    voice,mask,band,x,y,z,grade

Classification: Fermi-derived catalog axis table.

This is not a residual-map analysis and not a Fermi science result by itself.
It is the first minimal Fermi-derived input for the demask-shift CI harness.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import urllib.request
from pathlib import Path

import numpy as np
from astropy.io import fits


DEFAULT_CATALOG_URL = (
    "https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/gll_psc_v35.fit"
)


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    with urllib.request.urlopen(url, timeout=120) as response:
        path.write_bytes(response.read())


def colname(names: list[str], *candidates: str) -> str | None:
    lower = {name.lower(): name for name in names}
    for candidate in candidates:
        found = lower.get(candidate.lower())
        if found is not None:
            return found
    return None


def finite_array(table, name: str, default: float = np.nan) -> np.ndarray:
    if name is None:
        return np.full(len(table), default, dtype=float)
    values = np.asarray(table[name], dtype=float)
    if values.ndim > 1:
        values = np.asarray(values[:, 0], dtype=float)
    return values


def text_array(table, name: str | None) -> np.ndarray:
    if name is None:
        return np.array([""] * len(table), dtype=str)
    return np.char.strip(np.asarray(table[name]).astype(str))


def lonlat_to_unit(glon_deg: np.ndarray, glat_deg: np.ndarray) -> np.ndarray:
    lon = np.radians(glon_deg)
    lat = np.radians(glat_deg)
    return np.column_stack(
        [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)]
    )


def principal_axis(units: np.ndarray, weights: np.ndarray) -> np.ndarray | None:
    valid = (
        np.isfinite(units).all(axis=1)
        & np.isfinite(weights)
        & (weights > 0)
    )
    units = units[valid]
    weights = weights[valid]
    if len(units) < 3:
        return None
    tensor = np.einsum("i,ij,ik->jk", weights, units, units)
    tensor /= float(np.sum(weights))
    eigvals, eigvecs = np.linalg.eigh(tensor)
    axis = eigvecs[:, int(np.argmax(eigvals))]
    if axis[2] < 0:
        axis = -axis
    norm = np.linalg.norm(axis)
    if norm == 0:
        return None
    return axis / norm


def robust_positive(values: np.ndarray, fallback: float = 1.0) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    bad = ~np.isfinite(out) | (out <= 0)
    out[bad] = fallback
    return out


def source_masks(table) -> dict[str, np.ndarray]:
    names = list(table.names)
    glon_name = colname(names, "GLON", "glon")
    glat_name = colname(names, "GLAT", "glat")
    flags_name = colname(names, "Flags", "FLAGS")
    signif_name = colname(names, "Signif_Avg", "SignifAvg", "Significance")
    index_name = colname(names, "PL_Index", "LP_Index", "Spectral_Index")
    var_name = colname(names, "Variability_Index", "Variability")
    class_name = colname(names, "CLASS1", "CLASS")
    flux_name = colname(names, "Energy_Flux100", "Energy_Flux", "Flux1000")

    glon = finite_array(table, glon_name)
    glat = finite_array(table, glat_name)
    flags = finite_array(table, flags_name, default=0.0)
    signif = finite_array(table, signif_name, default=1.0)
    index = finite_array(table, index_name)
    variability = finite_array(table, var_name, default=0.0)
    energy_flux = finite_array(table, flux_name, default=1.0)
    classes = np.char.lower(text_array(table, class_name))

    base = np.isfinite(glon) & np.isfinite(glat)
    clean = base & (flags == 0)
    with_index = clean & np.isfinite(index)
    median_index = float(np.nanmedian(index[with_index])) if np.any(with_index) else 2.3
    with_var = clean & np.isfinite(variability)
    median_var = float(np.nanmedian(variability[with_var])) if np.any(with_var) else 0.0

    agn_like = clean & (
        (np.char.find(classes, "bll") >= 0)
        | (np.char.find(classes, "fsrq") >= 0)
        | (np.char.find(classes, "bcu") >= 0)
        | (np.char.find(classes, "agn") >= 0)
    )

    return {
        "base": base,
        "clean": clean,
        "signif": robust_positive(signif),
        "energy_flux": robust_positive(energy_flux),
        "hard": with_index & (index <= median_index),
        "soft": with_index & (index > median_index),
        "steady": with_var & (variability <= median_var),
        "variable": with_var & (variability > median_var),
        "agn_like": agn_like,
    }


def mask_state(glat: np.ndarray, flags: np.ndarray, state: str) -> np.ndarray:
    abs_b = np.abs(glat)
    if state == "M0":
        return np.isfinite(glat)
    if state == "M1":
        return abs_b > 10.0
    if state == "M2":
        return abs_b > 20.0
    if state == "M3":
        return abs_b > 30.0
    if state == "M4":
        return (abs_b > 20.0) & (flags == 0)
    raise ValueError(f"unknown mask state: {state}")


def build_axes(catalog_path: Path) -> tuple[list[dict], dict]:
    with fits.open(catalog_path, memmap=True) as hdul:
        table = hdul[1].data
        names = list(table.names)
        glon_name = colname(names, "GLON", "glon")
        glat_name = colname(names, "GLAT", "glat")
        flags_name = colname(names, "Flags", "FLAGS")
        if glon_name is None or glat_name is None:
            raise ValueError("4FGL catalog missing GLON/GLAT columns")
        glon = finite_array(table, glon_name)
        glat = finite_array(table, glat_name)
        flags = finite_array(table, flags_name, default=0.0)
        units = lonlat_to_unit(glon, glat)
        masks = source_masks(table)

    voices = [
        ("all_sources_count", masks["base"], np.ones_like(glon), "C"),
        ("clean_sources_count", masks["clean"], np.ones_like(glon), "C"),
        ("clean_energy_flux_weighted", masks["clean"], masks["energy_flux"], "C"),
        ("clean_significance_weighted", masks["clean"], masks["signif"], "C"),
        ("hard_spectrum_count", masks["hard"], np.ones_like(glon), "C"),
        ("soft_spectrum_count", masks["soft"], np.ones_like(glon), "C"),
        ("steady_sources_count", masks["steady"], np.ones_like(glon), "C"),
        ("variable_sources_count", masks["variable"], np.ones_like(glon), "C"),
        ("agn_like_count", masks["agn_like"], np.ones_like(glon), "C"),
    ]

    rows: list[dict] = []
    diagnostics: dict = {"catalog_rows": int(len(glon)), "voices": {}, "mask_states": {}}
    for state in ["M0", "M1", "M2", "M3", "M4"]:
        state_mask = mask_state(glat, flags, state)
        diagnostics["mask_states"][state] = int(np.sum(state_mask))
        for voice, voice_mask, weights, grade in voices:
            selection = state_mask & voice_mask
            axis = principal_axis(units[selection], weights[selection])
            diagnostics["voices"].setdefault(voice, {})[state] = int(np.sum(selection))
            if axis is None:
                continue
            rows.append(
                {
                    "voice": voice,
                    "mask": state,
                    "band": "catalog_principal_axis",
                    "x": float(axis[0]),
                    "y": float(axis[1]),
                    "z": float(axis[2]),
                    "grade": grade,
                }
            )
    return rows, diagnostics


def write_axes(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["voice", "mask", "band", "x", "y", "z", "grade"]
        )
        writer.writeheader()
        writer.writerows(rows)


def write_docs(out_dir: Path, catalog_url: str, diagnostics: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RUN_CLASSIFICATION.md").write_text(
        "# Run Classification\n\n"
        "Classification: Fermi-derived catalog axis table.\n\n"
        "This is derived from the public Fermi-LAT 14-year Source Catalog "
        "(4FGL-DR4), not from Fermi residual maps. It is a staged catalog "
        "axis run and is not a Fermi residual-sky science result.\n\n"
        "No quantum resources or physical intervention are used.\n",
        encoding="utf-8",
    )
    (out_dir / "DATA_PROVENANCE.md").write_text(
        "# Data Provenance\n\n"
        f"Catalog URL: `{catalog_url}`\n\n"
        "Source: Fermi Science Support Center LAT 14-year Source Catalog "
        "(4FGL-DR4) FITS product.\n\n"
        "Catalog description: 14 years of Fermi-LAT survey data in the "
        "50 MeV to 1 TeV energy range; source catalog, not residual map.\n\n"
        f"Rows in catalog: `{diagnostics['catalog_rows']}`\n\n"
        "No quantum resources, quantum simulators, Qiskit backends, or "
        "physical intervention are used.\n",
        encoding="utf-8",
    )
    (out_dir / "MASK_DEFINITIONS.md").write_text(
        "# Mask Definitions\n\n"
        "| mask | definition |\n"
        "| --- | --- |\n"
        "| M0 | no Galactic latitude cut |\n"
        "| M1 | `abs(GLAT) > 10 deg` |\n"
        "| M2 | `abs(GLAT) > 20 deg` |\n"
        "| M3 | `abs(GLAT) > 30 deg` |\n"
        "| M4 | `abs(GLAT) > 20 deg` and `Flags == 0` |\n\n"
        "These are catalog-selection masks, not residual-map masks.\n",
        encoding="utf-8",
    )
    (out_dir / "AXIS_EXTRACTION_METHOD.md").write_text(
        "# Axis Extraction Method\n\n"
        "For each voice and mask state:\n\n"
        "1. Select catalog sources by the declared voice rule and mask rule.\n"
        "2. Convert source `GLON`, `GLAT` to unit vectors.\n"
        "3. Build the weighted second-moment tensor `T = sum_i w_i n_i n_i^T / sum_i w_i`.\n"
        "4. Use the eigenvector with largest eigenvalue as the axial direction.\n"
        "5. Orient the representative to positive `z` for stable CSV output.\n\n"
        "Axes are interpreted axially by the SharedShift runner: `u == -u`.\n",
        encoding="utf-8",
    )
    (out_dir / "VOICE_INDEPENDENCE_LEDGER.md").write_text(
        "# Voice Independence Ledger\n\n"
        "Classification: Fermi-derived catalog axis table.\n\n"
        "All voices are catalog-selection or catalog-weighting voices over the "
        "same 4FGL-DR4 source catalog. They are grade C: useful for staged "
        "validation and first Fermi-derived contact, but not independent "
        "residual-map reconstructions.\n\n"
        "| voice | rule | grade |\n"
        "| --- | --- | --- |\n"
        "| all_sources_count | all finite GLON/GLAT sources, weight=1 | C |\n"
        "| clean_sources_count | Flags==0, weight=1 | C |\n"
        "| clean_energy_flux_weighted | Flags==0, weight=energy flux | C |\n"
        "| clean_significance_weighted | Flags==0, weight=Signif_Avg | C |\n"
        "| hard_spectrum_count | clean sources with spectral index <= median | C |\n"
        "| soft_spectrum_count | clean sources with spectral index > median | C |\n"
        "| steady_sources_count | clean sources with variability <= median | C |\n"
        "| variable_sources_count | clean sources with variability > median | C |\n"
        "| agn_like_count | clean AGN-like CLASS1 labels | C |\n",
        encoding="utf-8",
    )
    (out_dir / "FORBIDDEN_CLAIMS.md").write_text(
        "# Forbidden Claims\n\n"
        "Do not claim:\n\n"
        "1. This is a Fermi residual-map result.\n"
        "2. This validates AOC.\n"
        "3. This proves physical spin, recurrence, doom, or hazard.\n"
        "4. Catalog source-selection voices are independent sky reconstructions.\n"
        "5. Numeric-only SharedShift output is a calibrated detection.\n"
        "6. Any quantum resource, quantum simulator, Qiskit backend, or physical "
        "intervention was used.\n\n"
        "Allowed minimal claim: a public Fermi catalog-derived axis table was "
        "generated and is ready for passive SharedShift evaluation.\n",
        encoding="utf-8",
    )
    (out_dir / "diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-url", default=DEFAULT_CATALOG_URL)
    parser.add_argument("--catalog-path", type=Path, default=Path("data/fermi/gll_psc_v35.fit"))
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    download(args.catalog_url, args.catalog_path)
    rows, diagnostics = build_axes(args.catalog_path)
    write_axes(args.out_dir / "axes.csv", rows)
    write_docs(args.out_dir, args.catalog_url, diagnostics)
    print(f"wrote {len(rows)} Fermi catalog axis rows to {args.out_dir / 'axes.csv'}")


if __name__ == "__main__":
    main()
