"""Power test for the v0 AOC threshold-deformation diagnostic.

The v0 contract reports an exploratory ΔBIC ~ -3 at z_cut ~ 1.0 with best
fitted lambda ~ -0.13. That number is uninterpretable on its own: we do not
yet know whether the diagnostic has the power to detect a real signal at that
lambda, or whether the same ΔBIC could come from pure noise under the
Pantheon+ covariance.

This script answers that question by injecting a known lambda_inj into a
synthetic distance-modulus vector (mu_LCDM(z) + lambda_inj * log(1 + z/z_star)
+ multivariate-normal noise drawn from the Pantheon+ covariance), then running
the same v0 fit machinery to recover the best lambda and compute ΔBIC. This
is the SRMF amortization move applied to the v0 deformation contract: rather
than asking whether the same fit is portable across data splits, we ask
whether the fit can recover known truth on synthetic data whose pipeline is
fully ours.

Caveats:
1. The covariance matrix is taken as given; this is a power test conditional
   on Pantheon+'s stated noise model being correct.
2. The deformation form is held fixed at the v0 contract; this does not
   address misspecification of the deformation itself.
3. No real-cosmology claim follows from this run.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

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
RECOVERY_PATH = DERIVED_DIR / "pantheon_power_test_recovery.csv"
POWER_PATH = DERIVED_DIR / "pantheon_power_test_power.csv"
SUMMARY_PATH = DERIVED_DIR / "pantheon_power_test_summary.json"
PLOT_PATH = REPORT_DIR / "pantheon_power_test.png"

Z_STAR = 0.8
COSMOLOGY = FlatLambdaCDM()


def precompute_subset(
    rows,
    cov: np.ndarray,
    z_cut: float,
):
    """Precompute the per-(z_cut) tensors needed by the inner loop.

    Returns a dict with keys:
        n            int, subset size
        cho          scipy cho_factor of (subcov + jitter)
        deformation  shape (n,)
        ones         shape (n,)
        q_def        shape (n,) = solve(C, deformation)
        q_ones       shape (n,) = solve(C, ones)
        d_p_d, d_p_1, one_p_one  scalars
    """

    usable = [idx for idx, row in enumerate(rows) if row.mu is not None]
    subset = [idx for idx in usable if rows[idx].z <= z_cut]
    n = len(subset)
    z = np.array([rows[idx].z for idx in subset], dtype=float)
    deformation = np.log1p(z / Z_STAR)
    ones = np.ones(n, dtype=float)
    subcov = cov[np.ix_(subset, subset)] + np.eye(n) * 1e-9
    cho = cho_factor(subcov, lower=True, check_finite=False)
    q_def = cho_solve(cho, deformation, check_finite=False)
    q_ones = cho_solve(cho, ones, check_finite=False)
    d_p_d = float(deformation @ q_def)
    d_p_1 = float(deformation @ q_ones)
    one_p_one = float(ones @ q_ones)
    return {
        "n": n,
        "subset": subset,
        "cho": cho,
        "deformation": deformation,
        "ones": ones,
        "q_def": q_def,
        "q_ones": q_ones,
        "d_p_d": d_p_d,
        "d_p_1": d_p_1,
        "one_p_one": one_p_one,
    }


def chi2_from_residual_scalars(
    r_p_r: float,
    r_p_d: float,
    one_p_r: float,
    d_p_d: float,
    d_p_1: float,
    one_p_one: float,
    lambdas: np.ndarray,
):
    """Vectorized chi2 over a lambda grid for v = residual - lambda * deformation,
    with the constant magnitude offset marginalized.

    Identities:
        v_p_v(lambda)   = r_p_r - 2 lambda r_p_d + lambda^2 d_p_d
        one_p_v(lambda) = one_p_r - lambda d_p_1
        chi2(lambda)    = v_p_v - one_p_v^2 / one_p_one
    """

    v_p_v = r_p_r - 2.0 * lambdas * r_p_d + (lambdas ** 2) * d_p_d
    one_p_v = one_p_r - lambdas * d_p_1
    chi2 = v_p_v - (one_p_v ** 2) / one_p_one
    return chi2


def run_one_seed(
    rng: np.random.Generator,
    block: dict,
    lambda_inj_values: np.ndarray,
    lambda_test_grid: np.ndarray,
):
    """One seed: draw one noise vector, evaluate all (lambda_inj, lambda_test) pairs.

    For each lambda_inj, residual = lambda_inj * deformation + noise. We share
    the costly part across lambda_inj: precomputed q_def, q_ones, plus a single
    cho_solve for the noise vector.

    Returns a dict mapping lambda_inj -> (best_lambda, best_chi2, lcdm_chi2).
    """

    n = block["n"]
    cho = block["cho"]
    deformation = block["deformation"]
    q_def = block["q_def"]
    q_ones = block["q_ones"]
    d_p_d = block["d_p_d"]
    d_p_1 = block["d_p_1"]
    one_p_one = block["one_p_one"]
    ones = block["ones"]

    iid = rng.standard_normal(n)
    # noise = L @ iid where C = L L^T  (Cholesky lower); construct using cho_factor.
    L = np.tril(cho[0])
    noise = L @ iid

    q_n = cho_solve(cho, noise, check_finite=False)
    n_p_n = float(noise @ q_n)
    d_p_n = float(deformation @ q_n)  # equals noise @ q_def by symmetry
    one_p_n = float(ones @ q_n)

    out = {}
    for lambda_inj in lambda_inj_values:
        r_p_r = (lambda_inj ** 2) * d_p_d + 2.0 * lambda_inj * d_p_n + n_p_n
        r_p_d = lambda_inj * d_p_d + d_p_n
        one_p_r = lambda_inj * d_p_1 + one_p_n

        chi2_grid = chi2_from_residual_scalars(
            r_p_r, r_p_d, one_p_r, d_p_d, d_p_1, one_p_one, lambda_test_grid
        )
        # LCDM chi2 corresponds to dropping the deformation column entirely,
        # which is the lambda_test = 0 case in our parameterization.
        idx_zero = int(np.argmin(np.abs(lambda_test_grid)))
        lcdm_chi2 = float(chi2_grid[idx_zero])
        best_idx = int(np.argmin(chi2_grid))
        best_lambda = float(lambda_test_grid[best_idx])
        best_chi2 = float(chi2_grid[best_idx])
        out[float(lambda_inj)] = (best_lambda, best_chi2, lcdm_chi2)
    return out


def main() -> None:
    print("Loading Pantheon+ rows and covariance...")
    rows, _ = load_rows(RAW_PATH)
    cov = load_covariance(COV_PATH, len(rows))
    if cov is None:
        raise SystemExit("Covariance not available; cannot run power test.")

    z_cuts = [0.75, 1.0, 1.5]
    lambda_inj_values = np.array([0.0, -0.05, -0.10, -0.13, -0.15, -0.20, -0.25])
    lambda_test_grid = np.round(np.arange(-0.30, 0.301, 0.01), 6)
    n_seeds = 200
    seed_root = 20260426

    print(f"Precomputing per-z_cut blocks for z_cuts = {z_cuts}...")
    blocks = {z_cut: precompute_subset(rows, cov, z_cut) for z_cut in z_cuts}
    for z_cut, block in blocks.items():
        print(f"  z_cut={z_cut}: n={block['n']}")

    print(f"Running {n_seeds} seeds x {len(lambda_inj_values)} lambda_inj x {len(z_cuts)} z_cuts...")
    # Per (z_cut, lambda_inj), accumulate best_lambda and delta_bic across seeds.
    per_pair_results: dict[tuple[float, float], dict[str, list[float]]] = {}
    for z_cut in z_cuts:
        for lam in lambda_inj_values:
            per_pair_results[(z_cut, float(lam))] = {
                "best_lambda": [],
                "best_chi2": [],
                "lcdm_chi2": [],
                "delta_chi2": [],
                "delta_bic": [],
            }

    for z_cut in z_cuts:
        block = blocks[z_cut]
        n = block["n"]
        log_n = math.log(n)
        for seed_idx in range(n_seeds):
            rng = np.random.default_rng(seed_root + seed_idx)
            seed_results = run_one_seed(rng, block, lambda_inj_values, lambda_test_grid)
            for lam_inj, (best_lambda, best_chi2, lcdm_chi2) in seed_results.items():
                bucket = per_pair_results[(z_cut, lam_inj)]
                bucket["best_lambda"].append(best_lambda)
                bucket["best_chi2"].append(best_chi2)
                bucket["lcdm_chi2"].append(lcdm_chi2)
                delta_chi2 = best_chi2 - lcdm_chi2
                bucket["delta_chi2"].append(delta_chi2)
                bucket["delta_bic"].append(delta_chi2 + log_n)

    # Recovery + power tables.
    recovery_rows = []
    power_rows = []
    for z_cut in z_cuts:
        for lam_inj in lambda_inj_values:
            bucket = per_pair_results[(z_cut, float(lam_inj))]
            best_lambda = np.array(bucket["best_lambda"], dtype=float)
            delta_bic = np.array(bucket["delta_bic"], dtype=float)
            recovery_rows.append(
                {
                    "z_cut": z_cut,
                    "K_cut": 1.0 + z_cut,
                    "lambda_inj": float(lam_inj),
                    "n_seeds": int(len(best_lambda)),
                    "median_best_lambda": float(np.median(best_lambda)),
                    "p10_best_lambda": float(np.percentile(best_lambda, 10)),
                    "p90_best_lambda": float(np.percentile(best_lambda, 90)),
                    "bias_best_lambda": float(np.median(best_lambda) - lam_inj),
                }
            )
            power_rows.append(
                {
                    "z_cut": z_cut,
                    "K_cut": 1.0 + z_cut,
                    "lambda_inj": float(lam_inj),
                    "n_seeds": int(len(delta_bic)),
                    "median_delta_bic": float(np.median(delta_bic)),
                    "p10_delta_bic": float(np.percentile(delta_bic, 10)),
                    "p90_delta_bic": float(np.percentile(delta_bic, 90)),
                    "frac_delta_bic_below_zero": float(np.mean(delta_bic < 0.0)),
                    "frac_delta_bic_below_minus_two": float(np.mean(delta_bic < -2.0)),
                    "frac_delta_bic_below_minus_ten": float(np.mean(delta_bic < -10.0)),
                }
            )

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with RECOVERY_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(recovery_rows[0].keys()))
        writer.writeheader()
        writer.writerows(recovery_rows)
    with POWER_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(power_rows[0].keys()))
        writer.writeheader()
        writer.writerows(power_rows)

    summary = {
        "contract": "Pantheon+ v0 deformation power test under known lambda_inj",
        "allowed_claim": (
            "The v0 threshold-deformation diagnostic recovers injected lambda "
            "and has measured detection power against ΔBIC thresholds at the "
            "Pantheon+ covariance, conditional on that covariance being correct."
        ),
        "forbidden_claim": (
            "This validates AOC, refutes ΛCDM, or proves the observed Pantheon+ "
            "exploratory signal is real."
        ),
        "config": {
            "z_cuts": z_cuts,
            "lambda_inj_values": lambda_inj_values.tolist(),
            "lambda_test_grid_min": float(lambda_test_grid.min()),
            "lambda_test_grid_max": float(lambda_test_grid.max()),
            "lambda_test_grid_step": 0.01,
            "n_seeds": n_seeds,
            "z_star": Z_STAR,
            "cosmology": {"H0": COSMOLOGY.h0, "Omega_m": COSMOLOGY.omega_m},
            "subset_sizes": {str(z_cut): blocks[z_cut]["n"] for z_cut in z_cuts},
        },
        "recovery": recovery_rows,
        "power": power_rows,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Plot: recovery + power.
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        plt = None

    if plt is not None:
        fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), dpi=150)
        colors = ["#1d7f8c", "#d28f2d", "#6f5aa7"]
        for color, z_cut in zip(colors, z_cuts):
            rec = [r for r in recovery_rows if r["z_cut"] == z_cut]
            rec.sort(key=lambda r: r["lambda_inj"])
            x = [r["lambda_inj"] for r in rec]
            med = [r["median_best_lambda"] for r in rec]
            lo = [r["p10_best_lambda"] for r in rec]
            hi = [r["p90_best_lambda"] for r in rec]
            axes[0].plot(x, med, marker="o", color=color, label=f"z_cut={z_cut}")
            axes[0].fill_between(x, lo, hi, color=color, alpha=0.18)
        xs = [-0.27, 0.02]
        axes[0].plot(xs, xs, color="#9c4638", linewidth=1.0, linestyle="--", label="lambda_fit = lambda_inj")
        axes[0].set_xlabel("lambda_inj")
        axes[0].set_ylabel("recovered lambda_fit")
        axes[0].set_title("Recovery of injected lambda")
        axes[0].legend()
        axes[0].grid(True, alpha=0.22)

        for color, z_cut in zip(colors, z_cuts):
            pw = [r for r in power_rows if r["z_cut"] == z_cut]
            pw.sort(key=lambda r: r["lambda_inj"])
            x = [r["lambda_inj"] for r in pw]
            frac = [r["frac_delta_bic_below_minus_two"] for r in pw]
            axes[1].plot(x, frac, marker="o", color=color, label=f"z_cut={z_cut}")
        axes[1].axhline(0.5, color="#9c4638", linewidth=1.0, linestyle="--", label="50%")
        axes[1].set_xlabel("lambda_inj")
        axes[1].set_ylabel("P(ΔBIC < -2)")
        axes[1].set_title("Detection power at ΔBIC < -2")
        axes[1].set_ylim(-0.05, 1.05)
        axes[1].legend()
        axes[1].grid(True, alpha=0.22)

        fig.tight_layout()
        fig.savefig(PLOT_PATH)
        plt.close(fig)

    print(f"Wrote {RECOVERY_PATH}")
    print(f"Wrote {POWER_PATH}")
    print(f"Wrote {SUMMARY_PATH}")
    if PLOT_PATH.exists():
        print(f"Wrote {PLOT_PATH}")
    print()
    # Quick summary print for inspection (ASCII-only to keep Windows console happy).
    for z_cut in z_cuts:
        print(f"--- z_cut = {z_cut} (n = {blocks[z_cut]['n']}) ---")
        for lam in lambda_inj_values:
            bucket = per_pair_results[(z_cut, float(lam))]
            best_lambda = np.array(bucket["best_lambda"])
            delta_bic = np.array(bucket["delta_bic"])
            print(
                f"  lambda_inj={float(lam):+.3f}  "
                f"median lambda_fit={np.median(best_lambda):+.3f}  "
                f"median dBIC={np.median(delta_bic):+7.2f}  "
                f"P(dBIC<-2)={np.mean(delta_bic < -2.0):.2f}  "
                f"P(dBIC<-10)={np.mean(delta_bic < -10.0):.2f}"
            )


if __name__ == "__main__":
    main()
