"""Residue Evolution Map: Tracking the Fracture Gradient.

This script performs a rolling split of the Pantheon+ dataset to map how the 
inferred cosmology (H0, Om) 'drifts' as the observer transitions from 
high-density to saturated regimes.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
REPORT_DIR = ROOT / "reports" / "pantheon_plus"
EVOLUTION_PATH = DERIVED_DIR / "pantheon_residue_evolution.csv"
PLOT_PATH = REPORT_DIR / "pantheon_residue_evolution.png"

# Reuse loading and interpolation logic
from analyze_pantheon_k import load_rows, load_covariance, e_z

def precompute_dl_grid(z_max=2.5):
    om_vals = np.linspace(0.1, 0.6, 30)
    z_vals = np.linspace(0, z_max, 100)
    grid = np.zeros((len(om_vals), len(z_vals)))
    c_km_s = 299_792.458
    for i, om in enumerate(om_vals):
        for j, z in enumerate(z_vals):
            if z == 0: continue
            zs = np.linspace(0, z, 200)
            inv_e = 1.0 / np.sqrt(om * (1+zs)**3 + (1-om))
            # Use trapezoid for more accuracy
            comoving = (c_km_s / 1.0) * np.trapz(inv_e, zs) 
            grid[i, j] = (1+z) * comoving
    return RegularGridInterpolator((om_vals, z_vals), grid, bounds_error=False, fill_value=None)

def main():
    rows, _ = load_rows(RAW_PATH)
    n_total = len(rows)
    print("Loading data and precomputing distance atlas...")
    cov = load_covariance(COV_PATH, n_total)
    if cov is None: return
    diag_sigma = np.sqrt(np.diag(cov))
    dl_interp = precompute_dl_grid()

    # Define rolling boundaries
    z_splits = np.linspace(0.2, 1.0, 17) # Increments of 0.05
    
    # Fit ranges
    om_range = np.linspace(0.15, 0.50, 40)
    h0_range = np.linspace(65, 80, 40)

    results = []

    def get_best_fit(indices):
        if not indices: return None, None
        z_arr = np.array([rows[idx].z for idx in indices])
        obs_arr = np.array([rows[idx].mu for idx in indices])
        sig_arr = diag_sigma[indices]
        
        best_chi2 = float('inf')
        best_p = (0, 0)
        
        # Grid search using precomputed interpolator
        for om in om_range:
            dl_pre = dl_interp(np.column_stack([np.full_like(z_arr, om), z_arr]))
            for h0 in h0_range:
                theory = 5.0 * np.log10(dl_pre / h0) + 25.0
                c2 = np.sum(((obs_arr - theory) / sig_arr)**2)
                if c2 < best_chi2:
                    best_chi2 = c2
                    best_p = (om, h0)
        return best_p, best_chi2

    print("Mapping Residue Evolution...")
    for z_split in z_splits:
        local_idx = [idx for idx, row in enumerate(rows) if row.mu is not None and row.z <= z_split]
        ext_idx = [idx for idx, row in enumerate(rows) if row.mu is not None and row.z > z_split]
        
        if len(local_idx) < 10 or len(ext_idx) < 10: continue
        
        (om_l, h0_l), chi2_l = get_best_fit(local_idx)
        (om_e, h0_e), chi2_e = get_best_fit(ext_idx)
        
        results.append({
            "z_split": float(z_split),
            "n_local": len(local_idx),
            "n_extended": len(ext_idx),
            "h0_local": float(h0_l),
            "om_local": float(om_l),
            "h0_ext": float(h0_e),
            "om_ext": float(om_e),
            "delta_h0": float(h0_l - h0_e),
            "delta_om": float(om_l - om_e)
        })
        print(f"  z_split={z_split:.2f} => dH0={h0_l-h0_e:+.2f}, dOm={om_l-om_e:+.3f}")

    # Save results
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with open(EVOLUTION_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # Plotting (Residue Evolution)
    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=160)
        
        z = [r["z_split"] for r in results]
        h0_l = [r["h0_local"] for r in results]
        h0_e = [r["h0_ext"] for r in results]
        om_l = [r["om_local"] for r in results]
        om_e = [r["om_ext"] for r in results]
        
        axes[0].plot(z, h0_l, label="Local Atlas (z <= z_split)", marker='o', color="#1d7f8c")
        axes[0].plot(z, h0_e, label="Extended Atlas (z > z_split)", marker='s', color="#9c4638")
        axes[0].set_xlabel("Split Boundary z_split")
        axes[0].set_ylabel("Best-fit H0")
        axes[0].set_title("H0 Evolution across Atlas Fracture")
        axes[0].legend()
        axes[0].grid(True, alpha=0.2)
        
        axes[1].plot(z, om_l, marker='o', color="#1d7f8c")
        axes[1].plot(z, om_e, marker='s', color="#9c4638")
        axes[1].set_xlabel("Split Boundary z_split")
        axes[1].set_ylabel("Best-fit Omega_m")
        axes[1].set_title("Omega_m Evolution across Atlas Fracture")
        axes[1].grid(True, alpha=0.2)
        
        fig.tight_layout()
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(PLOT_PATH)
        print(f"Wrote plot to {PLOT_PATH}")
    except ImportError:
        pass

    print(f"Evolution map written to {EVOLUTION_PATH}")

if __name__ == "__main__":
    main()
