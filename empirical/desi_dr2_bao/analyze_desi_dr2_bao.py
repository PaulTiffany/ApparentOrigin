"""DESI DR2 BAO external-gate analysis for AOC.

This script implements the conservative DESI gate:

* compact DESI DR2 Gaussian BAO mean/covariance inputs,
* full covariance,
* analytic global alpha nuisance fit for every model,
* an Omega_m grid so the LCDM baseline is not fixed to Omega_m=0.3,
* frozen Pantheon+ v0/v1 deformation shapes only.

The result is a baseline-upgraded test of whether Pantheon-amplitude AOC
deformations survive BAO contact under the current observable map.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "desi_dr2_bao"
DERIVED_DIR = ROOT / "data" / "derived" / "desi_dr2_bao"
REPORT_DIR = ROOT / "reports" / "desi_dr2_bao"

MEAN_PATH = RAW_DIR / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
COV_PATH = RAW_DIR / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
TABLE_PATH = DERIVED_DIR / "desi_dr2_bao_all_gccomb_measurements.csv"
PROFILE_PATH = DERIVED_DIR / "desi_dr2_bao_omega_lambda_profile.csv"
SUMMARY_PATH = DERIVED_DIR / "desi_dr2_bao_summary.json"
REPORT_PATH = REPORT_DIR / "desi_dr2_bao_report.md"

C_KM_S = 299792.458
H0 = 70.0
R_D_MPC = 147.09
OMEGA_GRID = np.linspace(0.15, 0.45, 301)
LAMBDA_GRID = np.linspace(-0.35, 0.20, 551)
REFERENCE_OMEGA_M = 0.3


@dataclass(frozen=True)
class BaoPoint:
    index: int
    z: float
    value: float
    quantity: str


@dataclass(frozen=True)
class Shape:
    name: str
    pantheon_reference_lambda: float | None
    g: Callable[[np.ndarray], np.ndarray]
    dg_dz: Callable[[np.ndarray], np.ndarray]


def load_mean(path: Path = MEAN_PATH) -> list[BaoPoint]:
    points: list[BaoPoint] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            z_s, value_s, quantity = stripped.split()
            points.append(
                BaoPoint(
                    index=len(points),
                    z=float(z_s),
                    value=float(value_s),
                    quantity=quantity,
                )
            )
    return points


def load_cov(path: Path = COV_PATH) -> np.ndarray:
    values = [float(token) for token in path.read_text(encoding="utf-8").split()]
    n = int(round(math.sqrt(len(values))))
    if n * n != len(values):
        raise ValueError(f"Covariance has {len(values)} entries; not square.")
    return np.array(values, dtype=float).reshape((n, n))


def e_z_array(z: np.ndarray, omega_m: float) -> np.ndarray:
    return np.sqrt(omega_m * (1.0 + z) ** 3 + (1.0 - omega_m))


@lru_cache(maxsize=None)
def dm_mpc_cached(z: float, omega_m: float) -> float:
    if z == 0.0:
        return 0.0
    grid = np.linspace(0.0, z, 2048)
    integral = np.trapezoid(1.0 / e_z_array(grid, omega_m), grid)
    return (C_KM_S / H0) * float(integral)


def lcdm_prediction(points: list[BaoPoint], omega_m: float) -> np.ndarray:
    out: list[float] = []
    cache: dict[float, tuple[float, float, float]] = {}
    for point in points:
        if point.z not in cache:
            z_arr = np.array([point.z])
            dm_over_rd = dm_mpc_cached(point.z, float(omega_m)) / R_D_MPC
            dh_over_rd = (C_KM_S / (H0 * float(e_z_array(z_arr, omega_m)[0]))) / R_D_MPC
            dv_over_rd = (point.z * dm_over_rd * dm_over_rd * dh_over_rd) ** (1.0 / 3.0)
            cache[point.z] = (dm_over_rd, dh_over_rd, dv_over_rd)
        dm_over_rd, dh_over_rd, dv_over_rd = cache[point.z]
        if point.quantity == "DM_over_rs":
            out.append(dm_over_rd)
        elif point.quantity == "DH_over_rs":
            out.append(dh_over_rd)
        elif point.quantity == "DV_over_rs":
            out.append(dv_over_rd)
        else:
            raise ValueError(f"Unknown BAO quantity: {point.quantity}")
    return np.array(out, dtype=float)


def make_shapes() -> list[Shape]:
    return [
        Shape(
            name="v0_log",
            pantheon_reference_lambda=-0.13,
            g=lambda z: np.log1p(z / 0.8),
            dg_dz=lambda z: 1.0 / (z + 0.8),
        ),
        Shape(
            name="v1_pow_p1.8",
            pantheon_reference_lambda=-0.150,
            g=lambda z: (1.0 + z) ** 0.8,
            dg_dz=lambda z: 0.8 * (1.0 + z) ** -0.2,
        ),
        Shape(
            name="v1_pow_p2.0",
            pantheon_reference_lambda=-0.110,
            g=lambda z: 1.0 + z,
            dg_dz=lambda z: np.ones_like(z, dtype=float),
        ),
    ]


def aoc_prediction(
    points: list[BaoPoint],
    shape: Shape,
    lambda_k: float,
    mapping: str,
    omega_m: float,
) -> np.ndarray:
    out: list[float] = []
    cache: dict[float, tuple[float, float, float]] = {}
    log10_over_5 = math.log(10.0) / 5.0
    for point in points:
        if point.z not in cache:
            z_arr = np.array([point.z], dtype=float)
            dm_base = dm_mpc_cached(point.z, float(omega_m)) / R_D_MPC
            dh_base = (C_KM_S / (H0 * float(e_z_array(z_arr, omega_m)[0]))) / R_D_MPC
            g_val = float(shape.g(z_arr)[0])
            dg_val = float(shape.dg_dz(z_arr)[0])
            scale = math.exp(log10_over_5 * lambda_k * g_val)
            dscale_dz = scale * log10_over_5 * lambda_k * dg_val
            dm_new = dm_base * scale
            if mapping == "derivative_dm":
                dh_new = dh_base * scale + dm_base * dscale_dz
            elif mapping == "isotropic_scale":
                dh_new = dh_base * scale
            else:
                raise ValueError(f"Unknown mapping: {mapping}")
            dv_new = (point.z * dm_new * dm_new * dh_new) ** (1.0 / 3.0)
            cache[point.z] = (dm_new, dh_new, dv_new)
        dm_new, dh_new, dv_new = cache[point.z]
        if point.quantity == "DM_over_rs":
            out.append(dm_new)
        elif point.quantity == "DH_over_rs":
            out.append(dh_new)
        elif point.quantity == "DV_over_rs":
            out.append(dv_new)
        else:
            raise ValueError(f"Unknown BAO quantity: {point.quantity}")
    return np.array(out, dtype=float)


def fit_alpha_chi2(y: np.ndarray, pred: np.ndarray, cov_inv: np.ndarray) -> tuple[float, float]:
    numerator = float(pred @ cov_inv @ y)
    denominator = float(pred @ cov_inv @ pred)
    alpha = numerator / denominator
    resid = y - alpha * pred
    chi2 = float(resid @ cov_inv @ resid)
    return alpha, chi2


def normalize_table(points: list[BaoPoint], cov: np.ndarray) -> None:
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "z", "quantity", "value", "sigma"],
        )
        writer.writeheader()
        for point in points:
            writer.writerow(
                {
                    "index": point.index,
                    "z": f"{point.z:.8g}",
                    "quantity": point.quantity,
                    "value": f"{point.value:.12g}",
                    "sigma": f"{math.sqrt(cov[point.index, point.index]):.12g}",
                }
            )


def classify(best_lambda: float, reference_lambda: float | None) -> str:
    if reference_lambda is None:
        return "no_reference"
    if abs(best_lambda) < 0.025:
        return "desi_prefers_near_zero"
    if best_lambda * reference_lambda < 0:
        return "opposite_direction"
    ratio = abs(best_lambda / reference_lambda)
    if 0.5 <= ratio <= 1.5:
        return "compatible_magnitude"
    return "same_direction_different_magnitude"


def fit_lcdm_grid(
    points: list[BaoPoint],
    y: np.ndarray,
    cov_inv: np.ndarray,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    profile: list[dict[str, object]] = []
    for omega_m in OMEGA_GRID:
        pred = lcdm_prediction(points, float(omega_m))
        alpha, chi2 = fit_alpha_chi2(y, pred, cov_inv)
        profile.append(
            {
                "omega_m": float(omega_m),
                "alpha": alpha,
                "chi2": chi2,
            }
        )
    best = min(profile, key=lambda row: float(row["chi2"]))
    baseline = {
        "model": "flat_lcdm",
        "omega_m": best["omega_m"],
        "alpha": best["alpha"],
        "chi2": best["chi2"],
        "reference_omega_m_chi2": min(
            profile, key=lambda row: abs(float(row["omega_m"]) - REFERENCE_OMEGA_M)
        )["chi2"],
    }
    return baseline, profile


def fit_aoc_grid(
    points: list[BaoPoint],
    y: np.ndarray,
    cov_inv: np.ndarray,
    baseline_chi2: float,
    shape: Shape,
    mapping: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    omega_profile: list[dict[str, object]] = []
    best_row: dict[str, object] | None = None
    ref_best: dict[str, object] | None = None

    for omega_m in OMEGA_GRID:
        omega_best: dict[str, object] | None = None
        for lambda_k in LAMBDA_GRID:
            pred = aoc_prediction(points, shape, float(lambda_k), mapping, float(omega_m))
            if not np.all(np.isfinite(pred)):
                continue
            alpha, chi2 = fit_alpha_chi2(y, pred, cov_inv)
            row = {
                "omega_m": float(omega_m),
                "lambda_k": float(lambda_k),
                "alpha": alpha,
                "chi2": chi2,
                "delta_chi2_vs_lcdm_grid": chi2 - baseline_chi2,
            }
            if omega_best is None or chi2 < float(omega_best["chi2"]):
                omega_best = row
            if best_row is None or chi2 < float(best_row["chi2"]):
                best_row = row
            ref = shape.pantheon_reference_lambda
            if ref is not None and abs(float(lambda_k) - ref) < 5e-4:
                if ref_best is None or chi2 < float(ref_best["chi2"]):
                    ref_best = row
        if omega_best is None:
            raise RuntimeError(f"No finite rows for {shape.name} {mapping} at {omega_m}.")
        omega_profile.append(omega_best)

    if best_row is None:
        raise RuntimeError(f"No finite rows for {shape.name} {mapping}.")

    best = {
        "model": shape.name,
        "mapping": mapping,
        "best_omega_m": best_row["omega_m"],
        "best_lambda": best_row["lambda_k"],
        "pantheon_reference_lambda": shape.pantheon_reference_lambda,
        "best_alpha": best_row["alpha"],
        "best_chi2": best_row["chi2"],
        "best_delta_chi2_vs_lcdm_grid": best_row["delta_chi2_vs_lcdm_grid"],
        "best_delta_aic_vs_lcdm_grid": best_row["delta_chi2_vs_lcdm_grid"] + 2.0,
        "best_delta_bic_vs_lcdm_grid": best_row["delta_chi2_vs_lcdm_grid"] + math.log(len(points)),
        "best_classification": classify(
            float(best_row["lambda_k"]), shape.pantheon_reference_lambda
        ),
        "pantheon_reference_best_omega_m": None if ref_best is None else ref_best["omega_m"],
        "pantheon_reference_chi2": None if ref_best is None else ref_best["chi2"],
        "pantheon_reference_delta_chi2_vs_lcdm_grid": None
        if ref_best is None
        else ref_best["delta_chi2_vs_lcdm_grid"],
    }
    return best, omega_profile


def run_subset(
    subset_name: str,
    subset_indices: list[int],
    all_points: list[BaoPoint],
    all_cov: np.ndarray,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    points = [all_points[idx] for idx in subset_indices]
    cov = all_cov[np.ix_(subset_indices, subset_indices)]
    y = np.array([point.value for point in points], dtype=float)
    cov_inv = np.linalg.inv(cov)

    baseline, lcdm_profile = fit_lcdm_grid(points, y, cov_inv)
    baseline["subset"] = subset_name
    baseline["n_points"] = len(points)
    baseline["alpha_fitted"] = True
    baseline["omega_m_grid"] = [float(OMEGA_GRID[0]), float(OMEGA_GRID[-1]), len(OMEGA_GRID)]
    baseline["h0"] = H0
    baseline["r_d_mpc"] = R_D_MPC

    profile_rows = [
        {
            "subset": subset_name,
            "model": "flat_lcdm",
            "mapping": "none",
            "omega_m": row["omega_m"],
            "best_lambda": "",
            "alpha": row["alpha"],
            "chi2": row["chi2"],
            "delta_chi2_vs_lcdm_grid": float(row["chi2"]) - float(baseline["chi2"]),
            "classification": "baseline_profile",
        }
        for row in lcdm_profile
    ]

    best_by_model: list[dict[str, object]] = []
    for shape in make_shapes():
        for mapping in ["derivative_dm", "isotropic_scale"]:
            best, omega_profile = fit_aoc_grid(
                points, y, cov_inv, float(baseline["chi2"]), shape, mapping
            )
            best["subset"] = subset_name
            best["n_points"] = len(points)
            best_by_model.append(best)
            for row in omega_profile:
                profile_rows.append(
                    {
                        "subset": subset_name,
                        "model": shape.name,
                        "mapping": mapping,
                        "omega_m": row["omega_m"],
                        "best_lambda": row["lambda_k"],
                        "alpha": row["alpha"],
                        "chi2": row["chi2"],
                        "delta_chi2_vs_lcdm_grid": row["delta_chi2_vs_lcdm_grid"],
                        "classification": classify(
                            float(row["lambda_k"]), shape.pantheon_reference_lambda
                        ),
                    }
                )
    return baseline, best_by_model, profile_rows


def main() -> None:
    points = load_mean()
    cov = load_cov()
    if cov.shape != (len(points), len(points)):
        raise SystemExit(
            f"Mean/covariance mismatch: {len(points)} points, covariance {cov.shape}."
        )
    normalize_table(points, cov)

    subsets = {
        "all": list(range(len(points))),
        "galaxy_no_lya": [idx for idx, point in enumerate(points) if point.z < 2.0],
        "pantheon_overlap_z_le_1": [
            idx for idx, point in enumerate(points) if point.z <= 1.0
        ],
    }
    baselines: list[dict[str, object]] = []
    best_by_model: list[dict[str, object]] = []
    profile_rows: list[dict[str, object]] = []
    for subset_name, subset_indices in subsets.items():
        baseline, subset_best, subset_profile = run_subset(
            subset_name, subset_indices, points, cov
        )
        baselines.append(baseline)
        best_by_model.extend(subset_best)
        profile_rows.extend(subset_profile)

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    with PROFILE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "subset",
                "model",
                "mapping",
                "omega_m",
                "best_lambda",
                "alpha",
                "chi2",
                "delta_chi2_vs_lcdm_grid",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(profile_rows)

    summary = {
        "status": "baseline_upgraded_first_pass",
        "n_points": len(points),
        "subsets": list(subsets.keys()),
        "baselines": baselines,
        "covariance": {
            "path": str(COV_PATH.relative_to(ROOT)),
            "shape": list(cov.shape),
            "condition_number": float(np.linalg.cond(cov)),
        },
        "grids": {
            "omega_m": [float(OMEGA_GRID[0]), float(OMEGA_GRID[-1]), len(OMEGA_GRID)],
            "lambda_k": [float(LAMBDA_GRID[0]), float(LAMBDA_GRID[-1]), len(LAMBDA_GRID)],
        },
        "best_by_model": best_by_model,
        "allowed_claim": (
            "This is a DESI DR2 BAO external-gate calculation with Omega_m grid "
            "freedom and a global alpha nuisance scale. It can reject, tolerate, "
            "or weakly prefer a frozen AOC observable map; it cannot confirm AOC."
        ),
        "forbidden_claims": [
            "DESI confirms AOC.",
            "AOC explains evolving dark energy.",
            "AOC explains the Hubble tension.",
            "This first-pass BAO projection is the final AOC temporalization map.",
        ],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(summary)

    print(f"Normalized DESI table: {TABLE_PATH}")
    print(f"Omega/lambda profile: {PROFILE_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    print(f"Report: {REPORT_PATH}")
    for baseline in baselines:
        print(
            f"{baseline['subset']} LCDM chi2={float(baseline['chi2']):.3f}, "
            f"omega_m={float(baseline['omega_m']):.3f}, "
            f"alpha={float(baseline['alpha']):.5f}"
        )
    for row in best_by_model:
        print(
            f"{row['subset']} {row['model']} {row['mapping']}: "
            f"best_lambda={float(row['best_lambda']):+.3f}, "
            f"omega_m={float(row['best_omega_m']):.3f}, "
            f"delta_chi2={float(row['best_delta_chi2_vs_lcdm_grid']):+.3f}, "
            f"delta_bic={float(row['best_delta_bic_vs_lcdm_grid']):+.3f}, "
            f"class={row['best_classification']}"
        )


def write_report(summary: dict[str, object]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    baselines = summary["baselines"]
    assert isinstance(baselines, list)
    rows = summary["best_by_model"]
    assert isinstance(rows, list)

    lines = [
        "# DESI DR2 BAO Baseline-Upgraded AOC Gate",
        "",
        "Status: baseline-upgraded exploratory gate.",
        "",
        "This report uses the compact DESI DR2 Gaussian BAO likelihood input",
        "files from the Cobaya BAO data repository linked by the official DESI",
        "DR2 cosmology products page. It fits a global `alpha` scale for every",
        "model and now grids over `Omega_m`, so the comparison is about",
        "redshift-dependent shape after a stronger `LambdaCDM` baseline.",
        "",
        "## Baseline",
        "",
        "| Subset | Points | Best Omega_m | Fitted alpha | Baseline chi2 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for baseline_obj in baselines:
        baseline = dict(baseline_obj)
        lines.append(
            f"| {baseline['subset']} | {baseline['n_points']} | "
            f"{float(baseline['omega_m']):.3f} | {float(baseline['alpha']):.6f} | "
            f"{float(baseline['chi2']):.6f} |"
        )
    lines.extend(
        [
            "",
            f"Baseline cosmology: flat `LambdaCDM`, `H0={H0}`, `r_d={R_D_MPC} Mpc`,",
            f"`Omega_m` grid `{OMEGA_GRID[0]:.2f}` to `{OMEGA_GRID[-1]:.2f}`;",
            "each subset fits its own global `alpha`.",
            "",
            "## AOC Shape Gate",
            "",
            "| Subset | Shape | Mapping | Best Omega_m | Best lambda | Pantheon ref | Delta chi2 | Delta BIC | Classification | Ref delta chi2 |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |",
        ]
    )
    for row_obj in rows:
        row = dict(row_obj)
        ref = row["pantheon_reference_lambda"]
        ref_delta = row["pantheon_reference_delta_chi2_vs_lcdm_grid"]
        lines.append(
            "| {subset} | {model} | {mapping} | {omega:.3f} | {best:+.3f} | {ref} | {delta:+.3f} | {bic:+.3f} | {cls} | {ref_delta} |".format(
                subset=row["subset"],
                model=row["model"],
                mapping=row["mapping"],
                omega=float(row["best_omega_m"]),
                best=float(row["best_lambda"]),
                ref="n/a" if ref is None else f"{float(ref):+.3f}",
                delta=float(row["best_delta_chi2_vs_lcdm_grid"]),
                bic=float(row["best_delta_bic_vs_lcdm_grid"]),
                cls=row["best_classification"],
                ref_delta="n/a" if ref_delta is None else f"{float(ref_delta):+.3f}",
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is still not a confirmation test. The correct read is whether a",
            "Pantheon+-motivated deformation survives contact with a non-supernova",
            "ruler under a predeclared map after giving the `LambdaCDM` baseline",
            "basic `Omega_m` freedom.",
            "",
            "The subset split is part of the control discipline. `all` includes",
            "Ly-alpha at `z=2.33`; `galaxy_no_lya` removes that extrapolation;",
            "`pantheon_overlap_z_le_1` restricts DESI to the redshift range closest",
            "to the Pantheon+ deformation fit.",
            "",
            "Current read: compare the best `lambda_K` and penalized statistics",
            "against the Pantheon reference amplitudes. Any result that improves",
            "`chi2` but not BIC is treated as insufficient shape evidence.",
            "",
            "In the baseline-upgraded run, the `isotropic_scale` sensitivity map",
            "continues to prefer near-zero deformation. The `derivative_dm` map",
            "can improve chi2 in subsets only by flipping sign relative to the",
            "Pantheon+ deformation direction and, in some cases, by moving",
            "`Omega_m` to the upper grid edge. This is not evidence for",
            "Pantheon-amplitude portability.",
            "",
            "Allowed claim:",
            "",
            "> DESI DR2 BAO now has a baseline-upgraded external gate for the",
            "> frozen AOC observable maps.",
            "",
            "Forbidden claim:",
            "",
            "> DESI confirms AOC, explains dark energy evolution, or solves the",
            "> Hubble tension.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
