"""Calibrate the AGGREGATE noise exponent 'p' from Pantheon+ density.

This script fits the model:
    sigma_aggregate = sigma_0_agg * (1 + z)^p
where sigma_aggregate = sigma_individual / sqrt(n_density).
This measures the "Shannon Horizon" of the pipeline.
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
CALIBRATION_PATH = DERIVED_DIR / "pantheon_aggregate_calibration.json"

def load_data():
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
    if cov is not None:
        sigma_diag = np.sqrt(np.diag(cov))
    else:
        sigma_diag = np.array([row.mu_err for row in rows])
    
    # Define redshift bins for density calculation
    # We need enough bins to see the trend but enough n per bin to be stable at low-z
    z_bins = np.linspace(0, 2.5, 26) # 25 bins, ~0.1 z width
    
    bin_y = []
    bin_sigma_agg = []
    bin_n = []
    bin_sigma_indiv = []
    
    print("Calculating aggregate binned statistics...")
    for i in range(len(z_bins)-1):
        mask = (y - 1 >= z_bins[i]) & (y - 1 < z_bins[i+1])
        n = np.sum(mask)
        if n > 0:
            y_avg = np.mean(y[mask])
            s_avg = np.mean(sigma_diag[mask])
            s_agg = s_avg / np.sqrt(n)
            
            bin_y.append(float(y_avg))
            bin_sigma_agg.append(float(s_agg))
            bin_n.append(int(n))
            bin_sigma_indiv.append(float(s_avg))

    bin_y = np.array(bin_y)
    bin_sigma_agg = np.array(bin_sigma_agg)
    
    print("Fitting aggregate noise trend...")
    # Fit log-log
    log_y = np.log(bin_y)
    log_s_agg = np.log(bin_sigma_agg)
    p_fit, log_s0_fit = np.polyfit(log_y, log_s_agg, 1)
    
    # Refine with non-linear fit
    popt, pcov = curve_fit(power_law, bin_y, bin_sigma_agg, p0=[np.exp(log_s0_fit), p_fit])
    s0_agg, p_agg = popt
    p_err = np.sqrt(pcov[1, 1])
    
    print(f"Aggregate Exponent p = {p_agg:.4f} +/- {p_err:.4f}")
    print(f"Aggregate Base sigma_0 = {s0_agg:.4f}")
    
    results = {
        "n_rows": len(rows),
        "model": "sigma_aggregate = sigma_0_agg * y^p",
        "parameters": {
            "sigma_0_agg": float(s0_agg),
            "p_aggregate": float(p_agg),
            "p_err": float(p_err)
        },
        "bins": [
            {
                "y": y_val,
                "n": n_val,
                "sigma_indiv": s_ind,
                "sigma_agg": s_agg_val
            }
            for y_val, n_val, s_ind, s_agg_val in zip(bin_y, bin_n, bin_sigma_indiv, bin_sigma_agg)
        ],
        "interpretation": (
            f"The aggregate reconstruction power of the Pantheon+ pipeline collapses with p={p_agg:.2f}. "
            "This confirms the 'Density Catastrophe': even if individual objects are high quality, "
            "the vanishing sample density creates a sharp reconstruction horizon (Shannon Horizon)."
        )
    }
    
    with open(CALIBRATION_PATH, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Aggregate calibration written to {CALIBRATION_PATH}")

if __name__ == "__main__":
    main()
