"""Phase Q0: deliberately limited SI-unit self-gravity and heat-load calculator.

This is a conditional parameter calculator, not a technological growth or
confinement model. Reuses the natural compact-object ladder's constants.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from compact_object_ladder import (
    C, G, HBAR, bekenstein_bound_bits, black_hole_entropy_bits_same_mass,
    compactness, schwarzschild_radius_m,
)

SIGMA_SB = 5.670374419e-8  # W m^-2 K^-4
FOUR_PI = 4.0 * math.pi
DIAGNOSTIC_COMPACTNESS = 0.1  # Declared illustration, NOT a physical phase boundary


def _number(item: dict, field: str, *, positive: bool = False,
            nonnegative: bool = False) -> float:
    if field not in item or isinstance(item[field], bool):
        raise ValueError(f"Missing or invalid required numeric field: {field}")
    try:
        value = float(item[field])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric field: {field}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Nonfinite numeric field: {field}")
    if positive and not value > 0:
        raise ValueError(f"Expected {field} > 0")
    if nonnegative and not value >= 0:
        raise ValueError(f"Expected {field} >= 0")
    return value


def _optional(item: dict, field: str, *, nonnegative: bool = True) -> float | None:
    if item.get(field) is None:
        return None
    return _number(item, field, nonnegative=nonnegative)


def _diagnostics(m: float, r: float, p: float, epsilon: float,
                 s_bits: float | None, excitation_j: float | None,
                 temp_cap_k: float | None) -> dict:
    cpt = compactness(m, r)
    if not math.isfinite(cpt):
        raise ValueError("Compactness overflow: reduce input scale")
    area = FOUR_PI * r * r
    heat_flux = p / area
    temp_k = (heat_flux / (epsilon * SIGMA_SB)) ** 0.25
    bound_bits = bekenstein_bound_bits(m, r)
    bh_bits = black_hole_entropy_bits_same_mass(m)
    if not all(math.isfinite(x) for x in (area, heat_flux, temp_k, bound_bits, bh_bits)):
        raise ValueError("Derived quantity overflow: reduce input scale")
    weak_label = cpt < DIAGNOSTIC_COMPACTNESS
    if s_bits is None:
        entropy_status = "NOT_PROVIDED"
    elif not weak_label:
        entropy_status = "BOUND_NOT_USED_OUTSIDE_WEAK_REGIME"
    elif s_bits > bound_bits:
        entropy_status = "EXCEEDS_ASSUMED_BEKENSTEIN_BOUND"
    else:
        entropy_status = "BELOW_ASSUMED_BEKENSTEIN_BOUND"
    return {
        "mass_kg": m,
        "radius_m": r,
        "schwarzschild_radius_m": schwarzschild_radius_m(m),
        "compactness": cpt,
        "mean_density_kg_m3": m / ((FOUR_PI / 3.0) * r ** 3),
        "radiative_area_m2": area,
        "dissipated_power_w": p,
        "radiative_surface_flux_w_m2": heat_flux,
        "blackbody_equivalent_temperature_k": temp_k,
        "blackbody_temperature_cap_k": temp_cap_k,
        "thermal_cap_exceeded": None if temp_cap_k is None else temp_k > temp_cap_k,
        "bekenstein_formal_upper_bits": bound_bits,
        "bh_entropy_at_same_mass_bits": bh_bits,
        "assumed_entropy_bits": s_bits,
        "entropy_check": entropy_status,
        "margolus_levitin_upper_ops_s": (
            None if excitation_j is None else 2 * excitation_j / (math.pi * HBAR)
        ),
        "compactness_diagnostic": (
            "SCHWARZSCHILD_RATIO_GE_1_NOT_PROVEN_HORIZON" if cpt >= 1
            else "HIGH_COMPACTNESS_DIAGNOSTIC" if not weak_label
            else "LOW_COMPACTNESS_DIAGNOSTIC"
        ),
    }


def _crossing_time(m0: float, c0: float, mdot: float, exponent: float) -> float | None:
    # Only the stipulated constant-mdot, R ~ M^exponent law is considered.
    if c0 >= 1:
        return 0.0
    if mdot == 0 or exponent >= 1:
        return None
    log_ratio = -math.log(c0) / (1.0 - exponent)
    # Guard against numerical overflow rather than making an unphysical assertion.
    if log_ratio > 690.0:
        return None
    m_cross = m0 * math.exp(log_ratio)
    if not math.isfinite(m_cross):
        return None
    t = (m_cross - m0) / mdot
    return t if math.isfinite(t) and t >= 0 else None


def evaluate_case(case: dict) -> dict:
    name = case.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Each case needs a nonempty name")
    m0 = _number(case, "initial_mass_kg", positive=True)
    r0 = _number(case, "initial_radius_m", positive=True)
    p = _number(case, "dissipated_power_w", nonnegative=True)
    mdot = _number(case, "mass_growth_rate_kg_s", nonnegative=True)
    dt = _number(case, "duration_s", nonnegative=True)
    exponent = _number(case, "radius_mass_exponent")
    epsilon = _number(case, "radiation_emissivity", positive=True)
    if epsilon > 1:
        raise ValueError("radiation_emissivity must be <= 1")
    entropy_bits = _optional(case, "assumed_entropy_bits")
    excitation_j = _optional(case, "excitation_energy_above_ground_j")
    temp_cap = _optional(case, "max_surface_temperature_k")
    if temp_cap is not None and temp_cap <= 0:
        raise ValueError("max_surface_temperature_k must be positive")
    if excitation_j is not None and excitation_j > m0 * C * C:
        raise ValueError("Excitation energy cannot exceed initial total rest energy")
    mf = m0 + mdot * dt
    rf = r0 * (mf / m0) ** exponent
    if not (math.isfinite(mf) and math.isfinite(rf) and rf > 0):
        raise ValueError("Evolved mass/radius not finite or positive")
    initial = _diagnostics(m0, r0, p, epsilon, entropy_bits, excitation_j, temp_cap)
    final = _diagnostics(mf, rf, p, epsilon, entropy_bits, excitation_j, temp_cap)
    crossing_s = _crossing_time(m0, initial["compactness"], mdot, exponent)
    return {
        "name": name,
        "assumptions": {
            "mass_growth_rate_kg_s": mdot,
            "duration_s": dt,
            "radius_mass_exponent": exponent,
            "radiation_emissivity": epsilon,
            "growth_law": "M(t)=M0+mdot*t; R(t)=R0*(M(t)/M0)^exponent",
            "power_law": "constant total dissipated power (not a mass-energy supply model)",
            "thermal_law": "uniform-area Stefan-Boltzmann-equivalent radiation",
            "is_spherical_nonrotating_compactness_proxy": True,
        },
        "initial": initial,
        "final": final,
        "schwarzschild_ratio_crossing_s_under_law": crossing_s,
        "crossing_within_declared_duration": (
            None if crossing_s is None else crossing_s <= dt
        ),
        "physical_reachability_assessed": False,
    }


def evaluate_contract(contract: dict) -> dict:
    if contract.get("status") != "illustrative_conditional_sweep":
        raise ValueError("status must explicitly identify an illustrative conditional sweep")
    cases = contract.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    names = [c.get("name") for c in cases if isinstance(c, dict)]
    if len(set(names)) != len(cases):
        raise ValueError("Cases must have distinct names and be objects")
    return {
        "status": "CONDITIONAL_CALCULATION_NOT_EMPIRICAL_TEST",
        "diagnostic_compactness_threshold": DIAGNOSTIC_COMPACTNESS,
        "allowed_claim": "Textbook conditional bounds for the declared SI inputs and growth laws.",
        "forbidden_claim": "A feasible self-replicating trajectory, engineered collapse, black-hole formation, or quantum foam.",
        "cases": [evaluate_case(c) for c in cases],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate_contract(json.loads(args.contract.read_text(encoding="utf-8")))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
                        encoding="utf-8")


if __name__ == "__main__":
    main()
