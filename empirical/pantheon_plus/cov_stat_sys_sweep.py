"""Stat/Sys Covariance Decomposition Sweep for AOC v0 + v1.

This script tests the sensitivity of the Pantheon+ AOC signal to differential
rescaling of statistical and systematic uncertainties.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_SYS_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
COV_STAT_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STATONLY.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
REPORT_DIR = ROOT / "reports" / "pantheon_plus"
SWEEP_PATH = DERIVED_DIR / "pantheon_cov_stat_sys_sweep.csv"
SUMMARY_PATH = DERIVED_DIR / "pantheon_cov_stat_sys_summary.json"
PLOT_PATH = REPORT_DIR / "pantheon_cov_stat_sys_sweep.png"

# Reuse functions from analyze_pantheon_k.py
from analyze_pantheon_k import load_rows, load_covariance, aoc_threshold_grid_chi2

def main():
    rows, _ = load_rows(RAW_PATH)
    n = len(rows)
    print(f"Loading covariances for {n} rows...")
    c_total = load_covariance(COV_SYS_PATH, n)
    c_stat = load_covariance(COV_STAT_PATH, n)
    c_sys = c_total - c_stat # C_sys = C_total - C_stat
    
    # Grid of scales for stat and sys
    # s_total = s_stat * C_stat + s_sys * C_sys
    scales = [0.8, 1.0, 1.2, 1.5]
    
    lambdas = np.round(np.arange(-0.30, 0.301, 0.01), 6)
    z_cut = 1.0
    subset = [idx for idx, row in enumerate(rows) if row.mu is not None and row.z <= z_cut]
    
    results = []
    
    print("Running stat/sys sweep...")
    for s_stat in scales:
        for s_sys in scales:
            # Reconstruct covariance
            c_mod = s_stat * c_stat + s_sys * c_sys
            
            # Evaluate v0 (log deformation)
            # aoc_threshold_grid_chi2 uses z_star=0.8 and log(1+z/z_star)
            lcdm_chi2, lcdm_offset, evaluations = aoc_threshold_grid_chi2(rows, c_mod, subset, lambdas)
            best_lam, best_chi2, best_offset = min(evaluations, key=lambda x: x[1])
            
            delta_chi2 = best_chi2 - lcdm_chi2
            delta_bic = delta_chi2 + math.log(len(subset))
            
            results.append({
                "s_stat": s_stat,
                "s_sys": s_sys,
                "best_lambda": best_lam,
                "delta_chi2": delta_chi2,
                "delta_bic": delta_bic,
                "n": len(subset)
            })
            print(f"  s_stat={s_stat:.1f}, s_sys={s_sys:.1f} => dBIC={delta_bic:.2f}")

    # Write results
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with SWEEP_PATH.open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    
    summary = {
        "z_cut": z_cut,
        "n_subset": len(subset),
        "results": results
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {SWEEP_PATH}")

    # Plotting
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 6), dpi=160)
        
        # Create a heatmap-like visualization
        s_vals = sorted(list(set(scales)))
        data_matrix = np.zeros((len(s_vals), len(s_vals)))
        for r in results:
            i = s_vals.index(r["s_stat"])
            j = s_vals.index(r["s_sys"])
            data_matrix[i, j] = r["delta_bic"]
            
        im = ax.imshow(data_matrix, origin='lower', cmap='viridis_r')
        ax.set_xticks(np.arange(len(s_vals)))
        ax.set_yticks(np.arange(len(s_vals)))
        ax.set_xticklabels([f"{s:.1f}" for s in s_vals])
        ax.set_yticklabels([f"{s:.1f}" for s in s_vals])
        ax.set_xlabel("Systematic Scaling $s_{sys}$")
        ax.set_ylabel("Statistical Scaling $s_{stat}$")
        ax.set_title(f"AOC v0 Delta BIC Sensitivity (z_cut={z_cut})")
        
        # Add text annotations
        for i in range(len(s_vals)):
            for j in range(len(s_vals)):
                ax.text(j, i, f"{data_matrix[i, j]:.1f}", ha="center", va="center", color="w" if data_matrix[i, j] < -5 else "black")
        
        fig.colorbar(im, label="Delta BIC")
        fig.tight_layout()
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(PLOT_PATH)
        print(f"Wrote {PLOT_PATH}")
    except ImportError:
        pass

if __name__ == "__main__":
    main()
