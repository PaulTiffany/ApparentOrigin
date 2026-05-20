"""Refined Hubble Tension Mismatch Triangle using Linear Adaptedness Scaling.

This script applies the kappa_O ~ Omega_O scaling to the 3-probe triangle.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# Constants (Reported H0 values)
H0_SN = 73.4
H0_BAO = 68.0
H0_CMB = 67.4

# Pipeline Capacities (Omega_O)
# Formula: Omega_O = n_modes * a^2 / (relative_error)

# 1. SNIa (Pantheon+)
N_SN = 1550
A_SN = 1.0
SIGMA_SN = 0.08
OMEGA_SN = N_SN * (A_SN**2) / SIGMA_SN

# 2. BAO (DESI/eBOSS)
N_BAO = 15
A_BAO = 0.5 
SIGMA_BAO = 0.0052
OMEGA_BAO = N_BAO * (A_BAO**2) / SIGMA_BAO

# 3. CMB (Planck)
N_CMB = 6000000
A_CMB = 1.0 / 1100.0
SIGMA_CMB = 0.001
OMEGA_CMB = N_CMB * (A_CMB**2) / SIGMA_CMB

def predict_shift_linear(omega_from, omega_to, h0_base):
    # Refined Scaling: Delta H0 / H0 = Omega_global / Omega_local
    # Curvature (residue) is suppressed by the capacity of the local atlas.
    return h0_base * (omega_to / omega_from)

def main():
    print("AOC Hubble Tension: Linear Adaptedness Triangle")
    print("-" * 50)
    print(f"Capacity SN:  {OMEGA_SN:12.4e}")
    print(f"Capacity BAO: {OMEGA_BAO:12.4e}")
    print(f"Capacity CMB: {OMEGA_CMB:12.4e}")
    print("-" * 50)
    
    # Predictions
    # 1. SN to CMB (The Big Tension)
    shift_sn_cmb = predict_shift_linear(OMEGA_SN, OMEGA_CMB, H0_CMB)
    
    # 2. SN to BAO (The Local Tension)
    shift_sn_bao = predict_shift_linear(OMEGA_SN, OMEGA_BAO, H0_BAO)
    
    # 3. BAO to CMB (The Global Consistency)
    shift_bao_cmb = predict_shift_linear(OMEGA_BAO, OMEGA_CMB, H0_CMB)
    
    print(f"SN -> CMB Predicted Tension:  {shift_sn_cmb:6.2f} km/s/Mpc (Obs: {H0_SN-H0_CMB:6.2f})")
    print(f"SN -> BAO Predicted Tension:  {shift_sn_bao:6.2f} km/s/Mpc (Obs: {H0_SN-H0_BAO:6.2f})")
    print(f"BAO -> CMB Predicted Tension: {shift_bao_cmb:6.2f} km/s/Mpc (Obs: {H0_BAO-H0_CMB:6.2f})")
    print("-" * 50)
    
    accuracy_sn_cmb = 100 * (1 - abs(shift_sn_cmb - (H0_SN-H0_CMB))/(H0_SN-H0_CMB))
    accuracy_sn_bao = 100 * (1 - abs(shift_sn_bao - (H0_SN-H0_BAO))/(H0_SN-H0_BAO))
    accuracy_bao_cmb = 100 * (1 - abs(shift_bao_cmb - (H0_BAO-H0_CMB))/(H0_BAO-H0_CMB))
    
    print(f"Accuracy SN-CMB: {accuracy_sn_cmb:.1f}%")
    print(f"Accuracy SN-BAO: {accuracy_sn_bao:.1f}%")
    print(f"Accuracy BAO-CMB: {accuracy_bao_cmb:.1f}%")
    
    results = {
        "capacities": {"sn": OMEGA_SN, "bao": OMEGA_BAO, "cmb": OMEGA_CMB},
        "predictions": {
            "sn_cmb": {"predicted": shift_sn_cmb, "observed": H0_SN - H0_CMB},
            "sn_bao": {"predicted": shift_sn_bao, "observed": H0_SN - H0_BAO},
            "bao_cmb": {"predicted": shift_bao_cmb, "observed": H0_BAO - H0_CMB}
        }
    }
    
    out_path = Path("data/derived/pantheon_plus/hubble_triangle_linear.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
