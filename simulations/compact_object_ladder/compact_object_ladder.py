"""Natural compact-object ladder for transferability checks.

The cases are fixed astronomical/natural reference systems. This script does
not accept arbitrary inputs and does not model construction or growth.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

G = 6.67430e-11
C = 299_792_458.0
HBAR = 1.054_571_817e-34
LN2 = math.log(2.0)

M_SUN = 1.98847e30
R_SUN = 6.957e8
M_EARTH = 5.9722e24
R_EARTH = 6.371e6

REFERENCE_CASES = (
    ("Earth", M_EARTH, R_EARTH),
    ("Sun", M_SUN, R_SUN),
    ("Canonical 0.6 Msun white dwarf", 0.6 * M_SUN, 0.012 * R_SUN),
    ("Canonical 1.4 Msun neutron star", 1.4 * M_SUN, 12_000.0),
)


def schwarzschild_radius_m(mass_kg: float) -> float:
    return 2.0 * G * mass_kg / C**2


def compactness(mass_kg: float, radius_m: float) -> float:
    return schwarzschild_radius_m(mass_kg) / radius_m


def bekenstein_bound_bits(mass_kg: float, radius_m: float) -> float:
    energy_j = mass_kg * C**2
    return 2.0 * math.pi * radius_m * energy_j / (HBAR * C * LN2)


def black_hole_entropy_bits_same_mass(mass_kg: float) -> float:
    rs = schwarzschild_radius_m(mass_kg)
    area_m2 = 4.0 * math.pi * rs**2
    return C**3 * area_m2 / (4.0 * G * HBAR * LN2)


def row(name: str, mass_kg: float, radius_m: float) -> dict[str, object]:
    rs = schwarzschild_radius_m(mass_kg)
    comp = rs / radius_m
    bek = bekenstein_bound_bits(mass_kg, radius_m)
    bh = black_hole_entropy_bits_same_mass(mass_kg)
    return {
        "name": name,
        "mass_kg": mass_kg,
        "radius_m": radius_m,
        "schwarzschild_radius_m": rs,
        "compactness": comp,
        "radius_over_schwarzschild_radius": radius_m / rs,
        "bekenstein_bound_bits": bek,
        "bh_entropy_bits_same_mass": bh,
        "entropy_ratio": bek / bh,
    }


def rows() -> list[dict[str, object]]:
    out = [row(*case) for case in REFERENCE_CASES]
    rs_sun = schwarzschild_radius_m(M_SUN)
    out.append(row("1 Msun Schwarzschild boundary", M_SUN, rs_sun))
    return out


def write_csv(path: Path) -> None:
    data = rows()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    write_csv(Path(__file__).with_name("reference_results.csv"))
