#!/usr/bin/env python3
"""Inspect the fetched EXCELS spectrum and create controlled resolution-thinned views."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits

C_KMS = 299792.458


def first_spectral_table(path: Path):
    with fits.open(path, memmap=False) as hdul:
        schema = []
        for i, hdu in enumerate(hdul):
            columns = []
            if getattr(hdu, "columns", None) is not None:
                columns = list(hdu.columns.names or [])
            schema.append(
                {
                    "index": i,
                    "name": hdu.name,
                    "class": hdu.__class__.__name__,
                    "shape": list(hdu.data.shape) if getattr(hdu, "data", None) is not None and hasattr(hdu.data, "shape") else None,
                    "columns": columns,
                }
            )

            if not columns or hdu.data is None:
                continue
            lower = {name.lower(): name for name in columns}
            wave_name = next((lower[k] for k in ("wave", "wavelength", "lam", "lambda") if k in lower), None)
            flux_name = next((lower[k] for k in ("flux", "fnu", "flam") if k in lower), None)
            err_name = next((lower[k] for k in ("err", "error", "full_err", "flux_err", "sigma") if k in lower), None)
            if wave_name and flux_name:
                wave = np.asarray(hdu.data[wave_name], dtype=float).squeeze()
                flux = np.asarray(hdu.data[flux_name], dtype=float).squeeze()
                err = np.asarray(hdu.data[err_name], dtype=float).squeeze() if err_name else np.full_like(flux, np.nan)
                return wave, flux, err, {"hdu_index": i, "wave": wave_name, "flux": flux_name, "err": err_name}, schema

    raise RuntimeError(f"No table HDU with recognizable wavelength/flux columns found in {path}")


def finite_sorted(wave, flux, err):
    mask = np.isfinite(wave) & np.isfinite(flux) & (wave > 0)
    wave, flux, err = wave[mask], flux[mask], err[mask]
    order = np.argsort(wave)
    return wave[order], flux[order], err[order]


def gaussian_kernel(sigma_pix: float) -> np.ndarray:
    if sigma_pix <= 0.05:
        return np.array([1.0])
    radius = max(3, int(math.ceil(5 * sigma_pix)))
    x = np.arange(-radius, radius + 1, dtype=float)
    kernel = np.exp(-0.5 * (x / sigma_pix) ** 2)
    return kernel / kernel.sum()


def degrade_resolution(wave, flux, err, native_r: float, target_r: float):
    if target_r >= native_r:
        return wave.copy(), flux.copy(), err.copy()

    log_wave = np.log(wave)
    dlog = np.nanmedian(np.diff(log_wave))
    if not np.isfinite(dlog) or dlog <= 0:
        raise RuntimeError("Cannot establish a positive logarithmic wavelength spacing")

    grid = np.arange(log_wave[0], log_wave[-1] + dlog / 2, dlog)
    wave_grid = np.exp(grid)
    flux_grid = np.interp(grid, log_wave, flux)
    var_grid = np.interp(grid, log_wave, np.square(err), left=np.nan, right=np.nan)

    # For a Gaussian line-spread function, FWHM_v ~= c/R.
    fwhm_extra_v = C_KMS * math.sqrt(max(0.0, target_r ** -2 - native_r ** -2))
    sigma_extra_v = fwhm_extra_v / 2.354820045
    sigma_pix = (sigma_extra_v / C_KMS) / dlog
    kernel = gaussian_kernel(sigma_pix)

    flux_out = np.convolve(flux_grid, kernel, mode="same")
    # Independent input errors propagated through the normalized convolution.
    finite_var = np.nan_to_num(var_grid, nan=0.0, posinf=0.0, neginf=0.0)
    var_out = np.convolve(finite_var, np.square(kernel), mode="same")
    err_out = np.sqrt(var_out)
    return wave_grid, flux_out, err_out


def write_csv(path: Path, wave, flux, err):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["wavelength", "flux", "error"])
        writer.writerows(zip(wave, flux, err))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw/dja")
    parser.add_argument("--out", default="results/thinned")
    parser.add_argument("--native-r", type=float, default=1500.0)
    parser.add_argument("--targets", default="1200,900,600,450,300,150")
    args = parser.parse_args()

    fits_files = sorted(Path(args.raw_dir).glob("*.fits")) + sorted(Path(args.raw_dir).glob("*.fits.gz"))
    if len(fits_files) != 1:
        raise RuntimeError(f"Expected exactly one fetched DJA G395M FITS file, found {len(fits_files)}")

    source = fits_files[0]
    wave, flux, err, mapping, schema = first_spectral_table(source)
    wave, flux, err = finite_sorted(wave, flux, err)
    if len(wave) < 20:
        raise RuntimeError("Spectrum has too few finite samples for controlled thinning")

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    targets = [float(x) for x in args.targets.split(",") if x.strip()]
    products = []

    write_csv(outdir / f"R{int(args.native_r)}.csv", wave, flux, err)
    products.append({"R": args.native_r, "samples": len(wave), "file": f"R{int(args.native_r)}.csv"})

    for target in targets:
        tw, tf, te = degrade_resolution(wave, flux, err, args.native_r, target)
        filename = f"R{int(target)}.csv"
        write_csv(outdir / filename, tw, tf, te)
        products.append({"R": target, "samples": len(tw), "file": filename})

    report = {
        "source": source.name,
        "column_mapping": mapping,
        "fits_schema": schema,
        "native_resolution_assumption": args.native_r,
        "wavelength_min": float(np.nanmin(wave)),
        "wavelength_max": float(np.nanmax(wave)),
        "products": products,
        "note": "These are controlled observational views, not independent observations and not BH-mass inferences.",
    }
    (outdir.parent / "spectrum_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
