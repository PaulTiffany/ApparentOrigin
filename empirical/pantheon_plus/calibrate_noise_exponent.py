"""Calibrate the AOC noise exponent 'p' from the Pantheon+ pipeline performance.

This script fits the model:
    sigma_mu = sigma_0 * (1 + z)^p
to the actual Pantheon+ distance-modulus uncertainty. This derives the 'p'
parameter from the instrument/pipeline performance rather than a toy model.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import csv

import numpy as np
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
CALIBRATION_PATH = DERIVED_DIR / "pantheon_noise_calibration.json"

def load_data():
    # Reuse loading logic or simplified version
    from analyze_pantheon_k import load_rows, load_covariance
    rows, _ = load_rows(RAW_PATH)
    cov = load_covariance(COV_PATH, len(rows))
    return rows, cov

def power_law(y, sigma_0, p):
    return sigma_0 * (y**p)

def main():
    print("Loading Pantheon+ data...")
    rows, cov = load_data()
    
    y = np.array([row.y for row in rows])
    # Use the covariance diagonal as the most robust uncertainty measure
    if cov is not None:
        sigma = np.sqrt(np.diag(cov))
        source = "covariance_diagonal"
    else:
        sigma = np.array([row.mu_err for row in rows])
        source = "table_mu_err"
    
    print(f"Fitting noise trend using {source}...")
    
    # Fit in log-log space for stability: log(sigma) = log(sigma_0) + p * log(y)
    log_y = np.log(y)
    log_sigma = np.log(sigma)
    
    # Linear fit to log-log
    p_fit, log_sigma_0_fit = np.polyfit(log_y, log_sigma, 1)
    sigma_0_fit = np.exp(log_sigma_0_fit)
    
    # Non-linear fit for refinement and error estimation
    popt, pcov = curve_fit(power_law, y, sigma, p0=[sigma_0_fit, p_fit])
    sigma_0_refined, p_refined = popt
    p_err = np.sqrt(pcov[1, 1])
    
    print(f"Derived Exponent p = {p_refined:.4f} +/- {p_err:.4f}")
    print(f"Base Uncertainty sigma_0 = {sigma_0_refined:.4f}")
    
    # Calculate binned averages for reporting
    z_bins = np.linspace(0, 2.5, 11)
    binned_stats = []
    for i in range(len(z_bins)-1):
        mask = (y - 1 >= z_bins[i]) & (y - 1 < z_bins[i+1])
        if np.any(mask):
            binned_stats.append({
                "z_mid": float((z_bins[i] + z_bins[i+1])/2),
                "y_avg": float(np.mean(y[mask])),
                "sigma_avg": float(np.mean(sigma[mask])),
                "n": int(np.sum(mask))
            })

    result = {
        "source": source,
        "n_rows": len(rows),
        "model": "sigma_mu = sigma_0 * (1+z)^p",
        "parameters": {
            "sigma_0": float(sigma_0_refined),
            "p": float(p_refined),
            "p_err": float(p_err)
        },
        "binned_trend": binned_stats,
        "interpretation": (
            f"The Pantheon+ pipeline demonstrates a noise growth exponent of p={p_refined:.2f}. "
            "This is the 'thickness' of the observer for this instrument. "
            "In AOC, this exponent determines the curvature of the reconstruction floor."
        )
    }
    
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with open(CALIBRATION_PATH, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Calibration results written to {CALIBRATION_PATH}")

if __name__ == "__main__":
    main()
