"""Measure the Spectral Information Volume of the Pantheon+ pipeline.

This script calculates the Log-Determinant of the Precision Matrix (Information Volume)
across a redshift sweep. This provides a more rigorous grounding for Omega_O.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
SWEEP_PATH = DERIVED_DIR / "pantheon_spectral_info_sweep.csv"

# Reuse loading logic
from analyze_pantheon_k import load_rows, load_covariance

def main():
    rows, _ = load_rows(RAW_PATH)
    n_total = len(rows)
    print(f"Loading covariance matrix ({n_total}x{n_total})...")
    cov = load_covariance(COV_PATH, n_total)
    
    if cov is None:
        print("Error: Covariance matrix not found.")
        return

    # Redshift cutoffs for the sweep
    z_cuts = [0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.5]
    
    results = []
    
    print("Starting Spectral Volume Sweep...")
    for z_cut in z_cuts:
        # Identify subset
        subset_indices = [idx for idx, row in enumerate(rows) if row.z <= z_cut]
        n_sub = len(subset_indices)
        if n_sub < 2:
            continue
            
        # Extract sub-covariance
        subcov = cov[np.ix_(subset_indices, subset_indices)]
        
        # Calculate Spectral Information
        # Use eigenvalues for stability
        try:
            evals = np.linalg.eigvalsh(subcov)
            # Filter out near-zero eigenvalues that might be numerical noise
            evals = evals[evals > 1e-10]
            
            # 1. Log-Determinant (Entropy proxy): log(det(C)) = sum(log(lambda))
            # Precision Volume V = 1 / det(C) => log(V) = -sum(log(lambda))
            log_volume = -np.sum(np.log(evals))
            
            # 2. Effective Degrees of Freedom (n_eff)
            # Shannon-like count of independent resolution elements
            # Defined here as the number of eigenvalues above the median noise floor
            median_noise = np.median(evals)
            n_eff = np.sum(evals <= 2.0 * median_noise)
            
            # 3. Geometric Mean Uncertainty
            sigma_geom = np.exp(np.mean(np.log(np.sqrt(evals))))
            
            results.append({
                "z_cut": z_cut,
                "n_objects": n_sub,
                "n_eff_modes": int(n_eff),
                "log_info_volume": float(log_volume),
                "sigma_geom": float(sigma_geom)
            })
            print(f"  z < {z_cut:.2f}: n={n_sub}, n_eff={n_eff}, logV={log_volume:.2f}")
            
        except np.linalg.LinAlgError as e:
            print(f"  z < {z_cut:.2f}: SVD failure ({e})")
            continue

    # Write Results
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with open(SWEEP_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Spectral sweep written to {SWEEP_PATH}")

if __name__ == "__main__":
    main()
