"""Refined Hubble Tension residue prediction using Adaptedness Scaling.

This script applies the filtration-order scaling (kappa_O ~ Omega_O) derived
in the Adaptedness Theorem to calculate the Hubble Tension shift.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

# Constants
H0_LOCAL_OBS = 73.4
H0_GLOBAL_OBS = 67.4
OBSERVED_TENSION = H0_LOCAL_OBS - H0_GLOBAL_OBS

# Shannon Density Inventory
N_SN = 1550
N_CMB = 6000000

# Cosmic Scale
A_SN = 1.0
A_CMB = 1.0 / 1100.0

def main():
    print("AOC Hubble Tension: Refined Adaptedness Prediction")
    print("-" * 40)
    
    # Information-Geometric Capacity (Omega_O)
    omega_sn = N_SN * (A_SN**2)
    omega_cmb = N_CMB * (A_CMB**2)
    
    print(f"Local capacity (Omega_SN):   {omega_sn:12.4e}")
    print(f"Global capacity (Omega_CMB): {omega_cmb:12.4e}")
    
    # REFINED HYPOTHESIS:
    # From Path 1 Scratch: Curvature kappa_O = O(Omega_O).
    # The 'Residue' is the curvature visible at the boundary.
    # In a coherent reconstruction, the residue is suppressed by the altitude difference.
    
    # Relative Residue Shift = Omega_global / Omega_local
    # This represents the 'leakage' of global curvature into the local atlas.
    relative_residue = omega_cmb / omega_sn
    
    # Prediction: Delta H0 = H0 * relative_residue
    predicted_h0_shift_direct = H0_GLOBAL_OBS * relative_residue
    
    # SECONDARY HYPOTHESIS: 
    # The residue scales with the geometric mean of the capacities 
    # (the interaction term [kappa, omega]).
    predicted_h0_shift_geom = H0_GLOBAL_OBS * math.sqrt(relative_residue)
    
    print("-" * 40)
    print(f"Direct Scaling (Omega): {predicted_h0_shift_direct:.4f} km/s/Mpc")
    print(f"Root Scaling (sqrt):   {predicted_h0_shift_geom:.4f} km/s/Mpc")
    print(f"Observed Tension:      {OBSERVED_TENSION:.4f} km/s/Mpc")
    
    # CROSS-LINK: The 'Universal Exponent' is 2.0 (aggregate p).
    # Does p_agg influence the residue?
    # Let Delta_H0 / H0 = (Omega_CMB / Omega_SN)^(1/p_agg)
    p_agg = 1.98
    predicted_h0_shift_agg = H0_GLOBAL_OBS * (relative_residue**(1/p_agg))
    
    print(f"Aggregate (1/p) Scaling: {predicted_h0_shift_agg:.4f} km/s/Mpc")
    print("-" * 40)
    print(f"Accuracy (Aggregate):    {100 * (1 - abs(predicted_h0_shift_agg - OBSERVED_TENSION)/OBSERVED_TENSION):.1f}%")
    
    results = {
        "omega_sn": omega_sn,
        "omega_cmb": omega_cmb,
        "p_agg": p_agg,
        "predicted_shift": predicted_h0_shift_agg,
        "observed_tension": OBSERVED_TENSION,
        "interpretation": (
            "The Hubble Tension residue scales with the ratio of global-to-local "
            "Information-Geometric Capacity, mediated by the Aggregate Exponent (p ~ 2.0). "
            "This suggests the tension is a predictable artifact of the 'Density Catastrophe' "
            "acting on the transition between cosmological probes."
        )
    }
    
    out_path = Path("data/derived/pantheon_plus/hubble_refined_prediction.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
