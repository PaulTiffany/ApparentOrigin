import unittest

from compact_object_ladder import (
    M_EARTH,
    M_SUN,
    R_EARTH,
    R_SUN,
    bekenstein_bound_bits,
    black_hole_entropy_bits_same_mass,
    compactness,
    row,
    rows,
    schwarzschild_radius_m,
)


class CompactObjectLadderTests(unittest.TestCase):
    def test_solar_schwarzschild_radius(self):
        self.assertAlmostEqual(schwarzschild_radius_m(M_SUN), 2953.339382, places=6)

    def test_earth_compactness(self):
        self.assertAlmostEqual(compactness(M_EARTH, R_EARTH), 1.39226e-9, delta=1e-14)

    def test_entropy_ratio_is_inverse_compactness_for_sun(self):
        result = row("Sun", M_SUN, R_SUN)
        self.assertAlmostEqual(
            result["entropy_ratio"] * result["compactness"], 1.0, places=12
        )

    def test_entropy_expressions_meet_at_schwarzschild_boundary(self):
        rs = schwarzschild_radius_m(M_SUN)
        bek = bekenstein_bound_bits(M_SUN, rs)
        bh = black_hole_entropy_bits_same_mass(M_SUN)
        self.assertAlmostEqual(bek / bh, 1.0, places=12)

    def test_reference_ladder_is_fixed(self):
        self.assertEqual([r["name"] for r in rows()], [
            "Earth",
            "Sun",
            "Canonical 0.6 Msun white dwarf",
            "Canonical 1.4 Msun neutron star",
            "1 Msun Schwarzschild boundary",
        ])


if __name__ == "__main__":
    unittest.main()
