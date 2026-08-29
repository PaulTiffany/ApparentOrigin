"""Refined Hubble Tension Triangle using Parameter-Level Capacity.

This script uses the actual H0 parameter precision (sigma_H0) from the 
published results of each probe to define Information-Geometric Capacity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# Constants (Reported H0 values)
H0_SN = 73.4
H0_BAO = 68.0
H0_CMB = 67.4

# Parameter-Level Capacities (Omega_H0)
# We define Capacity as the Precision (1 / sigma^2) of the parameter H0.
# This reflects the 'Stiffness' of the manifold in the H0 direction.

# 1. SNIa (SH0ES/Pantheon+)
# sigma_H0 ~ 1.0 km/s/Mpc (approx 1.4%)
SIGMA_H0_SN = 1.0
OMEGA_SN = 1.0 / (SIGMA_H0_SN**2)

# 2. BAO (DESI 2024 consensus)
# Typical BAO H0 precision is ~0.8-1.0 km/s/Mpc depending on priors.
# Let's use 0.9 as a representative value.
SIGMA_H0_BAO = 0.9
OMEGA_BAO = 1.0 / (SIGMA_H0_BAO**2)

# 3. CMB (Planck 2018)
# sigma_H0 ~ 0.5 km/s/Mpc (approx 0.7%)
SIGMA_H0_CMB = 0.5
OMEGA_CMB = 1.0 / (SIGMA_H0_CMB**2)

def predict_tension(omega_from, omega_to, h0_base, p=2.0):
    # Tension = H0 * (Omega_global / Omega_local)^(1/p)
    # Using p=2.0 (The Shannon Horizon / Rayleigh Scaling)
    ratio = omega_to / omega_from
    return h0_base * (ratio**(1/p) - 1.0)

def main():
    print("AOC Hubble Tension: Parameter-Level Precision Triangle")
    print("-" * 50)
    print(f"Capacity SN  (1/sigma^2): {OMEGA_SN:6.2f}")
    print(f"Capacity BAO (1/sigma^2): {OMEGA_BAO:6.2f}")
    print(f"Capacity CMB (1/sigma^2): {OMEGA_CMB:6.2f}")
    print("-" * 50)
    
    # Predictions
    # 1. SN to CMB
    # We bridge from high-precision global to local. 
    # The residue is the 'excess' found when trying to fit the global capacity into local.
    shift_sn_cmb = predict_tension(OMEGA_SN, OMEGA_CMB, H0_CMB)
    
    # 2. SN to BAO
    shift_sn_bao = predict_tension(OMEGA_SN, OMEGA_BAO, H0_BAO)
    
    # 3. BAO to CMB
    shift_bao_cmb = predict_tension(OMEGA_BAO, OMEGA_CMB, H0_CMB)
    
    print(f"SN -> CMB Predicted Tension:  {shift_sn_cmb:6.2f} km/s/Mpc (Obs: {H0_SN-H0_CMB:6.2f})")
    print(f"SN -> BAO Predicted Tension:  {shift_sn_bao:6.2f} km/s/Mpc (Obs: {H0_SN-H0_BAO:6.2f})")
    print(f"BAO -> CMB Predicted Tension: {shift_bao_cmb:6.2f} km/s/Mpc (Obs: {H0_BAO-H0_CMB:6.2f})")
    print("-" * 50)
    
    # Result: If Omega_CMB > Omega_SN, then Predicted > 0.
    # Accuracy checks
    acc_sn_cmb = 100 * (1 - abs(shift_sn_cmb - (H0_SN-H0_CMB))/(H0_SN-H0_CMB))
    
    print(f"Accuracy SN-CMB: {acc_sn_cmb:.1f}%")
    
    results = {
        "omega": {"sn": OMEGA_SN, "bao": OMEGA_BAO, "cmb": OMEGA_CMB},
        "predictions": {
            "sn_cmb": {"pred": shift_sn_cmb, "obs": H0_SN - H0_CMB},
            "sn_bao": {"pred": shift_sn_bao, "obs": H0_SN - H0_BAO},
            "bao_cmb": {"pred": shift_bao_cmb, "obs": H0_BAO - H0_CMB}
        }
    }
    
    out_path = Path("data/derived/pantheon_plus/hubble_triangle_precision.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
