#!/usr/bin/env python3
"""Run the Phase-0 experiment with a bound-consistent structured-fit initializer.

The scientific model and bounds remain those in experiment.py. This wrapper only
ensures the initial absorption-center guess is chosen from the same +/-0.030 um
H-beta interval that the optimizer is allowed to explore.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import curve_fit

import experiment as base


def fit_models_bounded(
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

    p0_v = [cont, 0.0, amp0, center, sigma0]
    bounds_v = (
        [-np.inf, -np.inf, 0.0, center - 0.025, 0.002],
        [np.inf, np.inf, np.inf, center + 0.025, min(0.08, span / 2)],
    )
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
    allowed = np.abs(wave - center) <= 0.030
    if not allowed.any():
        raise RuntimeError("No samples inside the declared absorption-center bounds.")
    allowed_idx = np.flatnonzero(allowed)
    abs_idx = int(allowed_idx[np.nanargmax(residual[allowed])])
    abs_mu0 = float(wave[abs_idx])
    abs_amp0 = max(float(residual[abs_idx]), float(np.nanmedian(err)), 1e-6)

    p0_s = [*popt_v, abs_amp0, abs_mu0, 0.004]
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

    fwhm_um = 2.354820045 * abs(float(popt_v[4]))
    fwhm_kms = fwhm_um / float(popt_v[3]) * base.C_KMS
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


if __name__ == "__main__":
    base.fit_models = fit_models_bounded
    base.main()
