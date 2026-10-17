import unittest

from compact_object_ladder import M_SUN, R_SUN, compactness
from q0_self_gravity import evaluate_case, evaluate_contract


def example(**overrides):
    case = {
        "name": "case",
        "initial_mass_kg": M_SUN,
        "initial_radius_m": R_SUN,
        "dissipated_power_w": 3.828e26,
        "mass_growth_rate_kg_s": 0,
        "duration_s": 0,
        "radius_mass_exponent": 1 / 3,
        "radiation_emissivity": 1.0,
        "max_surface_temperature_k": 6000,
        "assumed_entropy_bits": None,
        "excitation_energy_above_ground_j": None,
    }
    case.update(overrides)
    return case


class Q0Tests(unittest.TestCase):
    def test_shared_ladder_compactness_and_equilibrium_temperature(self):
        r = evaluate_case(example())
        self.assertAlmostEqual(r["initial"]["compactness"], compactness(M_SUN, R_SUN))
        self.assertGreater(r["initial"]["blackbody_equivalent_temperature_k"], 5700)
        self.assertLess(r["initial"]["blackbody_equivalent_temperature_k"], 5900)
        self.assertFalse(r["initial"]["thermal_cap_exceeded"])
        self.assertEqual(r["initial"]["entropy_check"], "NOT_PROVIDED")
        self.assertFalse(r["physical_reachability_assessed"])

    def test_growth_law_crossing_is_only_conditional(self):
        # Mathematically crosses under a physically unsupported fixed-radius assumption.
        r = evaluate_case(example(
            initial_mass_kg=1e26, initial_radius_m=1.0,
            mass_growth_rate_kg_s=1e27, duration_s=10.0,
            radius_mass_exponent=0.0, max_surface_temperature_k=None,
        ))
        self.assertLess(r["initial"]["compactness"], 1)
        self.assertGreater(r["final"]["compactness"], 1)
        self.assertTrue(r["crossing_within_declared_duration"])
        self.assertFalse(r["physical_reachability_assessed"])

    def test_radius_linear_in_mass_never_crosses_from_weak(self):
        r = evaluate_case(example(
            initial_mass_kg=1e10, initial_radius_m=1,
            mass_growth_rate_kg_s=1e20, duration_s=100,
            radius_mass_exponent=1,
        ))
        self.assertAlmostEqual(r["initial"]["compactness"], r["final"]["compactness"])
        self.assertIsNone(r["schwarzschild_ratio_crossing_s_under_law"])

    def test_thermal_failure_not_gravity_failure(self):
        r = evaluate_case(example(dissipated_power_w=1e35, max_surface_temperature_k=6000))
        self.assertTrue(r["initial"]["thermal_cap_exceeded"])
        self.assertLess(r["initial"]["compactness"], 0.1)

    def test_excess_entropy_only_checked_under_declared_weak_proxy(self):
        r = evaluate_case(example(assumed_entropy_bits=1e100))
        self.assertEqual(r["initial"]["entropy_check"], "EXCEEDS_ASSUMED_BEKENSTEIN_BOUND")
        h = evaluate_case(example(
            initial_mass_kg=1e26, initial_radius_m=1.0,
            assumed_entropy_bits=1e100,
        ))
        self.assertEqual(h["initial"]["entropy_check"], "BOUND_NOT_USED_OUTSIDE_WEAK_REGIME")

    def test_missing_and_bad_parameters_cannot_be_interpreted_as_negative_science(self):
        c = example()
        del c["radius_mass_exponent"]
        with self.assertRaises(ValueError):
            evaluate_case(c)
        with self.assertRaises(ValueError):
            evaluate_case(example(radiation_emissivity=1.2))
        with self.assertRaises(ValueError):
            evaluate_contract({"status": "empirical", "cases": [example()]})

    def test_declared_sweep_marks_only_conditional_claim(self):
        x = evaluate_contract({"status": "illustrative_conditional_sweep",
                               "cases": [example()]})
        self.assertEqual(x["status"], "CONDITIONAL_CALCULATION_NOT_EMPIRICAL_TEST")
        self.assertEqual(len(x["cases"]), 1)


if __name__ == "__main__":
    unittest.main()
