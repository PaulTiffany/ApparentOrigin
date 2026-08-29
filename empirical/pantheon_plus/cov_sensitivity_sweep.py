"""Covariance-sensitivity sweep for v0 + v1 deformations.

Scales the assumed Pantheon+ covariance by `s` in `{0.7, 0.85, 1.0, 1.15,
1.3, 1.5}` and re-runs the actual-data fit and a null power test for the
three pre-registered specs (`v0_log`, `v1_pow_p1.8`, `v1_pow_p2.0`) at the
v1 primary cutoff `z_cut = 1.0`.

Scenario: the analyst chooses to use `sCov` consistently in the fit and the
null draw. Wilks then predicts that the null `Delta BIC` distribution stays
centered near `-1 + log(n) ~ +6.4` regardless of `s`, while the actual-data
`Delta BIC` scales as `Delta chi2_observed / s + log(n)` because chi2 with
the scaled covariance equals the original chi2 divided by `s`.

This is a simple uniform rescaling, not a stat/sys decomposition. The
underlying STAT+SYS distinction in Pantheon+ is not separated here; an
honest stat/sys sweep would require the un-summed components.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import cho_solve

from analyze_pantheon_k import (
    COV_PATH,
    RAW_PATH,
    load_covariance,
    load_rows,
)
from analyze_v1_proof_derived import (
    actual_data_fit,
    chi2_grid_inner,
    make_specs,
    precompute_block,
)


ROOT = Path(__file__).resolve().parents[2]
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
REPORT_DIR = ROOT / "reports" / "pantheon_plus"
SWEEP_PATH = DERIVED_DIR / "pantheon_cov_sweep.csv"
SUMMARY_PATH = DERIVED_DIR / "pantheon_cov_sweep_summary.json"
PLOT_PATH = REPORT_DIR / "pantheon_cov_sweep.png"


def main() -> None:
    print("Loading Pantheon+ rows and covariance...")
    rows, _ = load_rows(RAW_PATH)
    cov = load_covariance(COV_PATH, len(rows))
    if cov is None:
        raise SystemExit("Covariance not available; cannot run sweep.")

    specs = make_specs()
    z_cut = 1.0
    cov_scales = [0.7, 0.85, 1.0, 1.15, 1.3, 1.5]
    lambdas = np.round(np.arange(-0.30, 0.301, 0.01), 6)
    n_null_seeds = 100
    seed_root = 20260426

    rows_out: list[dict] = []
    for s in cov_scales:
        scaled = cov * s
        for spec in specs:
            block = precompute_block(rows, scaled, z_cut, spec.fn)
            fit = actual_data_fit(block, lambdas)

            # Null distribution: noise from sCov, fit assumes sCov.
            L = np.tril(block["cho"][0])
            log_n = math.log(block["n"])
            ones = block["ones"]
            deform = block["deformation"]
            d_p_d = block["d_p_d"]
            d_p_1 = block["d_p_1"]
            null_dbics: list[float] = []
            idx_zero = int(np.argmin(np.abs(lambdas)))
            for sd in range(n_null_seeds):
                rng = np.random.default_rng(seed_root + sd)
                iid = rng.standard_normal(block["n"])
                noise = L @ iid
                q_n = cho_solve(block["cho"], noise, check_finite=False)
                n_p_n = float(noise @ q_n)
                d_p_n = float(deform @ q_n)
                one_p_n = float(ones @ q_n)
                # lambda_inj = 0:
                r_p_r = n_p_n
                r_p_d = d_p_n
                one_p_r = one_p_n
                chi2_grid = chi2_grid_inner(block, r_p_r, r_p_d, one_p_r, lambdas)
                lcdm_chi2 = float(chi2_grid[idx_zero])
                best_idx = int(np.argmin(chi2_grid))
                best_chi2 = float(chi2_grid[best_idx])
                null_dbics.append(best_chi2 - lcdm_chi2 + log_n)

            null_arr = np.array(null_dbics)
            row = {
                "spec": spec.name,
                "p": spec.p if spec.p is not None else "",
                "z_cut": z_cut,
                "cov_scale": s,
                "n": block["n"],
                "actual_best_lambda": fit["best_lambda"],
                "actual_delta_chi2": fit["delta_chi2"],
                "actual_delta_aic": fit["delta_aic"],
                "actual_delta_bic": fit["delta_bic"],
                "null_n_seeds": n_null_seeds,
                "null_median_dbic": float(np.median(null_arr)),
                "null_p10_dbic": float(np.percentile(null_arr, 10)),
                "null_p90_dbic": float(np.percentile(null_arr, 90)),
                "null_min_dbic": float(np.min(null_arr)),
                "null_frac_below_minus_two": float(np.mean(null_arr < -2.0)),
                "gap_actual_to_null_p10": fit["delta_bic"]
                - float(np.percentile(null_arr, 10)),
            }
            rows_out.append(row)

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with SWEEP_PATH.open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)
    SUMMARY_PATH.write_text(
        json.dumps({"sweep": rows_out, "scales": cov_scales, "z_cut": z_cut}, indent=2),
        encoding="utf-8",
    )

    print()
    print(f"Covariance-sensitivity sweep at z_cut = {z_cut}:")
    print("  scale | spec            |  actual_dBIC | null_med | null_p10 |   gap")
    for s in cov_scales:
        for spec in specs:
            r = next(rr for rr in rows_out if rr["cov_scale"] == s and rr["spec"] == spec.name)
            print(
                f"  {s:5.2f} | {spec.name.ljust(14)} | "
                f"{r['actual_delta_bic']:+10.2f} | "
                f"{r['null_median_dbic']:+7.2f} | "
                f"{r['null_p10_dbic']:+7.2f} | "
                f"{r['gap_actual_to_null_p10']:+7.2f}"
            )

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        plt = None
    if plt is not None:
        fig, ax = plt.subplots(1, 1, figsize=(8.0, 4.8), dpi=150)
        colors = {
            "v0_log": "#1d7f8c",
            "v1_pow_p1.8": "#d28f2d",
            "v1_pow_p2.0": "#6f5aa7",
        }
        for spec in specs:
            xs = []
            actual = []
            null_med = []
            null_p10 = []
            null_p90 = []
            for s in cov_scales:
                r = next(rr for rr in rows_out if rr["cov_scale"] == s and rr["spec"] == spec.name)
                xs.append(s)
                actual.append(r["actual_delta_bic"])
                null_med.append(r["null_median_dbic"])
                null_p10.append(r["null_p10_dbic"])
                null_p90.append(r["null_p90_dbic"])
            ax.plot(xs, actual, marker="o", linewidth=1.6, color=colors[spec.name], label=f"{spec.name} actual")
            ax.plot(xs, null_med, marker="s", linewidth=1.0, linestyle="--", color=colors[spec.name], alpha=0.75, label=f"{spec.name} null median")
            ax.fill_between(xs, null_p10, null_p90, color=colors[spec.name], alpha=0.10)
        ax.axhline(-2, color="#9c4638", linewidth=0.9, linestyle=":", label="dBIC = -2")
        ax.set_xlabel("covariance scale s (analyst's chosen rescaling)")
        ax.set_ylabel("Delta BIC at z_cut = 1.0")
        ax.set_title("Covariance-sensitivity sweep: v0 + v1 specs")
        ax.grid(True, alpha=0.22)
        ax.legend(fontsize=8, ncol=2, loc="upper left")
        fig.tight_layout()
        fig.savefig(PLOT_PATH)
        plt.close(fig)

    print()
    print(f"Wrote {SWEEP_PATH}")
    print(f"Wrote {SUMMARY_PATH}")
    if PLOT_PATH.exists():
        print(f"Wrote {PLOT_PATH}")


if __name__ == "__main__":
    main()
