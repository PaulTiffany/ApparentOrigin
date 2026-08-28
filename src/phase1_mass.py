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
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

import experiment as base


SQRT2PI = math.sqrt(2.0 * math.pi)


def fit_dual(wave: np.ndarray, flux: np.ndarray, err: np.ndarray, center: float) -> dict[str, float]:
    finite = np.isfinite(wave) & np.isfinite(flux) & np.isfinite(err) & (err > 0)
    wave = np.asarray(wave[finite], dtype=float)
    flux = np.asarray(flux[finite], dtype=float)
    err = np.asarray(err[finite], dtype=float)
    if wave.size < 25:
        raise RuntimeError("Not enough valid samples in H-beta window.")

    edge = max(3, wave.size // 8)
    cont = float(np.nanmedian(np.r_[flux[:edge], flux[-edge:]]))
    amp0 = max(float(np.nanmax(flux) - cont), float(np.nanstd(flux)), 1e-9)
    sigma0 = 0.018
    span = float(wave.max() - wave.min())

    bounds_v = (
        [-np.inf, -np.inf, 0.0, center - 0.025, 0.002],
        [np.inf, np.inf, np.inf, center + 0.025, min(0.08, span / 2)],
    )
    p0_v = base.strictly_feasible([cont, 0.0, amp0, center, sigma0], bounds_v)
    popt_v, _ = curve_fit(
        base.virial_like,
        wave,
        flux,
        p0=p0_v,
        sigma=err,
        absolute_sigma=True,
        bounds=bounds_v,
        maxfev=50000,
    )
    pred_v = base.virial_like(wave, *popt_v)
    bic_v, chi2_v = base.bic(flux, pred_v, err, len(popt_v))

    residual = pred_v - flux
    absorption_region = np.abs(wave - center) <= 0.030
    if not absorption_region.any():
        raise RuntimeError("No samples inside the predeclared H-beta absorption region.")
    candidate_indices = np.flatnonzero(absorption_region)
    abs_idx = int(candidate_indices[np.nanargmax(residual[absorption_region])])
    abs_mu0 = float(wave[abs_idx])
    abs_amp0 = max(float(residual[abs_idx]), float(np.nanmedian(err)), 1e-9)

    bounds_s = (
        [-np.inf, -np.inf, 0.0, center - 0.025, 0.002, 0.0, center - 0.030, 0.0005],
        [np.inf, np.inf, np.inf, center + 0.025, min(0.08, span / 2), np.inf, center + 0.030, 0.020],
    )
    p0_s = base.strictly_feasible([*popt_v, abs_amp0, abs_mu0, 0.004], bounds_s)
    popt_s, _ = curve_fit(
        base.structured,
        wave,
        flux,
        p0=p0_s,
        sigma=err,
        absolute_sigma=True,
        bounds=bounds_s,
        maxfev=80000,
    )
    pred_s = base.structured(wave, *popt_s)
    bic_s, chi2_s = base.bic(flux, pred_s, err, len(popt_s))

    def emission_stats(popt: np.ndarray) -> tuple[float, float, float]:
        amp = float(popt[2])
        mu = float(popt[3])
        sigma = abs(float(popt[4]))
        line_flux_coord = max(amp * sigma * SQRT2PI, 1e-300)
        fwhm_kms = (2.354820045 * sigma / mu) * base.C_KMS
        q = 0.59 * math.log10(line_flux_coord) + 2.0 * math.log10(max(fwhm_kms, 1e-300))
        return line_flux_coord, fwhm_kms, q

    v_flux, v_fwhm, v_q = emission_stats(popt_v)
    s_flux, s_fwhm, s_q = emission_stats(popt_s)

    return {
        "bic_virial_like": bic_v,
        "bic_structured": bic_s,
        "delta_bic": bic_v - bic_s,
        "chi2_virial_like": chi2_v,
        "chi2_structured": chi2_s,
        "virial_line_flux_coord": v_flux,
        "virial_fwhm_kms": v_fwhm,
        "virial_q": v_q,
        "structured_line_flux_coord": s_flux,
        "structured_fwhm_kms": s_fwhm,
        "structured_q": s_q,
        "absorption_depth_fit": float(popt_s[5]),
        "absorption_center_um": float(popt_s[6]),
        "absorption_sigma_um": float(popt_s[7]),
    }


def local_arrays(spec: dict[str, np.ndarray], z: float, half_window_um: float):
    center = base.HBETA_REST_UM * (1.0 + z)
    mask = (
        spec["valid"]
        & np.isfinite(spec["wave"])
        & np.isfinite(spec["flux"])
        & (np.abs(spec["wave"] - center) <= half_window_um)
    )
    wave = np.asarray(spec["wave"][mask], dtype=float)
    flux = np.asarray(spec["flux"][mask], dtype=float)
    err = np.asarray(spec["err"][mask], dtype=float)
    rr = np.asarray(spec["R"][mask], dtype=float)
    order = np.argsort(wave)
    wave, flux, err, rr = wave[order], flux[order], err[order], rr[order]
    if wave.size < 25:
        raise RuntimeError("Insufficient H-beta samples after selection.")
    uniform_wave = np.linspace(float(wave.min()), float(wave.max()), wave.size)
    uniform_flux = np.interp(uniform_wave, wave, flux)
    good = np.isfinite(err) & (err > 0)
    fallback = float(np.nanmedian(err[good])) if good.any() else 1.0
    uniform_err = np.interp(uniform_wave, wave, np.where(good, err, fallback))
    native_values = rr[np.isfinite(rr) & (rr > 0)]
    native_r = float(np.nanmedian(native_values)) if native_values.size else 1000.0
    return center, uniform_wave, uniform_flux, uniform_err, native_r


def absorption_mask(wave: np.ndarray, center: float, centers_kms=(0.0, -1500.0, 1500.0), halfwidth_kms=500.0):
    velocity = (wave / center - 1.0) * base.C_KMS
    keep = np.ones(wave.size, dtype=bool)
    for vc in centers_kms:
        keep &= np.abs(velocity - vc) > halfwidth_kms
    return keep


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="run/raw/excels_g395m.fits")
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run/phase1")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    z = float(manifest["target"]["redshift"])
    exp = manifest["experiment"]
    p1 = manifest["phase1"]
    half_window = float(exp["hbeta_half_window_um"])
    target_rs = [float(x) for x in exp["target_resolutions"]]

    spec = base.load_spec1d(Path(args.input))
    center, wave, flux, err, native_r = local_arrays(spec, z, half_window)
    ladder = [native_r] + [r for r in target_rs if r < native_r * 0.98]

    rows: list[dict[str, float | str]] = []
    for r in ladder:
        dflux, derr = base.gaussian_degrade(
            wave, flux, err, native_r=native_r, target_r=float(r), center_um=center
        )
        fit = fit_dual(wave, dflux, derr, center)
        fit.update({"intervention": "resolution", "target_R": float(r), "native_R": native_r})
        rows.append(fit)

    resolution_df = pd.DataFrame(rows).sort_values("target_R", ascending=False).reset_index(drop=True)
    q_ref = float(resolution_df.iloc[0]["structured_q"])
    resolution_df["rho_M_virial_dex"] = resolution_df["virial_q"] - q_ref
    resolution_df["rho_M_structured_dex"] = resolution_df["structured_q"] - q_ref

    mask = absorption_mask(
        wave,
        center,
        centers_kms=tuple(float(x) for x in p1["mask_control"]["centers_kms"]),
        halfwidth_kms=float(p1["mask_control"]["halfwidth_kms"]),
    )
    masked_fit = fit_dual(wave[mask], flux[mask], err[mask], center)
    masked = {
        **masked_fit,
        "intervention": "mask_absorption_triplet",
        "target_R": native_r,
        "native_R": native_r,
        "retained_fraction": float(mask.mean()),
        "rho_M_virial_dex": float(masked_fit["virial_q"] - q_ref),
        "rho_M_structured_dex": float(masked_fit["structured_q"] - q_ref),
    }

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    resolution_df.to_csv(out / "mass_residue_resolution.csv", index=False)
    pd.DataFrame([masked]).to_csv(out / "mass_residue_mask_control.csv", index=False)

    corr = spearmanr(resolution_df["target_R"], resolution_df["delta_bic"])
    native_rho = float(resolution_df.iloc[0]["rho_M_virial_dex"])
    low_rho = float(resolution_df.iloc[-1]["rho_M_virial_dex"])
    residue_increase = low_rho - native_rho
    min_low = float(p1["falsification"]["min_low_r_virial_residue_dex"])
    min_increase = float(p1["falsification"]["min_virial_residue_increase_dex"])
    phase0_collapse = bool(
        float(resolution_df.iloc[0]["delta_bic"]) >= float(exp["falsification"]["min_full_delta_bic"])
        and float(resolution_df.iloc[0]["delta_bic"] - resolution_df.iloc[-1]["delta_bic"])
        >= float(exp["falsification"]["min_delta_bic_drop"])
        and float(corr.statistic) > 0
    )
    supported = bool(phase0_collapse and low_rho >= min_low and residue_increase >= min_increase)

    summary = {
        "status": "SUPPORTED_DIRECTIONAL_MASS_RESIDUE" if supported else "NOT_SUPPORTED_DIRECTIONAL_MASS_RESIDUE",
        "reference": "full-access structured surrogate at native G395M resolution; not ground truth",
        "native_R": native_r,
        "native_virial_rho_M_dex": native_rho,
        "lowest_R": float(resolution_df.iloc[-1]["target_R"]),
        "lowest_R_virial_rho_M_dex": low_rho,
        "virial_residue_increase_dex": residue_increase,
        "native_delta_bic": float(resolution_df.iloc[0]["delta_bic"]),
        "lowest_R_delta_bic": float(resolution_df.iloc[-1]["delta_bic"]),
        "spearman_R_vs_delta_bic": float(corr.statistic),
        "mask_control_virial_rho_M_dex": float(masked["rho_M_virial_dex"]),
        "mask_control_retained_fraction": float(masked["retained_fraction"]),
        "thresholds": {
            "min_low_r_virial_residue_dex": min_low,
            "min_virial_residue_increase_dex": min_increase,
        },
        "boundary": "Relative virial mass-coordinate test only; no Cloudy/COLT posterior and no absolute BH mass claim.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    plt.figure(figsize=(7, 4))
    plt.plot(resolution_df["delta_bic"], resolution_df["rho_M_virial_dex"], marker="o", label="virial-like")
    plt.plot(resolution_df["delta_bic"], resolution_df["rho_M_structured_dex"], marker="o", label="absorption-aware")
    plt.axhline(0.0, linewidth=1)
    plt.xlabel("Delta BIC: virial-like minus structured")
    plt.ylabel("Relative virial mass coordinate rho_M [dex]")
    plt.title("MoM-BH*-1: reconstruction residue vs distinguishability")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "mass_residue_vs_distinguishability.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(resolution_df["target_R"], resolution_df["rho_M_virial_dex"], marker="o", label="virial-like")
    plt.plot(resolution_df["target_R"], resolution_df["rho_M_structured_dex"], marker="o", label="absorption-aware")
    plt.axhline(0.0, linewidth=1)
    plt.xscale("log")
    plt.xlabel("Target resolving power R")
    plt.ylabel("Relative virial mass coordinate rho_M [dex]")
    plt.title("MoM-BH*-1: mass reconstruction under controlled thinning")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "mass_residue_vs_resolution.png", dpi=180)
    plt.close()

    md = f"""# Phase 1A: directional mass-residue test

**Result:** `{summary['status']}`

Reference: full-access absorption-aware structured surrogate at native G395M resolution (**not ground truth**).

- Native R: {native_r:.1f}
- Native virial-like mass residue: {native_rho:+.3f} dex
- Lowest tested R: {summary['lowest_R']:.1f}
- Lowest-R virial-like mass residue: {low_rho:+.3f} dex
- Virial-like residue change, native -> lowest R: {residue_increase:+.3f} dex
- Native Delta BIC: {summary['native_delta_bic']:.2f}
- Lowest-R Delta BIC: {summary['lowest_R_delta_bic']:.2f}
- Native-resolution absorption-mask control: {summary['mask_control_virial_rho_M_dex']:+.3f} dex (retained {100*summary['mask_control_retained_fraction']:.1f}% of samples)

Predeclared directional thresholds:

- lowest-R virial-like residue >= {min_low:+.2f} dex
- native-to-lowest-R virial-like residue increase >= {min_increase:+.2f} dex

The mass coordinate uses the relative Greene-Ho-style scaling `M ~ L_Hbeta^0.59 FWHM^2`. Because this is one source at one distance, the absolute luminosity normalization cancels. This test does not reproduce Cloudy/COLT and does not estimate a ground-truth black-hole mass.
"""
    (out / "summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
