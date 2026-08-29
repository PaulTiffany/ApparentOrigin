"""Measure the Stitching Residue at the z=0.5 Saturation Boundary.

This script splits the Pantheon+ covariance into Local (z <= 0.5) and 
Extended (z > 0.5) blocks and calculates the discrepancy in inferred 
magnitude offsets. This measures the 'Internal Tension' of the pipeline.
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
STITCHING_PATH = DERIVED_DIR / "pantheon_stitching_residue.json"

# Reuse loading and chi2 logic
from analyze_pantheon_k import load_rows, load_covariance, distance_modulus_lcdm, FlatLambdaCDM, chi2_with_offset

def main():
    rows, _ = load_rows(RAW_PATH)
    n_total = len(rows)
    print(f"Loading covariance matrix ({n_total}x{n_total})...")
    cov = load_covariance(COV_PATH, n_total)
    
    if cov is None:
        return

    # 1. Define Atlas Blocks
    z_split = 0.5
    local_indices = [idx for idx, row in enumerate(rows) if row.mu is not None and row.z <= z_split]
    extended_indices = [idx for idx, row in enumerate(rows) if row.mu is not None and row.z > z_split]
    
    n_local = len(local_indices)
    n_extended = len(extended_indices)
    
    print(f"Split at z={z_split}: Local (n={n_local}), Extended (n={n_extended})")

    # 2. Calculate Local Residue (H0_local proxy)
    obs_local = np.array([rows[idx].mu for idx in local_indices], dtype=float)
    cov_local = cov[np.ix_(local_indices, local_indices)]
    theory_local = np.array([distance_modulus_lcdm(rows[idx].z, FlatLambdaCDM()) for idx in local_indices], dtype=float)
    
    chi2_local, offset_local = chi2_with_offset(obs_local - theory_local, cov_local)
    
    # 3. Calculate Extended Residue (H0_extended proxy)
    obs_ext = np.array([rows[idx].mu for idx in extended_indices], dtype=float)
    cov_ext = cov[np.ix_(extended_indices, extended_indices)]
    theory_ext = np.array([distance_modulus_lcdm(rows[idx].z, FlatLambdaCDM()) for idx in extended_indices], dtype=float)
    
    chi2_ext, offset_ext = chi2_with_offset(obs_ext - theory_ext, cov_ext)

    # 4. Calculate Combined Residue (The Stitching Cost)
    full_indices = local_indices + extended_indices
    obs_full = np.array([rows[idx].mu for idx in full_indices], dtype=float)
    cov_full = cov[np.ix_(full_indices, full_indices)]
    theory_full = np.array([distance_modulus_lcdm(rows[idx].z, FlatLambdaCDM()) for idx in full_indices], dtype=float)
    
    chi2_full, offset_full = chi2_with_offset(obs_full - theory_full, cov_full)

    # 5. Measure 'Stitching Cost' (Excess Chi2 from combining)
    stitching_cost = chi2_full - (chi2_local + chi2_ext)
    
    # 6. Calculate Parameter Shift (The Internal Tension)
    mag_shift = offset_local - offset_ext
    h0_shift_pct = (10**(mag_shift / 5.0) - 1.0) * 100
    
    print("-" * 40)
    print(f"Local Offset (mag):    {offset_local:8.4f}")
    print(f"Extended Offset (mag): {offset_ext:8.4f}")
    print(f"Internal mag shift:    {mag_shift:8.4f}")
    print(f"Predicted H0 Tension:  {h0_shift_pct:8.2f}%")
    print(f"Stitching Chi2 Cost:   {stitching_cost:8.2f}")
    print("-" * 40)

    results = {
        "z_split": z_split,
        "n_local": n_local,
        "n_extended": n_extended,
        "offset_local": offset_local,
        "offset_extended": offset_ext,
        "mag_shift": mag_shift,
        "h0_shift_percent": h0_shift_pct,
        "stitching_chi2_cost": stitching_cost,
        "interpretation": (
            f"The Pantheon+ pipeline exhibits an internal tension of {h0_shift_pct:.2f}% "
            f"at the z={z_split} boundary. The stitching cost (excess chi2) of {stitching_cost:.2f} "
            "represents the 'Residue' of trying to glue the saturated high-z atlas "
            "to the high-density local atlas. This internal mismatch is the seed of the global Hubble Tension."
        )
    }
    
    with open(STITCHING_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Stitching results written to {STITCHING_PATH}")

if __name__ == "__main__":
    main()
