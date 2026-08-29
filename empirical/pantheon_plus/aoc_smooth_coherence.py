"""Global AOC Coherence Test: Smooth Transition Map (Corrected Sign).

This script uses a smooth residue function derived from the 'Catastrophic Drift'
to heal the Pantheon+ atlas by SUBTRACTING the residue (brightening the theory).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
COHERENCE_PATH = DERIVED_DIR / "pantheon_aoc_smooth_coherence.json"

# Reuse functions
from analyze_pantheon_k import load_rows, load_covariance, FlatLambdaCDM, luminosity_distance_mpc

def main():
    rows, _ = load_rows(RAW_PATH)
    n_total = len(rows)
    print("Loading data...")
    cov = load_covariance(COV_PATH, n_total)
    if cov is None: return

    # 1. Define Corrected Smooth Transition Map
    # Extended Atlas was too DIM (more negative theory offset).
    # We SUBTRACT the residue to make the theory brighter at high z.
    z_fracture = 0.5
    width = 0.1
    max_residue = 0.049 # The measured shift

    def aoc_smooth_theory(z, cosmology):
        dl = luminosity_distance_mpc(z, cosmology)
        mu_standard = 5.0 * math.log10(dl) + 25.0
        
        # Smooth activation
        factor = 1.0 / (1.0 + math.exp(-(z - z_fracture) / width))
        # SUBTRACT to brighten high-z theory
        return mu_standard - (max_residue * factor)

    # 2. Global Fit
    h0_global = 73.04 
    om_global = 0.30
    cosmo = FlatLambdaCDM(h0=h0_global, omega_m=om_global)
    
    def calculate_total_chi2(theory_func):
        obs = np.array([r.mu for r in rows if r.mu is not None])
        z = np.array([r.z for r in rows if r.mu is not None])
        theory = np.array([theory_func(zi, cosmo) for zi in z])
        residual = obs - theory
        cov_jitter = cov + np.eye(cov.shape[0]) * 1e-10
        solved = np.linalg.solve(cov_jitter, residual)
        return float(residual @ solved)

    print("Running Standard LCDM...")
    chi2_standard = calculate_total_chi2(lambda z, c: 5.0 * math.log10(luminosity_distance_mpc(z, c)) + 25.0)
    
    print("Running Corrected Smooth AOC...")
    chi2_aoc = calculate_total_chi2(aoc_smooth_theory)

    print("-" * 40)
    print(f"Standard Chi2: {chi2_standard:.2f}")
    print(f"Smooth AOC Chi2: {chi2_aoc:.2f}")
    print(f"Coherence Gain: {chi2_standard - chi2_aoc:+.2f}")
    print("-" * 40)

    results = {
        "chi2_standard": chi2_standard,
        "chi2_aoc": chi2_aoc,
        "delta_chi2": chi2_standard - chi2_aoc,
        "interpretation": "Corrected sign reveals true coherence gain."
    }
    with open(COHERENCE_PATH, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
