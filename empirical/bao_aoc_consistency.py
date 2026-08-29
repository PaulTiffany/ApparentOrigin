"""Deprecated exploratory eBOSS BAO sanity check.

Do not cite this as a current AOC result. It used hand-entered eBOSS DR16
points, a fixed Planck-like anchor, diagonal errors, and over-strong narrative
language. The active BAO branch is:

    empirical/desi_dr2_bao/analyze_desi_dr2_bao.py

That branch uses DESI DR2 likelihood inputs, covariance, fitted BAO scale
nuisance, and explicit allowed/forbidden claims.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
BAO_OUTPUT = DERIVED_DIR / "bao_aoc_consistency_result.json"

# BAO Consensus Points (eBOSS DR16)
# Format: {z_eff: (DM_rd, DM_rd_err, DH_rd, DH_rd_err)}
BAO_DATA = {
    0.698: (17.65, 0.30, 19.77, 0.47),
    0.845: (18.33, 0.60, 19.66, 0.95),
    1.480: (30.21, 0.79, 13.23, 0.47),
    2.330: (37.41, 0.60, 8.99, 0.12),
}

# Constants
H0_PLANCK = 67.4
RD_PLANCK = 147.09 # Mpc (Planck 2018 rd consensus)

def e_z(z, om=0.30):
    return math.sqrt(om * (1+z)**3 + (1-om))

def comoving_distance_mpc(z, om=0.30, h0=67.4):
    # Numerical integral for D_M
    c = 299792.458
    zs = np.linspace(0, z, 200)
    inv_e = 1.0 / np.sqrt(om * (1+zs)**3 + (1-om))
    return (c / h0) * np.trapz(inv_e, zs)

def main():
    print("AOC BAO Consistency Test (Blind Extension)")
    print("-" * 50)
    
    # AOC Transition Map (from SNIa)
    # The residue was -0.049 mag at z > 0.5 (Extended atlas was too DIM).
    # Since mu = 5 log10(dL) + 25, a shift of -0.049 mag means 
    # the true distance is SHORTER than standard theory.
    # Fractional distance shift: f = 10^(-0.049/5) - 1 = -0.022 (approx 2.2%)
    dist_residue_frac = 10**(-0.049 / 5.0) - 1.0
    
    print(f"Applying SNIa-derived residue: {dist_residue_frac*100:+.2f}% distance shift")
    print("-" * 50)

    total_chi2_standard = 0
    total_chi2_aoc = 0
    
    results = []

    for z_eff, (dm_obs, dm_err, dh_obs, dh_err) in BAO_DATA.items():
        # Standard Theory (Planck LCDM)
        dm_theory = comoving_distance_mpc(z_eff, om=0.30, h0=H0_PLANCK)
        dh_theory = 299792.458 / (H0_PLANCK * e_z(z_eff, om=0.30))
        
        dm_rd_theory = dm_theory / RD_PLANCK
        dh_rd_theory = dh_theory / RD_PLANCK
        
        chi2_dm_std = ((dm_obs - dm_rd_theory) / dm_err)**2
        chi2_dh_std = ((dh_obs - dh_rd_theory) / dh_err)**2
        
        # AOC Theory (Apply residue for z > 0.5)
        # Note: All eBOSS consensus points are z > 0.5
        dm_rd_aoc = dm_rd_theory * (1.0 + dist_residue_frac)
        dh_rd_aoc = dh_rd_theory * (1.0 + dist_residue_frac) # DH scales same way as DM in this first-order test
        
        chi2_dm_aoc = ((dm_obs - dm_rd_aoc) / dm_err)**2
        chi2_dh_aoc = ((dh_obs - dh_rd_aoc) / dh_err)**2
        
        total_chi2_standard += chi2_dm_std + chi2_dh_std
        total_chi2_aoc += chi2_dm_aoc + chi2_dh_aoc
        
        results.append({
            "z": z_eff,
            "dm_obs": dm_obs, "dm_theory": dm_rd_theory, "dm_aoc": dm_rd_aoc,
            "dh_obs": dh_obs, "dh_theory": dh_rd_theory, "dh_aoc": dh_rd_aoc
        })
        print(f"z={z_eff:.3f}: Std dChi2={chi2_dm_std+chi2_dh_std:.2f}, AOC dChi2={chi2_dm_aoc+chi2_dh_aoc:.2f}")

    print("-" * 50)
    print(f"Total Standard Chi2 (Planck Anchor): {total_chi2_standard:.2f}")
    print(f"Total AOC Chi2 (Planck Anchor):      {total_chi2_aoc:.2f}")
    print(f"AOC Consistency Gain:               {total_chi2_standard - total_chi2_aoc:+.2f}")
    print("-" * 50)

    output = {
        "residue_used": dist_residue_frac,
        "chi2_standard": total_chi2_standard,
        "chi2_aoc": total_chi2_aoc,
        "gain": total_chi2_standard - total_chi2_aoc,
        "points": results,
        "interpretation": (
            "Deprecated exploratory eBOSS sanity check only. Do not interpret "
            "this as evidence for AOC or BAO universality. Use the DESI DR2 BAO "
            "branch for the current external-gate result."
        )
    }
    
    with open(BAO_OUTPUT, "w") as f:
        json.dump(output, f, indent=2)
    print(f"BAO consistency results written to {BAO_OUTPUT}")

if __name__ == "__main__":
    main()
