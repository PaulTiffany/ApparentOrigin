#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from astropy.io import fits
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

C_KMS = 299792.458
HBETA_REST_UM = 0.4861333


def load_spec1d(path: Path) -> dict[str, np.ndarray]:
    with fits.open(path, memmap=False) as hdul:
        hdu = next((h for h in hdul if h.name.upper() == "SPEC1D" and h.data is not None), None)
        if hdu is None or not getattr(hdu.data, "names", None):
            raise RuntimeError(f"{path} has no SPEC1D binary table.")
        names = {n.lower(): n for n in hdu.data.names}
        for needed in ("wave", "flux"):
            if needed not in names:
                raise RuntimeError(f"{path} SPEC1D missing required column {needed!r}.")
        out = {
            "wave": np.asarray(hdu.data[names["wave"]], dtype=float),
            "flux": np.asarray(hdu.data[names["flux"]], dtype=float),
        }
        err_key = names.get("full_err") or names.get("err")
        out["err"] = (
            np.asarray(hdu.data[err_key], dtype=float)
            if err_key
            else np.full_like(out["flux"], np.nan)
        )
        valid_key = names.get("valid")
        out["valid"] = (
            np.asarray(hdu.data[valid_key], dtype=bool)
            if valid_key
            else np.isfinite(out["wave"]) & np.isfinite(out["flux"])
        )
        r_key = names.get("r")
        out["R"] = (
            np.asarray(hdu.data[r_key], dtype=float)
            if r_key
            else np.full_like(out["flux"], np.nan)
        )
        return out


def gaussian_degrade(
    wave: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    native_r: float,
    target_r: float,
    center_um: float,
) -> tuple[np.ndarray, np.ndarray]:
    if target_r >= native_r:
        return flux.copy(), err.copy()
    dw = float(np.nanmedian(np.diff(wave)))
    if not np.isfinite(dw) or dw <= 0:
        raise ValueError("Wavelength grid must be increasing.")
    fwhm_native = center_um / native_r
    fwhm_target = center_um / target_r
    fwhm_add = math.sqrt(max(0.0, fwhm_target**2 - fwhm_native**2))
    sigma_pix = (fwhm_add / 2.354820045) / dw
    if sigma_pix <= 0:
        return flux.copy(), err.copy()
    good = np.isfinite(err) & (err > 0)
    fallback = float(np.nanmedian(err[good])) if good.any() else 1.0
    good_err = np.where(good, err, fallback)
    smooth_flux = gaussian_filter1d(flux, sigma=sigma_pix, mode="nearest")
    smooth_var = gaussian_filter1d(good_err**2, sigma=sigma_pix, mode="nearest")
    return smooth_flux, np.sqrt(np.maximum(smooth_var, 1e-30))


def virial_like(x, c0, c1, amp, mu, sigma):
    return c0 + c1 * (x - mu) + amp * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def structured(x, c0, c1, amp, mu, sigma, abs_amp, abs_mu, abs_sigma):
    emission = virial_like(x, c0, c1, amp, mu, sigma)
    absorption = abs_amp * np.exp(-0.5 * ((x - abs_mu) / abs_sigma) ** 2)
    return emission - absorption


def bic(y: np.ndarray, model: np.ndarray, err: np.ndarray, k: int) -> tuple[float, float]:
    resid = (y - model) / err
    chi2 = float(np.sum(resid**2))
    n = int(y.size)
    return chi2 + k * math.log(n), chi2


def strictly_feasible(p0: list[float], bounds: tuple[list[float], list[float]]) -> list[float]:
    """Move optimizer seeds just inside existing bounds without changing them."""
    lower, upper = bounds
    out: list[float] = []
    for value, lo, hi in zip(p0, lower, upper):
        x = float(value)
        if np.isfinite(lo) and x <= lo:
            x = float(np.nextafter(float(lo), np.inf))
        if np.isfinite(hi) and x >= hi:
            x = float(np.nextafter(float(hi), -np.inf))
        out.append(x)
    return out


def fit_models(
    wave: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    center: float,
) -> dict[str, float]:
    finite = np.isfinite(wave) & np.isfinite(flux) & np.isfinite(err) & (err > 0)
    wave = wave[finite]
    flux = flux[finite]
    err = err[finite]
    if wave.size < 25:
        raise RuntimeError("Not enough valid samples in H-beta window.")

    edge = max(3, wave.size // 8)
    cont = float(np.nanmedian(np.r_[flux[:edge], flux[-edge:]]))
    amp0 = max(float(np.nanmax(flux) - cont), float(np.nanstd(flux)), 1e-6)
    sigma0 = 0.018
    span = float(wave.max() - wave.min())

    bounds_v = (
        [-np.inf, -np.inf, 0.0, center - 0.025, 0.002],
        [np.inf, np.inf, np.inf, center + 0.025, min(0.08, span / 2)],
    )
    p0_v = strictly_feasible([cont, 0.0, amp0, center, sigma0], bounds_v)
    popt_v, _ = curve_fit(
        virial_like,
        wave,
        flux,
        p0=p0_v,
        sigma=err,
        absolute_sigma=True,
        bounds=bounds_v,
        maxfev=50000,
    )
    pred_v = virial_like(wave, *popt_v)
    bic_v, chi2_v = bic(flux, pred_v, err, len(popt_v))

    residual = pred_v - flux
    # The structured model predeclares absorption within +/-0.03 um of H-beta.
    # Seed from the largest positive residual *inside that same region* rather
    # than letting an unrelated edge residual create an infeasible p0.
    absorption_region = np.abs(wave - center) <= 0.030
    if not absorption_region.any():
        raise RuntimeError("No samples inside the predeclared H-beta absorption region.")
    candidate_indices = np.flatnonzero(absorption_region)
    abs_idx = int(candidate_indices[np.nanargmax(residual[absorption_region])])
    abs_mu0 = float(wave[abs_idx])
    abs_amp0 = max(float(residual[abs_idx]), float(np.nanmedian(err)), 1e-6)

    bounds_s = (
        [
            -np.inf,
            -np.inf,
            0.0,
            center - 0.025,
            0.002,
            0.0,
            center - 0.030,
            0.0005,
        ],
        [
            np.inf,
            np.inf,
            np.inf,
            center + 0.025,
            min(0.08, span / 2),
            np.inf,
            center + 0.030,
            0.020,
        ],
    )
    p0_s = strictly_feasible([*popt_v, abs_amp0, abs_mu0, 0.004], bounds_s)
    popt_s, _ = curve_fit(
        structured,
        wave,
        flux,
        p0=p0_s,
        sigma=err,
        absolute_sigma=True,
        bounds=bounds_s,
        maxfev=80000,
    )
    pred_s = structured(wave, *popt_s)
    bic_s, chi2_s = bic(flux, pred_s, err, len(popt_s))

    fwhm_um = 2.354820045 * abs(float(popt_v[4]))
    fwhm_kms = fwhm_um / float(popt_v[3]) * C_KMS
    # Literature-anchored proxy only: keep continuum luminosity fixed and use M ~ FWHM^2.
    logm_proxy = 8.3 + 2.0 * math.log10(max(fwhm_kms, 1e-9) / 3036.0)

    return {
        "bic_virial_like": bic_v,
        "bic_structured": bic_s,
        "delta_bic": bic_v - bic_s,
        "chi2_virial_like": chi2_v,
        "chi2_structured": chi2_s,
        "fwhm_virial_like_kms": fwhm_kms,
        "log10_mbh_virial_proxy": logm_proxy,
        "absorption_depth_fit": float(popt_s[5]),
        "absorption_center_um": float(popt_s[6]),
        "absorption_sigma_um": float(popt_s[7]),
    }


def run_resolution_ladder(
    spec: dict[str, np.ndarray],
    z: float,
    target_rs: list[float],
    half_window_um: float,
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    center = HBETA_REST_UM * (1 + z)
    mask = (
        spec["valid"]
        & np.isfinite(spec["wave"])
        & np.isfinite(spec["flux"])
        & (np.abs(spec["wave"] - center) <= half_window_um)
    )
    wave = spec["wave"][mask]
    flux = spec["flux"][mask]
    err = spec["err"][mask]
    rr = spec["R"][mask]
    order = np.argsort(wave)
    wave, flux, err, rr = wave[order], flux[order], err[order], rr[order]

    native_values = rr[np.isfinite(rr) & (rr > 0)]
    native_r = float(np.nanmedian(native_values)) if native_values.size else 1000.0

    # Regrid once locally so synthetic convolution has a well-defined pixel scale.
    uniform_wave = np.linspace(float(wave.min()), float(wave.max()), wave.size)
    uniform_flux = np.interp(uniform_wave, wave, flux)
    good = np.isfinite(err) & (err > 0)
    fallback = float(np.nanmedian(err[good])) if good.any() else 1.0
    good_err = np.where(good, err, fallback)
    uniform_err = np.interp(uniform_wave, wave, good_err)

    ladder = [native_r] + [r for r in target_rs if r < native_r * 0.98]
    rows = []
    profiles: dict[str, np.ndarray] = {"wave": uniform_wave, "native_flux": uniform_flux}
    for r in ladder:
        dflux, derr = gaussian_degrade(
            uniform_wave,
            uniform_flux,
            uniform_err,
            native_r=native_r,
            target_r=float(r),
            center_um=center,
        )
        fit = fit_models(uniform_wave, dflux, derr, center=center)
        fit["target_R"] = float(r)
        fit["native_R"] = native_r
        rows.append(fit)
        profiles[f"R_{int(round(r))}"] = dflux

    df = pd.DataFrame(rows).sort_values("target_R", ascending=False).reset_index(drop=True)
    return df, profiles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="run/raw/excels_g395m.fits")
    parser.add_argument("--prism", default="run/raw/mom_prism.fits")
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run/results")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    z = float(manifest["target"]["redshift"])
    target_rs = [float(x) for x in manifest["experiment"]["target_resolutions"]]
    half_window = float(manifest["experiment"]["hbeta_half_window_um"])

    spec = load_spec1d(Path(args.input))
    df, profiles = run_resolution_ladder(spec, z=z, target_rs=target_rs, half_window_um=half_window)
    df.to_csv(out / "resolution_ladder.csv", index=False)

    corr = spearmanr(df["target_R"], df["delta_bic"])
    full_delta = float(df.iloc[0]["delta_bic"])
    low_delta = float(df.iloc[-1]["delta_bic"])
    threshold_full = float(manifest["experiment"]["falsification"]["min_full_delta_bic"])
    threshold_drop = float(manifest["experiment"]["falsification"]["min_delta_bic_drop"])
    supported = bool(full_delta >= threshold_full and (full_delta - low_delta) >= threshold_drop and corr.statistic > 0)

    summary = {
        "status": "SUPPORTED_NECESSARY_CONDITION" if supported else "NOT_SUPPORTED_NECESSARY_CONDITION",
        "interpretation": (
            "This phase-0 test measures whether resolvable non-virial H-beta structure becomes less distinguishable "
            "under controlled spectral thinning. It does not reproduce the Naidu et al. Cloudy/COLT posterior and "
            "does not establish a true black-hole mass."
        ),
        "native_R": float(df.iloc[0]["native_R"]),
        "full_delta_bic": full_delta,
        "lowest_R_delta_bic": low_delta,
        "delta_bic_drop": full_delta - low_delta,
        "spearman_R_vs_delta_bic": float(corr.statistic),
        "spearman_pvalue": float(corr.pvalue),
        "falsification_thresholds": {
            "min_full_delta_bic": threshold_full,
            "min_delta_bic_drop": threshold_drop,
        },
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    plt.figure(figsize=(7, 4))
    plt.plot(df["target_R"], df["delta_bic"], marker="o")
    plt.axhline(0, linewidth=1)
    plt.xlabel("Target resolving power R")
    plt.ylabel("Delta BIC: virial-like minus structured")
    plt.title("MoM-BH*-1 H-beta model distinguishability")
    plt.xscale("log")
    plt.tight_layout()
    plt.savefig(out / "distinguishability_vs_resolution.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(df["target_R"], df["log10_mbh_virial_proxy"], marker="o")
    plt.xlabel("Target resolving power R")
    plt.ylabel("log10(MBH/Msun), virial scaling proxy")
    plt.title("Resolution dependence of naive virial mass proxy")
    plt.xscale("log")
    plt.tight_layout()
    plt.savefig(out / "virial_proxy_vs_resolution.png", dpi=180)
    plt.close()

    profile_df = pd.DataFrame(profiles)
    profile_df.to_csv(out / "thinned_hbeta_profiles.csv", index=False)

    prism_note = "not evaluated"
    prism_path = Path(args.prism)
    if prism_path.exists():
        try:
            prism = load_spec1d(prism_path)
            prism_df, _ = run_resolution_ladder(prism, z=z, target_rs=[], half_window_um=half_window)
            prism_df.to_csv(out / "published_prism_fit.csv", index=False)
            prism_note = "evaluated; see published_prism_fit.csv"
        except Exception as exc:
            prism_note = f"available but fit failed: {exc}"

    md = f"""# MoM-BH*-1 observer-thinning preflight

**Result:** `{summary['status']}`

- Native G395M resolving power in the H-beta window: {summary['native_R']:.1f}
- Delta BIC at native resolution: {full_delta:.2f}
- Delta BIC at lowest tested resolution: {low_delta:.2f}
- Delta BIC drop under thinning: {full_delta - low_delta:.2f}
- Spearman correlation, R vs Delta BIC: {corr.statistic:.3f} (p={corr.pvalue:.3g})
- Public prism comparison: {prism_note}

`Delta BIC > 0` favors the nested structured line model over the single broad-Gaussian virial-like model.

## Boundary of this result

This is a **necessary-condition preflight**, not the final dual-operator mass experiment.
The structured fit is a deliberately small empirical surrogate for resolvable absorption/scattering structure.
It does **not** reproduce the paper's Cloudy/COLT radiative-transfer inference and the virial mass column is only a literature-anchored `M ~ FWHM^2` proxy.

A negative result is scientifically valid: CI should remain green when the hypothesis is not supported.
"""
    (out / "summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
