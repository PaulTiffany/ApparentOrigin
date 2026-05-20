"""Pre-registered v1 proof-derived AOC threshold-deformation analysis.

Implements the contract in `empirical/aoc_proof_derived_contract_v1.md`:

    delta_mu_AOC(z; lambda_K, p) = lambda_K * (1 + z)^{p - 1}

Pre-registered p values (committed before any v1 fit was run):
    p_primary = 1.8 (matches simulations/apparatus_bound_k/apparatus_k.py)
    p_robust  = 2.0

Pre-registered cutoffs:
    z_cut_primary   = 1.0
    z_cut_secondary = 0.75

Pre-registered injection grid (power test):
    lambda_K_inj in {0.0, -0.025, -0.050, -0.075, -0.100, -0.150, -0.200}
    n_seeds = 200, seed_root = 20260426

The v0 phenomenological log-threshold deformation is also evaluated on the
same machinery and the same lambda_K injection grid for direct shape
comparison. v1 does not deprecate v0; both contracts coexist.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.linalg import cho_factor, cho_solve

from analyze_pantheon_k import (
    COV_PATH,
    RAW_PATH,
    FlatLambdaCDM,
    distance_modulus_lcdm,
    load_covariance,
    load_rows,
)


ROOT = Path(__file__).resolve().parents[2]
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
REPORT_DIR = ROOT / "reports" / "pantheon_plus"
ACTUAL_PATH = DERIVED_DIR / "pantheon_v1_actual_fit.csv"
POWER_PATH = DERIVED_DIR / "pantheon_v1_power.csv"
SUMMARY_PATH = DERIVED_DIR / "pantheon_v1_summary.json"
PLOT_PATH = REPORT_DIR / "pantheon_v1_proof_derived.png"

COSMO = FlatLambdaCDM()


def deformation_v0(z: np.ndarray) -> np.ndarray:
    """v0 phenomenological: log(1 + z / 0.8)."""

    return np.log1p(np.asarray(z, dtype=float) / 0.8)


def deformation_v1(z: np.ndarray, p: float) -> np.ndarray:
    """v1 proof-derived: (1 + z)^{p - 1}."""

    return (1.0 + np.asarray(z, dtype=float)) ** (p - 1.0)


@dataclass(frozen=True)
class Spec:
    name: str
    p: float | None
    fn: Callable[[np.ndarray], np.ndarray]
    shape_at_z1: float

    def deform_at_z(self, z: float) -> float:
        return float(self.fn(np.array([z]))[0])


def make_specs() -> list[Spec]:
    return [
        Spec(
            name="v0_log",
            p=None,
            fn=deformation_v0,
            shape_at_z1=float(deformation_v0(np.array([1.0]))[0]),
        ),
        Spec(
            name="v1_pow_p1.8",
            p=1.8,
            fn=lambda z: deformation_v1(z, 1.8),
            shape_at_z1=float(deformation_v1(np.array([1.0]), 1.8)[0]),
        ),
        Spec(
            name="v1_pow_p2.0",
            p=2.0,
            fn=lambda z: deformation_v1(z, 2.0),
            shape_at_z1=float(deformation_v1(np.array([1.0]), 2.0)[0]),
        ),
    ]


def precompute_block(rows, cov, z_cut, deformation_fn):
    """Subset by z_cut and precompute the linear-algebra tensors."""

    usable = [idx for idx, row in enumerate(rows) if row.mu is not None]
    subset = [idx for idx in usable if rows[idx].z <= z_cut]
    n = len(subset)
    z = np.array([rows[idx].z for idx in subset], dtype=float)
    mu_obs = np.array([rows[idx].mu for idx in subset], dtype=float)
    mu_lcdm = np.array(
        [distance_modulus_lcdm(rows[idx].z, COSMO) for idx in subset], dtype=float
    )
    deform = deformation_fn(z)
    ones = np.ones(n, dtype=float)
    subcov = cov[np.ix_(subset, subset)] + np.eye(n) * 1e-9
    cho = cho_factor(subcov, lower=True, check_finite=False)
    q_def = cho_solve(cho, deform, check_finite=False)
    q_ones = cho_solve(cho, ones, check_finite=False)
    return {
        "n": n,
        "z_cut": z_cut,
        "z": z,
        "mu_obs": mu_obs,
        "mu_lcdm": mu_lcdm,
        "deformation": deform,
        "ones": ones,
        "cho": cho,
        "q_def": q_def,
        "q_ones": q_ones,
        "d_p_d": float(deform @ q_def),
        "d_p_1": float(deform @ q_ones),
        "one_p_one": float(ones @ q_ones),
    }


def chi2_grid_inner(block, r_p_r, r_p_d, one_p_r, lambdas):
    """Vectorized chi2 grid given precomputed scalar inner products."""

    d_p_d = block["d_p_d"]
    d_p_1 = block["d_p_1"]
    one_p_one = block["one_p_one"]
    v_p_v = r_p_r - 2.0 * lambdas * r_p_d + (lambdas ** 2) * d_p_d
    one_p_v = one_p_r - lambdas * d_p_1
    return v_p_v - (one_p_v ** 2) / one_p_one


def actual_data_fit(block, lambdas):
    residual = block["mu_obs"] - block["mu_lcdm"]
    q_r = cho_solve(block["cho"], residual, check_finite=False)
    r_p_r = float(residual @ q_r)
    r_p_d = float(residual @ block["q_def"])
    one_p_r = float(block["ones"] @ q_r)
    chi2_grid = chi2_grid_inner(block, r_p_r, r_p_d, one_p_r, lambdas)
    idx_zero = int(np.argmin(np.abs(lambdas)))
    lcdm_chi2 = float(chi2_grid[idx_zero])
    best_idx = int(np.argmin(chi2_grid))
    best_lambda = float(lambdas[best_idx])
    best_chi2 = float(chi2_grid[best_idx])
    return {
        "n": block["n"],
        "z_cut": block["z_cut"],
        "best_lambda": best_lambda,
        "lcdm_chi2": lcdm_chi2,
        "best_chi2": best_chi2,
        "delta_chi2": best_chi2 - lcdm_chi2,
        "delta_aic": (best_chi2 - lcdm_chi2) + 2.0,
        "delta_bic": (best_chi2 - lcdm_chi2) + math.log(block["n"]),
    }


def power_test_block(block, lambda_inj_values, lambdas, n_seeds, seed_root):
    """Run the power test for one (spec, z_cut) block; return per-lambda_inj arrays."""

    n = block["n"]
    L = np.tril(block["cho"][0])
    log_n = math.log(n)
    deform = block["deformation"]
    ones = block["ones"]
    d_p_d = block["d_p_d"]
    d_p_1 = block["d_p_1"]

    out = {
        float(lam): {"best_lambda": [], "delta_chi2": [], "delta_bic": []}
        for lam in lambda_inj_values
    }

    idx_zero = int(np.argmin(np.abs(lambdas)))
    for seed_idx in range(n_seeds):
        rng = np.random.default_rng(seed_root + seed_idx)
        iid = rng.standard_normal(n)
        noise = L @ iid
        q_n = cho_solve(block["cho"], noise, check_finite=False)
        n_p_n = float(noise @ q_n)
        d_p_n = float(deform @ q_n)
        one_p_n = float(ones @ q_n)
        for lam_inj in lambda_inj_values:
            r_p_r = (lam_inj ** 2) * d_p_d + 2.0 * lam_inj * d_p_n + n_p_n
            r_p_d = lam_inj * d_p_d + d_p_n
            one_p_r = lam_inj * d_p_1 + one_p_n
            chi2_grid = chi2_grid_inner(block, r_p_r, r_p_d, one_p_r, lambdas)
            lcdm_chi2 = float(chi2_grid[idx_zero])
            best_idx = int(np.argmin(chi2_grid))
            best_lambda = float(lambdas[best_idx])
            best_chi2 = float(chi2_grid[best_idx])
            delta_chi2 = best_chi2 - lcdm_chi2
            out[float(lam_inj)]["best_lambda"].append(best_lambda)
            out[float(lam_inj)]["delta_chi2"].append(delta_chi2)
            out[float(lam_inj)]["delta_bic"].append(delta_chi2 + log_n)
    return out


def main():
    print("Loading Pantheon+ rows and covariance...")
    rows, _ = load_rows(RAW_PATH)
    cov = load_covariance(COV_PATH, len(rows))
    if cov is None:
        raise SystemExit("Covariance not available; cannot run v1 contract.")

    specs = make_specs()
    z_cuts = [1.0, 0.75]
    lambdas = np.round(np.arange(-0.30, 0.301, 0.01), 6)
    lambda_inj_values = [0.0, -0.025, -0.050, -0.075, -0.100, -0.150, -0.200]
    n_seeds = 200
    seed_root = 20260426

    print(
        f"Running 3 specs x {len(z_cuts)} z_cuts; "
        f"each: actual fit + power test ({n_seeds} seeds x {len(lambda_inj_values)} lambda_inj)..."
    )

    actual_rows = []
    power_rows = []

    for spec in specs:
        for z_cut in z_cuts:
            print(f"  spec={spec.name} z_cut={z_cut} ...")
            block = precompute_block(rows, cov, z_cut, spec.fn)
            fit = actual_data_fit(block, lambdas)
            mag_at_z1 = fit["best_lambda"] * spec.shape_at_z1
            actual_rows.append(
                {
                    "spec": spec.name,
                    "p": spec.p if spec.p is not None else "",
                    "z_cut": z_cut,
                    "n": block["n"],
                    "best_lambda": fit["best_lambda"],
                    "shape_at_z1": spec.shape_at_z1,
                    "mag_shift_at_z1": mag_at_z1,
                    "lcdm_chi2": fit["lcdm_chi2"],
                    "best_chi2": fit["best_chi2"],
                    "delta_chi2": fit["delta_chi2"],
                    "delta_aic": fit["delta_aic"],
                    "delta_bic": fit["delta_bic"],
                }
            )
            results = power_test_block(block, lambda_inj_values, lambdas, n_seeds, seed_root)
            for lam in lambda_inj_values:
                bucket = results[float(lam)]
                bl = np.array(bucket["best_lambda"])
                db = np.array(bucket["delta_bic"])
                power_rows.append(
                    {
                        "spec": spec.name,
                        "p": spec.p if spec.p is not None else "",
                        "z_cut": z_cut,
                        "lambda_inj": float(lam),
                        "shape_at_z1": spec.shape_at_z1,
                        "mag_inj_at_z1": float(lam) * spec.shape_at_z1,
                        "n_seeds": int(n_seeds),
                        "median_best_lambda": float(np.median(bl)),
                        "p10_best_lambda": float(np.percentile(bl, 10)),
                        "p90_best_lambda": float(np.percentile(bl, 90)),
                        "bias_best_lambda": float(np.median(bl) - lam),
                        "median_delta_bic": float(np.median(db)),
                        "p10_delta_bic": float(np.percentile(db, 10)),
                        "p90_delta_bic": float(np.percentile(db, 90)),
                        "frac_dbic_below_zero": float(np.mean(db < 0.0)),
                        "frac_dbic_below_minus_two": float(np.mean(db < -2.0)),
                        "frac_dbic_below_minus_ten": float(np.mean(db < -10.0)),
                    }
                )

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with ACTUAL_PATH.open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(actual_rows[0].keys()))
        writer.writeheader()
        writer.writerows(actual_rows)
    with POWER_PATH.open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(power_rows[0].keys()))
        writer.writeheader()
        writer.writerows(power_rows)

    summary = {
        "contract": "v1 proof-derived AOC deformation (pre-registered 2026-04-26)",
        "specs": [
            {
                "name": s.name,
                "p": s.p,
                "shape_at_z1": s.shape_at_z1,
                "shape_form": (
                    "log(1 + z/0.8)" if s.name == "v0_log" else f"(1+z)^{(s.p - 1):.3g}"
                ),
            }
            for s in specs
        ],
        "z_cuts": z_cuts,
        "lambda_inj_values": lambda_inj_values,
        "n_seeds": n_seeds,
        "seed_root": seed_root,
        "actual_fits": actual_rows,
        "power": power_rows,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Console summary
    print()
    print("Actual-data fits:")
    print(
        "  "
        + "  ".join(["spec".ljust(15), "z_cut", "n", "best_lambda", "mag_at_z1", "delta_chi2", "delta_bic"])
    )
    for r in actual_rows:
        print(
            f"  {r['spec'].ljust(15)} {r['z_cut']:.2f}  {r['n']:5d}  "
            f"best_lambda={r['best_lambda']:+.3f}  "
            f"mag@z=1={r['mag_shift_at_z1']:+.3f}  "
            f"delta_chi2={r['delta_chi2']:+8.2f}  "
            f"delta_bic={r['delta_bic']:+8.2f}"
        )

    print()
    print("Power summary at z_cut = 1.0 (frac dBIC < -2):")
    for spec in specs:
        print(f"  {spec.name}:")
        for r in power_rows:
            if r["spec"] == spec.name and r["z_cut"] == 1.0:
                print(
                    f"    lam_inj={r['lambda_inj']:+.4f} "
                    f"mag@z=1={r['mag_inj_at_z1']:+.3f}  "
                    f"med dBIC={r['median_delta_bic']:+7.2f}  "
                    f"P(dBIC<-2)={r['frac_dbic_below_minus_two']:.2f}  "
                    f"P(dBIC<-10)={r['frac_dbic_below_minus_ten']:.2f}"
                )

    # Plot: recovery + power on common magnitude scale at z=1
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        plt = None

    if plt is not None:
        fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), dpi=150)
        colors = {
            "v0_log": "#1d7f8c",
            "v1_pow_p1.8": "#d28f2d",
            "v1_pow_p2.0": "#6f5aa7",
        }

        # Panel 1: recovery on lambda scale (separate axes per spec, plot in own units).
        for spec in specs:
            rows_for = [r for r in power_rows if r["spec"] == spec.name and r["z_cut"] == 1.0]
            rows_for.sort(key=lambda r: r["lambda_inj"])
            x = [r["lambda_inj"] for r in rows_for]
            med = [r["median_best_lambda"] for r in rows_for]
            lo = [r["p10_best_lambda"] for r in rows_for]
            hi = [r["p90_best_lambda"] for r in rows_for]
            axes[0].plot(x, med, marker="o", color=colors[spec.name], label=spec.name)
            axes[0].fill_between(x, lo, hi, color=colors[spec.name], alpha=0.18)
        axes[0].plot([-0.22, 0.02], [-0.22, 0.02], color="#9c4638", linewidth=1.0, linestyle="--", label="lambda_fit = lambda_inj")
        axes[0].set_xlabel("lambda_K_inj (per-spec units)")
        axes[0].set_ylabel("recovered lambda_fit")
        axes[0].set_title("Recovery (z_cut = 1.0)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.22)

        # Panel 2: power vs magnitude shift at z=1 (apples-to-apples across specs).
        for spec in specs:
            rows_for = [r for r in power_rows if r["spec"] == spec.name and r["z_cut"] == 1.0]
            rows_for.sort(key=lambda r: r["mag_inj_at_z1"])
            x = [r["mag_inj_at_z1"] for r in rows_for]
            frac = [r["frac_dbic_below_minus_two"] for r in rows_for]
            axes[1].plot(x, frac, marker="o", color=colors[spec.name], label=spec.name)
        axes[1].axhline(0.5, color="#9c4638", linewidth=1.0, linestyle="--", label="50%")
        axes[1].set_xlabel("injected mu shift at z = 1 (mag)")
        axes[1].set_ylabel("P(dBIC < -2)")
        axes[1].set_title("Detection power, common z=1 magnitude scale")
        axes[1].set_ylim(-0.05, 1.05)
        axes[1].legend()
        axes[1].grid(True, alpha=0.22)

        # Mark the actual-data best-fit magnitude at z=1 for each spec at z_cut=1.0.
        for spec in specs:
            row = [r for r in actual_rows if r["spec"] == spec.name and r["z_cut"] == 1.0][0]
            axes[1].axvline(
                row["mag_shift_at_z1"],
                color=colors[spec.name],
                linewidth=0.9,
                linestyle=":",
                alpha=0.9,
            )

        fig.tight_layout()
        fig.savefig(PLOT_PATH)
        plt.close(fig)

    print()
    print(f"Wrote {ACTUAL_PATH}")
    print(f"Wrote {POWER_PATH}")
    print(f"Wrote {SUMMARY_PATH}")
    if PLOT_PATH.exists():
        print(f"Wrote {PLOT_PATH}")


if __name__ == "__main__":
    main()
