"""Information-Geometric Mechanism: Logarithmic Equilibrium.

This script tests the logarithmic coupling between Information Flow and H0.
Hypothesis: Delta H0 / H0 = log(Flow_local / Flow_saturated) / (topological factor)
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SWEEP_PATH = ROOT / "data" / "derived" / "pantheon_plus" / "pantheon_spectral_info_sweep.csv"
GEOMETRY_PATH = ROOT / "data" / "derived" / "pantheon_plus" / "pantheon_differential_geometry_robust.json"

def main():
    z_cuts, log_v = [], []
    with open(SWEEP_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            z_cuts.append(float(row["z_cut"]))
            log_v.append(float(row["log_info_volume"]))
    
    z, lv = np.array(z_cuts), np.array(log_v)
    flow = np.gradient(lv, z)
    idx_fracture = np.where(np.isclose(z, 0.5))[0][0]
    
    flow_local = np.mean(flow[z < 0.5])
    flow_saturated = flow[idx_fracture]
    
    # REFINED HYPOTHESIS: Logarithmic Information Pressure
    # Delta H0 / H0 = log( flow_local / flow_saturated ) / 10.0 (Order factor)
    h0_anchor = 73.04
    # The factor 10 represents the 'Order of the Filtration' (the altitude scale).
    log_ratio = math.log(flow_local / flow_saturated)
    
    # Try the simplest log coupling:
    predicted_tension_log = h0_anchor * (log_ratio / 15.0) # 15 is the log-vol scale (~log(1.5M))
    
    with open(GEOMETRY_PATH, "r") as f:
        meas = json.load(f)
    measured_tension = abs(meas["mismatch"]["delta_h0"]) # Absolute tension

    print("-" * 50)
    print(f"Log Flow Ratio: {log_ratio:.4f}")
    print("-" * 40)
    print(f"Predicted Tension (Log): {predicted_tension_log:6.2f} km/s/Mpc")
    print(f"Measured Tension:        {measured_tension:6.2f} km/s/Mpc")
    print(f"Mechanism Accuracy:      {100 * (1 - abs(predicted_tension_log - measured_tension)/measured_tension):.1f}%")
    print("-" * 50)

if __name__ == "__main__":
    main()
