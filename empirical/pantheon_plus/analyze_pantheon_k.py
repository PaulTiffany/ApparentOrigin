"""Compute a provisional apparatus-bound K from Pantheon+ distances.

This is an empirical interface test, not a cosmological model fit. It defines
K_P as the largest observed y=1+z value whose distance-modulus uncertainty
passes a chosen threshold.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES.dat"
COV_PATH = ROOT / "data" / "raw" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
DERIVED_DIR = ROOT / "data" / "derived" / "pantheon_plus"
REPORT_DIR = ROOT / "reports" / "pantheon_plus"
SUMMARY_PATH = DERIVED_DIR / "pantheon_k_summary.json"
BINS_PATH = DERIVED_DIR / "pantheon_k_bins.csv"
REPORT_PATH = REPORT_DIR / "pantheon_k_report.md"
PLOT_PATH = REPORT_DIR / "pantheon_k_uncertainty.png"
SWEEP_PATH = DERIVED_DIR / "pantheon_k_threshold_sweep.csv"
RESIDUALS_PATH = DERIVED_DIR / "pantheon_lcdm_residual_bins.csv"
COV_SUMMARY_PATH = DERIVED_DIR / "pantheon_covariance_summary.json"
COV_K_SWEEP_PATH = DERIVED_DIR / "pantheon_covariance_diag_k_sweep.csv"
DISCRIMINABILITY_PATH = DERIVED_DIR / "pantheon_model_discriminability.csv"
AOC_DEFORMATION_PATH = DERIVED_DIR / "pantheon_aoc_threshold_deformation.csv"
AOC_HOLDOUT_PATH = DERIVED_DIR / "pantheon_aoc_holdout_validation.csv"
AOC_SPLIT_ROBUSTNESS_PATH = DERIVED_DIR / "pantheon_aoc_split_robustness.csv"
DISCRIMINABILITY_PLOT_PATH = REPORT_DIR / "pantheon_model_discriminability.png"
AOC_DEFORMATION_PLOT_PATH = REPORT_DIR / "pantheon_aoc_threshold_deformation.png"
AOC_HOLDOUT_PLOT_PATH = REPORT_DIR / "pantheon_aoc_holdout_validation.png"
AOC_SPLIT_ROBUSTNESS_PLOT_PATH = REPORT_DIR / "pantheon_aoc_split_robustness.png"
SWEEP_PLOT_PATH = REPORT_DIR / "pantheon_k_threshold_sweep.png"
RESIDUAL_PLOT_PATH = REPORT_DIR / "pantheon_lcdm_residuals.png"


Z_CANDIDATES = ["zHD", "zCMB", "zHEL", "zcmb", "zhel", "z"]
CID_CANDIDATES = ["CID", "cid", "SNID", "snid", "name"]
MU_CANDIDATES = ["MU_SH0ES", "MU", "mu"]
MU_ERR_CANDIDATES = [
    "MU_SH0ES_ERR_DIAG",
    "MUERR",
    "MU_ERR",
    "m_b_corr_err_DIAG",
    "mBERR",
]


@dataclass(frozen=True)
class PantheonRow:
    index: int
    cid: str
    z: float
    y: float
    mu: float | None
    mu_err: float


@dataclass(frozen=True)
class FlatLambdaCDM:
    h0: float = 70.0
    omega_m: float = 0.3

    @property
    def omega_lambda(self) -> float:
        return 1.0 - self.omega_m


def _first_existing(fieldnames: list[str], candidates: list[str]) -> str:
    lower_lookup = {name.lower(): name for name in fieldnames}
    for candidate in candidates:
        if candidate in fieldnames:
            return candidate
        if candidate.lower() in lower_lookup:
            return lower_lookup[candidate.lower()]
    raise KeyError(f"None of these columns were found: {candidates}. Available: {fieldnames}")


def load_rows(path: Path) -> tuple[list[PantheonRow], dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run empirical\\pantheon_plus\\download_pantheon_plus.py first."
        )

    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter=" ", skipinitialspace=True)
        fieldnames = reader.fieldnames or []
        z_col = _first_existing(fieldnames, Z_CANDIDATES)
        mu_err_col = _first_existing(fieldnames, MU_ERR_CANDIDATES)
        try:
            cid_col = _first_existing(fieldnames, CID_CANDIDATES)
        except KeyError:
            cid_col = ""
        try:
            mu_col = _first_existing(fieldnames, MU_CANDIDATES)
        except KeyError:
            mu_col = ""

        rows: list[PantheonRow] = []
        for raw in reader:
            try:
                z = float(raw[z_col])
                mu_err = float(raw[mu_err_col])
                mu = float(raw[mu_col]) if mu_col else None
            except (TypeError, ValueError):
                continue
            if z <= 0 or mu_err <= 0 or not math.isfinite(z) or not math.isfinite(mu_err):
                continue
            row_index = len(rows)
            cid = str(raw.get(cid_col) or f"row-{row_index}") if cid_col else f"row-{row_index}"
            rows.append(PantheonRow(index=row_index, cid=cid, z=z, y=1.0 + z, mu=mu, mu_err=mu_err))

    return rows, {"cid": cid_col, "z": z_col, "mu": mu_col, "mu_err": mu_err_col}


def load_covariance(path: Path, expected_n: int):
    """Load Pantheon covariance matrix with flexible first-value handling."""

    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for covariance-aware analysis") from exc

    if not path.exists():
        return None

    values = np.loadtxt(path)
    flat = values.reshape(-1)
    if flat.size == expected_n * expected_n:
        return flat.reshape((expected_n, expected_n))
    if flat.size == expected_n * expected_n + 1 and int(round(float(flat[0]))) == expected_n:
        return flat[1:].reshape((expected_n, expected_n))
    raise ValueError(
        f"Unexpected covariance size {flat.size}; expected {expected_n ** 2} or {expected_n ** 2 + 1}"
    )


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[int(pos)]
    weight = pos - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def summarize(rows: list[PantheonRow], columns: dict[str, str], mu_err_max: float = 0.20) -> dict[str, object]:
    passing = [row for row in rows if row.mu_err <= mu_err_max]
    if not passing:
        raise ValueError(f"No rows pass mu_err_max={mu_err_max}")

    max_row = max(passing, key=lambda row: row.y)
    mu_err_values = [row.mu_err for row in rows]
    z_values = [row.z for row in rows]

    return {
        "contract": "Pantheon+ provisional apparatus-bound K",
        "allowed_claim": "AOC's K formalism can be computed on a real supernova distance dataset.",
        "forbidden_claim": "AOC explains cosmic acceleration.",
        "columns": columns,
        "n_rows": len(rows),
        "mu_err_max": mu_err_max,
        "n_passing": len(passing),
        "K_P": max_row.y,
        "z_at_K_P": max_row.z,
        "mu_err_at_K_P": max_row.mu_err,
        "z_min": min(z_values),
        "z_max": max(z_values),
        "mu_err_median": quantile(mu_err_values, 0.50),
        "mu_err_p90": quantile(mu_err_values, 0.90),
        "mu_err_p95": quantile(mu_err_values, 0.95),
        "interpretation": (
            "K_P is the largest observed 1+z value passing the provisional "
            "distance-modulus uncertainty threshold. This is a pipeline dynamic-range "
            "estimate, not a cosmological claim."
        ),
    }


def e_z(z: float, cosmology: FlatLambdaCDM) -> float:
    return math.sqrt(cosmology.omega_m * (1.0 + z) ** 3 + cosmology.omega_lambda)


def luminosity_distance_mpc(z: float, cosmology: FlatLambdaCDM, steps: int = 900) -> float:
    """Return flat-LambdaCDM luminosity distance in Mpc via Simpson integration."""

    if z <= 0:
        return 0.0
    if steps % 2:
        steps += 1
    dz = z / steps
    total = 1.0 / e_z(0.0, cosmology) + 1.0 / e_z(z, cosmology)
    for idx in range(1, steps):
        coeff = 4.0 if idx % 2 else 2.0
        total += coeff / e_z(idx * dz, cosmology)
    c_km_s = 299_792.458
    comoving = (c_km_s / cosmology.h0) * (dz / 3.0) * total
    return (1.0 + z) * comoving


def distance_modulus_lcdm(z: float, cosmology: FlatLambdaCDM) -> float:
    d_l = luminosity_distance_mpc(z, cosmology)
    if d_l <= 0:
        return float("nan")
    return 5.0 * math.log10(d_l) + 25.0


def distance_modulus_coasting(z: float, h0: float = 70.0) -> float:
    """Return a simple coasting-universe luminosity distance baseline.

    This is used as a comparison instrument only. It is not an AOC model.
    """

    c_km_s = 299_792.458
    if z <= 0:
        return float("nan")
    d_l = (c_km_s / h0) * (1.0 + z) * math.log1p(z)
    return 5.0 * math.log10(d_l) + 25.0


def distance_modulus_low_z_linear(z: float, h0: float = 70.0) -> float:
    """Return the low-z linear Hubble law extended beyond its valid regime."""

    c_km_s = 299_792.458
    if z <= 0:
        return float("nan")
    d_l = (c_km_s / h0) * z
    return 5.0 * math.log10(d_l) + 25.0


def distance_modulus_aoc_threshold(
    z: float,
    lambda_threshold: float,
    z_star: float = 0.8,
    cosmology: FlatLambdaCDM = FlatLambdaCDM(),
) -> float:
    """Return a minimal AOC-style threshold deformation of flat LambdaCDM.

    The deformation is intentionally conservative and phenomenological:

        mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)

    lambda=0 recovers the baseline exactly. Positive lambda makes high-z
    distances dimmer; negative lambda makes them brighter. This is not claimed
    as the final AOC distance law. It is a one-parameter threshold deformation
    used to test whether the empirical contract can evaluate AOC-motivated
    operators.
    """

    return distance_modulus_lcdm(z, cosmology) + lambda_threshold * math.log1p(z / z_star)


def build_threshold_sweep(rows: list[PantheonRow], thresholds: list[float] | None = None) -> list[dict[str, float | int]]:
    if thresholds is None:
        thresholds = [0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30, 0.35, 0.40]

    sweep: list[dict[str, float | int]] = []
    for threshold in thresholds:
        passing = [row for row in rows if row.mu_err <= threshold]
        if not passing:
            sweep.append({"mu_err_max": threshold, "n_passing": 0, "K_P": float("nan"), "z_at_K_P": float("nan")})
            continue
        max_row = max(passing, key=lambda row: row.y)
        sweep.append(
            {
                "mu_err_max": threshold,
                "n_passing": len(passing),
                "K_P": max_row.y,
                "z_at_K_P": max_row.z,
                "mu_err_at_K_P": max_row.mu_err,
            }
        )
    return sweep


def build_covariance_diag_k_sweep(
    rows: list[PantheonRow],
    cov,
    thresholds: list[float] | None = None,
) -> list[dict[str, float | int]]:
    try:
        import numpy as np
    except ImportError:
        return []
    if cov is None:
        return []
    if thresholds is None:
        thresholds = [0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30, 0.35, 0.40]

    diag_sigma = np.sqrt(np.diag(cov))
    sweep: list[dict[str, float | int]] = []
    for threshold in thresholds:
        passing_indices = [idx for idx, sigma in enumerate(diag_sigma) if float(sigma) <= threshold]
        if not passing_indices:
            sweep.append({"mu_err_max": threshold, "n_passing": 0, "K_P": float("nan"), "z_at_K_P": float("nan")})
            continue
        best_idx = max(passing_indices, key=lambda idx: rows[idx].y)
        sweep.append(
            {
                "mu_err_max": threshold,
                "n_passing": len(passing_indices),
                "K_P": rows[best_idx].y,
                "z_at_K_P": rows[best_idx].z,
                "cov_diag_sigma_at_K_P": float(diag_sigma[best_idx]),
            }
        )
    return sweep


def build_lcdm_residual_bins(
    rows: list[PantheonRow],
    cosmology: FlatLambdaCDM = FlatLambdaCDM(),
    n_bins: int = 12,
) -> list[dict[str, float | int]]:
    usable = [row for row in rows if row.mu is not None]
    z_min = min(row.z for row in usable)
    z_max = max(row.z for row in usable)
    width = (z_max - z_min) / n_bins
    residual_rows = [
        {
            "z": row.z,
            "residual": row.mu - distance_modulus_lcdm(row.z, cosmology),  # type: ignore[operator]
            "pull": (row.mu - distance_modulus_lcdm(row.z, cosmology)) / row.mu_err,  # type: ignore[operator]
        }
        for row in usable
    ]

    bins: list[dict[str, float | int]] = []
    for idx in range(n_bins):
        lo = z_min + idx * width
        hi = z_min + (idx + 1) * width if idx < n_bins - 1 else z_max + 1e-12
        members = [row for row in residual_rows if lo <= row["z"] < hi]
        if not members:
            bins.append(
                {
                    "bin": idx,
                    "z_lo": lo,
                    "z_hi": hi,
                    "n": 0,
                    "median_residual": float("nan"),
                    "median_pull": float("nan"),
                }
            )
            continue
        residuals = [float(row["residual"]) for row in members]
        pulls = [float(row["pull"]) for row in members]
        bins.append(
            {
                "bin": idx,
                "z_lo": lo,
                "z_hi": hi,
                "n": len(members),
                "median_residual": quantile(residuals, 0.50),
                "p10_residual": quantile(residuals, 0.10),
                "p90_residual": quantile(residuals, 0.90),
                "median_pull": quantile(pulls, 0.50),
            }
        )
    return bins


def covariance_summary(rows: list[PantheonRow], cov) -> dict[str, object]:
    """Return diagonal and covariance-aware residual diagnostics."""

    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for covariance-aware analysis") from exc

    if cov is None:
        return {
            "available": False,
            "interpretation": "Covariance file not available; covariance-aware diagnostics skipped.",
        }

    usable_mu = np.array([row.mu if row.mu is not None else np.nan for row in rows], dtype=float)
    if np.isnan(usable_mu).any():
        return {
            "available": False,
            "interpretation": "Some rows lack distance modulus; covariance-aware diagnostics skipped.",
        }

    table_sigma = np.array([row.mu_err for row in rows], dtype=float)
    cov_diag_sigma = np.sqrt(np.diag(cov))
    diag_delta = cov_diag_sigma - table_sigma

    cosmology = FlatLambdaCDM()
    theory = np.array([distance_modulus_lcdm(row.z, cosmology) for row in rows], dtype=float)
    residual = usable_mu - theory
    ones = np.ones_like(residual)

    # Marginalize/calibrate a constant magnitude offset against the covariance.
    cov_jitter = cov + np.eye(cov.shape[0]) * 1e-10
    solved_residual = np.linalg.solve(cov_jitter, residual)
    solved_ones = np.linalg.solve(cov_jitter, ones)
    offset = float((ones @ solved_residual) / (ones @ solved_ones))
    centered = residual - offset * ones
    solved_centered = np.linalg.solve(cov_jitter, centered)
    chi2 = float(centered @ solved_centered)
    dof = int(len(rows) - 1)

    return {
        "available": True,
        "covariance_shape": list(cov.shape),
        "table_sigma_column": "MU_SH0ES_ERR_DIAG",
        "diag_sigma_median": float(np.median(cov_diag_sigma)),
        "table_sigma_median": float(np.median(table_sigma)),
        "diag_minus_table_sigma_median": float(np.median(diag_delta)),
        "diag_minus_table_sigma_max_abs": float(np.max(np.abs(diag_delta))),
        "baseline": "flat LambdaCDM, H0=70, Omega_m=0.3, constant magnitude offset marginalized",
        "marginalized_offset_mag": offset,
        "chi2_after_offset": chi2,
        "dof_after_offset": dof,
        "chi2_per_dof_after_offset": chi2 / dof,
        "interpretation": (
            "This is a covariance-aware baseline residual diagnostic, not a fit. "
            "The constant offset absorbs calibration/H0-like magnitude shifts."
        ),
    }


def chi2_with_offset(residual, cov):
    """Return chi2 after marginalizing a constant offset."""

    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for covariance-aware analysis") from exc

    ones = np.ones_like(residual)
    cov_jitter = cov + np.eye(cov.shape[0]) * 1e-10
    solved_residual = np.linalg.solve(cov_jitter, residual)
    solved_ones = np.linalg.solve(cov_jitter, ones)
    offset = float((ones @ solved_residual) / (ones @ solved_ones))
    centered = residual - offset * ones
    solved_centered = np.linalg.solve(cov_jitter, centered)
    chi2 = float(centered @ solved_centered)
    return chi2, offset


def aoc_threshold_grid_chi2(
    rows: list[PantheonRow],
    cov,
    subset: list[int],
    lambdas: list[float],
):
    """Evaluate the threshold deformation over a lambda grid with one solve.

    For fixed cosmology, the deformation is linear in `lambda` and the nuisance
    magnitude offset is also linear. The covariance solve can therefore be
    shared across the whole grid for a given subset.
    """

    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for covariance-aware analysis") from exc

    cosmology = FlatLambdaCDM()
    obs = np.array([rows[idx].mu for idx in subset], dtype=float)
    subcov = cov[np.ix_(subset, subset)]
    lcdm_theory = np.array([distance_modulus_lcdm(rows[idx].z, cosmology) for idx in subset], dtype=float)
    deformation = np.array([math.log1p(rows[idx].z / 0.8) for idx in subset], dtype=float)
    residual = obs - lcdm_theory
    ones = np.ones_like(residual)

    cov_jitter = subcov + np.eye(subcov.shape[0]) * 1e-10
    solved = np.linalg.solve(cov_jitter, np.column_stack([residual, deformation, ones]))
    p_residual = solved[:, 0]
    p_deformation = solved[:, 1]
    p_ones = solved[:, 2]

    one_p_one = float(ones @ p_ones)
    one_p_residual = float(ones @ p_residual)
    one_p_deformation = float(ones @ p_deformation)
    residual_p_residual = float(residual @ p_residual)
    residual_p_deformation = float(residual @ p_deformation)
    deformation_p_deformation = float(deformation @ p_deformation)

    lcdm_offset = one_p_residual / one_p_one
    lcdm_chi2 = residual_p_residual - (one_p_residual * one_p_residual / one_p_one)
    evaluations = []
    for lam in lambdas:
        v_p_v = (
            residual_p_residual
            - 2.0 * lam * residual_p_deformation
            + lam * lam * deformation_p_deformation
        )
        one_p_v = one_p_residual - lam * one_p_deformation
        offset = one_p_v / one_p_one
        chi2 = v_p_v - (one_p_v * one_p_v / one_p_one)
        evaluations.append((lam, float(chi2), float(offset)))

    return float(lcdm_chi2), float(lcdm_offset), evaluations


def build_model_discriminability(rows: list[PantheonRow], cov) -> list[dict[str, float | int | str]]:
    """Compare simple distance curves over increasing redshift cutoffs.

    The statistic is delta chi2 against a fixed flat-LambdaCDM baseline after
    marginalizing a constant magnitude offset separately for each model and
    cutoff. Larger positive delta chi2 means the alternative is more strongly
    disfavored by the data subset.
    """

    try:
        import numpy as np
    except ImportError:
        return []
    if cov is None:
        return []

    usable_indices = [idx for idx, row in enumerate(rows) if row.mu is not None]
    cutoffs = [0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50]
    alternatives = [
        ("coasting", lambda z: distance_modulus_coasting(z)),
        ("linear_low_z", lambda z: distance_modulus_low_z_linear(z)),
    ]
    lcdm = FlatLambdaCDM()
    out: list[dict[str, float | int | str]] = []

    for cutoff in cutoffs:
        subset = [idx for idx in usable_indices if rows[idx].z <= cutoff]
        if len(subset) < 3:
            continue
        obs = np.array([rows[idx].mu for idx in subset], dtype=float)
        subcov = cov[np.ix_(subset, subset)]
        lcdm_theory = np.array([distance_modulus_lcdm(rows[idx].z, lcdm) for idx in subset], dtype=float)
        lcdm_chi2, lcdm_offset = chi2_with_offset(obs - lcdm_theory, subcov)
        for name, fn in alternatives:
            alt_theory = np.array([fn(rows[idx].z) for idx in subset], dtype=float)
            alt_chi2, alt_offset = chi2_with_offset(obs - alt_theory, subcov)
            delta = alt_chi2 - lcdm_chi2
            out.append(
                {
                    "alternative": name,
                    "z_cut": cutoff,
                    "K_cut": 1.0 + cutoff,
                    "n": len(subset),
                    "lcdm_chi2": lcdm_chi2,
                    "lcdm_offset": lcdm_offset,
                    "alt_chi2": alt_chi2,
                    "alt_offset": alt_offset,
                    "delta_chi2_alt_minus_lcdm": delta,
                    "delta_chi2_per_dof": delta / max(1, len(subset) - 1),
                }
            )
    return out


def build_aoc_threshold_deformation(rows: list[PantheonRow], cov) -> list[dict[str, float | int]]:
    """Grid-search a one-parameter AOC-style threshold deformation."""

    try:
        import numpy as np
    except ImportError:
        return []
    if cov is None:
        return []

    usable_indices = [idx for idx, row in enumerate(rows) if row.mu is not None]
    cutoffs = [0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50]
    lambdas = [round(-0.3 + 0.01 * idx, 6) for idx in range(61)]
    out: list[dict[str, float | int]] = []

    for cutoff in cutoffs:
        subset = [idx for idx in usable_indices if rows[idx].z <= cutoff]
        if len(subset) < 3:
            continue
        lcdm_chi2, lcdm_offset, evaluations = aoc_threshold_grid_chi2(rows, cov, subset, lambdas)

        best: dict[str, float | int] | None = None
        for lam, chi2, offset in evaluations:
            row = {
                "z_cut": cutoff,
                "K_cut": 1.0 + cutoff,
                "n": len(subset),
                "lambda_threshold": lam,
                "lcdm_chi2": lcdm_chi2,
                "lcdm_offset": lcdm_offset,
                "aoc_chi2": chi2,
                "aoc_offset": offset,
                "delta_chi2_aoc_minus_lcdm": chi2 - lcdm_chi2,
                "delta_aic_aoc_minus_lcdm": (chi2 + 2.0) - lcdm_chi2,
                "delta_bic_aoc_minus_lcdm": (chi2 + math.log(len(subset))) - lcdm_chi2,
            }
            out.append(row)
            if best is None or float(row["aoc_chi2"]) < float(best["aoc_chi2"]):
                best = row

        if best is not None:
            for row in out:
                if row["z_cut"] == cutoff:
                    row["best_lambda_for_cutoff"] = float(best["lambda_threshold"])
                    row["best_delta_chi2_for_cutoff"] = float(best["delta_chi2_aoc_minus_lcdm"])
                    row["best_delta_aic_for_cutoff"] = float(best["delta_aic_aoc_minus_lcdm"])
                    row["best_delta_bic_for_cutoff"] = float(best["delta_bic_aoc_minus_lcdm"])
    return out


def deterministic_split_label(cid: str, salt: str = "") -> str:
    """Assign a stable train/holdout label from object identity."""

    token = f"{salt}:{cid}" if salt else cid
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return "train" if digest[0] % 2 == 0 else "holdout"


def aoc_subset_chi2(rows: list[PantheonRow], cov, subset: list[int], lambda_threshold: float):
    lcdm_chi2, lcdm_offset, evaluations = aoc_threshold_grid_chi2(rows, cov, subset, [lambda_threshold])
    _, aoc_chi2, aoc_offset = evaluations[0]
    return lcdm_chi2, lcdm_offset, aoc_chi2, aoc_offset


def build_aoc_holdout_validation(rows: list[PantheonRow], cov) -> list[dict[str, float | int | str]]:
    """Train lambda on a deterministic CID split and evaluate on holdout."""

    if cov is None:
        return []

    usable_indices = [idx for idx, row in enumerate(rows) if row.mu is not None]
    cutoffs = [0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50]
    lambdas = [round(-0.3 + 0.01 * idx, 6) for idx in range(61)]
    out: list[dict[str, float | int | str]] = []

    for cutoff in cutoffs:
        subset = [idx for idx in usable_indices if rows[idx].z <= cutoff]
        train = [idx for idx in subset if deterministic_split_label(rows[idx].cid) == "train"]
        holdout = [idx for idx in subset if deterministic_split_label(rows[idx].cid) == "holdout"]
        if len(train) < 3 or len(holdout) < 3:
            continue

        train_lcdm_chi2, _, train_evaluations = aoc_threshold_grid_chi2(rows, cov, train, lambdas)
        best_lambda, best_train_chi2, _ = min(train_evaluations, key=lambda item: item[1])
        best_train_delta = best_train_chi2 - train_lcdm_chi2

        holdout_lcdm_chi2, holdout_lcdm_offset, holdout_aoc_chi2, holdout_aoc_offset = aoc_subset_chi2(
            rows,
            cov,
            holdout,
            best_lambda,
        )
        holdout_delta = holdout_aoc_chi2 - holdout_lcdm_chi2
        out.append(
            {
                "split_rule": "sha256(CID) first byte parity",
                "z_cut": cutoff,
                "K_cut": 1.0 + cutoff,
                "n_train": len(train),
                "n_holdout": len(holdout),
                "best_lambda_train": best_lambda,
                "train_delta_chi2_aoc_minus_lcdm": best_train_delta,
                "holdout_lcdm_chi2": holdout_lcdm_chi2,
                "holdout_lcdm_offset": holdout_lcdm_offset,
                "holdout_aoc_chi2": holdout_aoc_chi2,
                "holdout_aoc_offset": holdout_aoc_offset,
                "holdout_delta_chi2_aoc_minus_lcdm": holdout_delta,
                "holdout_delta_aic_aoc_minus_lcdm": holdout_delta + 2.0,
                "holdout_delta_bic_aoc_minus_lcdm": holdout_delta + math.log(len(holdout)),
            }
        )
    return out


def build_aoc_split_robustness(rows: list[PantheonRow], cov) -> list[dict[str, float | int]]:
    """Summarize holdout stability across several salted CID splits."""

    if cov is None:
        return []
    usable_indices = [idx for idx, row in enumerate(rows) if row.mu is not None]
    cutoffs = [0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50]
    lambdas = [round(-0.3 + 0.01 * idx, 6) for idx in range(61)]
    salts = [f"robust-{idx:02d}" for idx in range(16)]
    out: list[dict[str, float | int]] = []

    for cutoff in cutoffs:
        subset = [idx for idx in usable_indices if rows[idx].z <= cutoff]
        split_results: list[tuple[float, float, float]] = []
        for salt in salts:
            train = [idx for idx in subset if deterministic_split_label(rows[idx].cid, salt) == "train"]
            holdout = [idx for idx in subset if deterministic_split_label(rows[idx].cid, salt) == "holdout"]
            if len(train) < 3 or len(holdout) < 3:
                continue
            train_lcdm_chi2, _, train_evaluations = aoc_threshold_grid_chi2(rows, cov, train, lambdas)
            best_lambda, best_train_chi2, _ = min(train_evaluations, key=lambda item: item[1])
            holdout_lcdm_chi2, _, holdout_aoc_chi2, _ = aoc_subset_chi2(rows, cov, holdout, best_lambda)
            holdout_delta = holdout_aoc_chi2 - holdout_lcdm_chi2
            holdout_bic = holdout_delta + math.log(len(holdout))
            split_results.append((best_lambda, holdout_delta, holdout_bic))

        if not split_results:
            continue
        best_lambdas = [item[0] for item in split_results]
        holdout_deltas = [item[1] for item in split_results]
        holdout_bics = [item[2] for item in split_results]
        out.append(
            {
                "z_cut": cutoff,
                "K_cut": 1.0 + cutoff,
                "n_splits": len(split_results),
                "median_lambda_train": quantile(best_lambdas, 0.50),
                "median_holdout_delta_chi2": quantile(holdout_deltas, 0.50),
                "p10_holdout_delta_chi2": quantile(holdout_deltas, 0.10),
                "p90_holdout_delta_chi2": quantile(holdout_deltas, 0.90),
                "median_holdout_delta_bic": quantile(holdout_bics, 0.50),
                "p10_holdout_delta_bic": quantile(holdout_bics, 0.10),
                "p90_holdout_delta_bic": quantile(holdout_bics, 0.90),
                "frac_delta_bic_below_zero": sum(1 for value in holdout_bics if value < 0.0) / len(holdout_bics),
                "frac_delta_bic_below_minus_two": sum(1 for value in holdout_bics if value < -2.0) / len(holdout_bics),
            }
        )
    return out


def build_bins(rows: list[PantheonRow], n_bins: int = 12) -> list[dict[str, float | int]]:
    z_min = min(row.z for row in rows)
    z_max = max(row.z for row in rows)
    width = (z_max - z_min) / n_bins
    bins: list[dict[str, float | int]] = []
    for idx in range(n_bins):
        lo = z_min + idx * width
        hi = z_min + (idx + 1) * width if idx < n_bins - 1 else z_max + 1e-12
        members = [row for row in rows if lo <= row.z < hi]
        if not members:
            bins.append({"bin": idx, "z_lo": lo, "z_hi": hi, "n": 0, "mu_err_median": float("nan")})
            continue
        errs = [row.mu_err for row in members]
        bins.append(
            {
                "bin": idx,
                "z_lo": lo,
                "z_hi": hi,
                "n": len(members),
                "mu_err_median": quantile(errs, 0.50),
                "mu_err_p90": quantile(errs, 0.90),
            }
        )
    return bins


def write_bins(path: Path, bins: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["bin", "z_lo", "z_hi", "n", "mu_err_median", "mu_err_p90"])
        writer.writeheader()
        writer.writerows(bins)


def write_table(path: Path, rows: list[dict[str, float | int]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    summary: dict[str, object],
    bins: list[dict[str, float | int]],
    sweep: list[dict[str, float | int]],
    residual_bins: list[dict[str, float | int]],
    cov_k_sweep: list[dict[str, float | int]],
    discriminability: list[dict[str, float | int | str]],
    aoc_deformation: list[dict[str, float | int]],
    aoc_holdout: list[dict[str, float | int | str]],
    aoc_split_robustness: list[dict[str, float | int]],
) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    cov_available = bool(summary.get("covariance", {}).get("available")) if isinstance(summary.get("covariance"), dict) else False
    lines = [
        "# Pantheon+ Apparatus-Bound K Report",
        "",
        "Status: provisional empirical contract.",
        "",
        "## Allowed Claim",
        "",
        str(summary["allowed_claim"]),
        "",
        "## Forbidden Claim",
        "",
        str(summary["forbidden_claim"]),
        "",
        "## Summary",
        "",
        f"- Rows parsed: `{summary['n_rows']}`",
        f"- Redshift column: `{summary['columns']['z']}`",
        f"- Uncertainty column: `{summary['columns']['mu_err']}`",
        f"- Threshold `mu_err_max`: `{summary['mu_err_max']}`",
        f"- Rows passing threshold: `{summary['n_passing']}`",
        f"- Provisional `K_P = max(1+z)`: `{summary['K_P']:.6g}`",
        f"- Redshift at `K_P`: `{summary['z_at_K_P']:.6g}`",
        f"- Uncertainty at `K_P`: `{summary['mu_err_at_K_P']:.6g}`",
        "",
        "## Interpretation",
        "",
        str(summary["interpretation"]),
        "",
        "## Binned Uncertainty",
        "",
        "| bin | z range | n | median sigma_mu | p90 sigma_mu |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in bins:
        lines.append(
            f"| {row['bin']} | {row['z_lo']:.4g}-{row['z_hi']:.4g} | {row['n']} | "
            f"{row['mu_err_median']:.4g} | {row.get('mu_err_p90', float('nan')):.4g} |"
        )
    lines.extend(
        [
            "",
            "## Threshold Sensitivity",
            "",
            "| mu_err_max | n passing | K_P | z at K_P |",
            "| ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sweep:
        lines.append(
            f"| {row['mu_err_max']:.3g} | {row['n_passing']} | {row['K_P']:.6g} | {row['z_at_K_P']:.6g} |"
        )
    lines.extend(
        [
            "",
            "## Baseline LambdaCDM Residual Check",
            "",
            "Baseline used only as a comparison instrument:",
            "",
            "```text",
            "flat LambdaCDM, H0 = 70 km/s/Mpc, Omega_m = 0.3",
            "```",
            "",
            "This is not a cosmological fit and does not use the covariance matrix.",
            "",
            "| bin | z range | n | median residual mag | p10-p90 residual mag | median pull |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in residual_bins:
        lines.append(
            f"| {row['bin']} | {row['z_lo']:.4g}-{row['z_hi']:.4g} | {row['n']} | "
            f"{row['median_residual']:.4g} | {row.get('p10_residual', float('nan')):.4g} to "
            f"{row.get('p90_residual', float('nan')):.4g} | {row['median_pull']:.4g} |"
        )
    lines.extend(
        [
            "",
            "## Covariance-Aware Diagnostic",
            "",
        ]
    )
    if cov_available:
        cov_summary = summary["covariance"]  # type: ignore[index]
        lines.extend(
            [
                "Covariance file loaded successfully.",
                "",
                f"- Shape: `{cov_summary['covariance_shape']}`",
                f"- Median covariance diagonal sigma: `{cov_summary['diag_sigma_median']:.6g}`",
                f"- Median table sigma: `{cov_summary['table_sigma_median']:.6g}`",
                f"- Median diagonal-minus-table sigma: `{cov_summary['diag_minus_table_sigma_median']:.6g}`",
                f"- Max absolute diagonal-minus-table sigma: `{cov_summary['diag_minus_table_sigma_max_abs']:.6g}`",
                f"- Marginalized constant offset: `{cov_summary['marginalized_offset_mag']:.6g}` mag",
                f"- Chi2 after offset: `{cov_summary['chi2_after_offset']:.6g}`",
                f"- DOF after offset: `{cov_summary['dof_after_offset']}`",
                f"- Chi2/DOF after offset: `{cov_summary['chi2_per_dof_after_offset']:.6g}`",
                "",
                str(cov_summary["interpretation"]),
                "",
            ]
        )
        if cov_k_sweep:
            lines.extend(
                [
                    "### Covariance-Diagonal K Sensitivity",
                    "",
                    "This repeats the `K_P` threshold sweep using `sqrt(diag(C))` from the",
                    "downloaded covariance matrix rather than `MU_SH0ES_ERR_DIAG` from the",
                    "table. Because these differ, both are reported separately.",
                    "",
                    "| sigma threshold | n passing | K_P | z at K_P | sigma at K_P |",
                    "| ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for row in cov_k_sweep:
                lines.append(
                    f"| {row['mu_err_max']:.3g} | {row['n_passing']} | {row['K_P']:.6g} | "
                    f"{row['z_at_K_P']:.6g} | {row.get('cov_diag_sigma_at_K_P', float('nan')):.6g} |"
                )
            lines.append("")
        if discriminability:
            lines.extend(
                [
                    "### Model-Discriminability K",
                    "",
                    "This compares simple alternative distance curves against the fixed",
                    "flat-`LambdaCDM` baseline over increasing redshift cutoffs using the",
                    "full covariance submatrix. A constant magnitude offset is marginalized",
                    "separately for each model and cutoff.",
                    "",
                    "These alternatives are comparison instruments, not AOC models.",
                    "",
                    "| alternative | z cut | K cut | n | delta chi2 | delta chi2 / dof |",
                    "| --- | ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for row in discriminability:
                lines.append(
                    f"| {row['alternative']} | {row['z_cut']:.3g} | {row['K_cut']:.3g} | "
                    f"{row['n']} | {row['delta_chi2_alt_minus_lcdm']:.6g} | "
                    f"{row['delta_chi2_per_dof']:.6g} |"
                )
            lines.append("")
        if aoc_deformation:
            best_rows = []
            seen = set()
            for row in aoc_deformation:
                z_cut = float(row["z_cut"])
                if z_cut in seen:
                    continue
                seen.add(z_cut)
                best_rows.append(row)
            lines.extend(
                [
                    "### AOC Threshold-Deformation Probe",
                    "",
                    "Minimal one-parameter deformation:",
                    "",
                    "```text",
                    "mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)",
                    "z_star = 0.8",
                    "```",
                    "",
                    "`lambda = 0` recovers the flat-`LambdaCDM` baseline exactly. This is",
                    "a phenomenological threshold probe, not the final AOC distance law.",
                    "",
                    "| z cut | K cut | n | best lambda | best delta chi2 | best delta AIC | best delta BIC |",
                    "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for row in best_rows:
                lines.append(
                    f"| {row['z_cut']:.3g} | {row['K_cut']:.3g} | {row['n']} | "
                    f"{row['best_lambda_for_cutoff']:.3g} | {row['best_delta_chi2_for_cutoff']:.6g} | "
                    f"{row['best_delta_aic_for_cutoff']:.6g} | {row['best_delta_bic_for_cutoff']:.6g} |"
                )
            lines.append("")
        if aoc_holdout:
            lines.extend(
                [
                    "### AOC Threshold-Deformation Holdout Check",
                    "",
                    "This is a deterministic exploratory train/holdout check. The split is",
                    "by `CID` using `sha256(CID)` first-byte parity, so repeated rows for",
                    "the same object stay on the same side where the identifier is stable.",
                    "",
                    "For each redshift cutoff, `lambda` is selected on the train side and",
                    "then evaluated once on the holdout side. Because the deformation form",
                    "was chosen after earlier Pantheon+ exploration, this is still not a",
                    "fully blinded confirmation.",
                    "",
                    "| z cut | K cut | n train | n holdout | train lambda | holdout delta chi2 | holdout delta AIC | holdout delta BIC |",
                    "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for row in aoc_holdout:
                lines.append(
                    f"| {row['z_cut']:.3g} | {row['K_cut']:.3g} | {row['n_train']} | {row['n_holdout']} | "
                    f"{row['best_lambda_train']:.3g} | {row['holdout_delta_chi2_aoc_minus_lcdm']:.6g} | "
                    f"{row['holdout_delta_aic_aoc_minus_lcdm']:.6g} | "
                    f"{row['holdout_delta_bic_aoc_minus_lcdm']:.6g} |"
                )
            lines.append("")
        if aoc_split_robustness:
            lines.extend(
                [
                    "### AOC Split-Robustness Check",
                    "",
                    "This repeats the train/holdout procedure across 16 salted `CID`",
                    "splits and summarizes the holdout distribution. It checks whether",
                    "the exploratory pattern depends heavily on the single primary split.",
                    "",
                    "| z cut | K cut | splits | median lambda | median holdout delta chi2 | median holdout delta BIC | frac BIC < 0 | frac BIC < -2 |",
                    "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for row in aoc_split_robustness:
                lines.append(
                    f"| {row['z_cut']:.3g} | {row['K_cut']:.3g} | {row['n_splits']} | "
                    f"{row['median_lambda_train']:.3g} | {row['median_holdout_delta_chi2']:.6g} | "
                    f"{row['median_holdout_delta_bic']:.6g} | {row['frac_delta_bic_below_zero']:.3g} | "
                    f"{row['frac_delta_bic_below_minus_two']:.3g} |"
                )
            lines.append("")
    else:
        lines.extend(
            [
                "Covariance file was not available or could not be used.",
                "",
            ]
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "Run the predeclared rule on a genuinely separate dataset or a blinded split, "
            "then replace the phenomenological threshold deformation with a distance law "
            "derived from the AOC proof spine.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_plot(rows: list[PantheonRow], summary: dict[str, object]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    z = [row.z for row in rows]
    mu_err = [row.mu_err for row in rows]
    plt.figure(figsize=(8, 4.8), dpi=160)
    plt.scatter(z, mu_err, s=7, alpha=0.38, color="#1d7f8c", edgecolors="none")
    plt.axhline(float(summary["mu_err_max"]), color="#9c4638", linewidth=1.4, label="threshold")
    plt.axvline(float(summary["z_at_K_P"]), color="#d28f2d", linewidth=1.4, label="z at K_P")
    plt.xlabel("redshift z")
    plt.ylabel("distance-modulus uncertainty proxy")
    plt.title("Pantheon+ provisional apparatus-bound K")
    plt.legend()
    plt.grid(True, alpha=0.22)
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    plt.close()


def write_sweep_plot(sweep: list[dict[str, float | int]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    thresholds = [float(row["mu_err_max"]) for row in sweep]
    k_values = [float(row["K_P"]) for row in sweep]
    n_passing = [int(row["n_passing"]) for row in sweep]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=160)
    axes[0].plot(thresholds, k_values, marker="o", color="#1d7f8c")
    axes[0].set_xlabel("mu_err_max")
    axes[0].set_ylabel("K_P")
    axes[0].set_title("K_P threshold sensitivity")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(thresholds, n_passing, marker="o", color="#d28f2d")
    axes[1].set_xlabel("mu_err_max")
    axes[1].set_ylabel("rows passing")
    axes[1].set_title("sample included")
    axes[1].grid(True, alpha=0.25)

    fig.tight_layout()
    fig.savefig(SWEEP_PLOT_PATH)
    plt.close(fig)


def write_residual_plot(rows: list[PantheonRow], cosmology: FlatLambdaCDM = FlatLambdaCDM()) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    usable = [row for row in rows if row.mu is not None]
    z = [row.z for row in usable]
    residual = [row.mu - distance_modulus_lcdm(row.z, cosmology) for row in usable]  # type: ignore[operator]

    plt.figure(figsize=(8, 4.8), dpi=160)
    plt.scatter(z, residual, s=7, alpha=0.35, color="#1d7f8c", edgecolors="none")
    plt.axhline(0, color="#9c4638", linewidth=1.2)
    plt.xlabel("redshift z")
    plt.ylabel("mu_observed - mu_flat_LCDM")
    plt.title("Pantheon+ residuals against simple flat LambdaCDM baseline")
    plt.grid(True, alpha=0.22)
    plt.tight_layout()
    plt.savefig(RESIDUAL_PLOT_PATH)
    plt.close()


def write_discriminability_plot(discriminability: list[dict[str, float | int | str]]) -> None:
    if not discriminability:
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    alternatives = sorted({str(row["alternative"]) for row in discriminability})
    plt.figure(figsize=(8, 4.8), dpi=160)
    for alt in alternatives:
        rows_for_alt = [row for row in discriminability if row["alternative"] == alt]
        rows_for_alt.sort(key=lambda row: float(row["z_cut"]))
        z_cut = [float(row["z_cut"]) for row in rows_for_alt]
        delta = [float(row["delta_chi2_alt_minus_lcdm"]) for row in rows_for_alt]
        plt.plot(z_cut, delta, marker="o", label=alt)
    plt.axhline(0, color="#9c4638", linewidth=1.0)
    plt.xlabel("redshift cutoff")
    plt.ylabel("delta chi2 vs flat LambdaCDM")
    plt.title("Pantheon+ model-discriminability over redshift cutoffs")
    plt.legend()
    plt.grid(True, alpha=0.22)
    plt.tight_layout()
    plt.savefig(DISCRIMINABILITY_PLOT_PATH)
    plt.close()


def write_aoc_deformation_plot(aoc_deformation: list[dict[str, float | int]]) -> None:
    if not aoc_deformation:
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    cutoffs = sorted({float(row["z_cut"]) for row in aoc_deformation})
    best_lambda = []
    best_delta = []
    best_delta_bic = []
    for cutoff in cutoffs:
        rows = [row for row in aoc_deformation if float(row["z_cut"]) == cutoff]
        best = min(rows, key=lambda row: float(row["aoc_chi2"]))
        best_lambda.append(float(best["lambda_threshold"]))
        best_delta.append(float(best["delta_chi2_aoc_minus_lcdm"]))
        best_delta_bic.append(float(best["delta_bic_aoc_minus_lcdm"]))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=160)
    axes[0].plot(cutoffs, best_lambda, marker="o", color="#1d7f8c")
    axes[0].axhline(0, color="#9c4638", linewidth=1.0)
    axes[0].set_xlabel("redshift cutoff")
    axes[0].set_ylabel("best lambda")
    axes[0].set_title("Best threshold deformation")
    axes[0].grid(True, alpha=0.22)

    axes[1].plot(cutoffs, best_delta, marker="o", color="#d28f2d", label="delta chi2")
    axes[1].plot(cutoffs, best_delta_bic, marker="s", color="#6f5aa7", label="delta BIC")
    axes[1].axhline(0, color="#9c4638", linewidth=1.0)
    axes[1].set_xlabel("redshift cutoff")
    axes[1].set_ylabel("best delta chi2 vs LCDM")
    axes[1].set_title("Improvement over baseline")
    axes[1].legend()
    axes[1].grid(True, alpha=0.22)

    fig.tight_layout()
    fig.savefig(AOC_DEFORMATION_PLOT_PATH)
    plt.close(fig)


def write_aoc_holdout_plot(aoc_holdout: list[dict[str, float | int | str]]) -> None:
    if not aoc_holdout:
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    rows = sorted(aoc_holdout, key=lambda row: float(row["z_cut"]))
    z_cut = [float(row["z_cut"]) for row in rows]
    lambdas = [float(row["best_lambda_train"]) for row in rows]
    delta_chi2 = [float(row["holdout_delta_chi2_aoc_minus_lcdm"]) for row in rows]
    delta_bic = [float(row["holdout_delta_bic_aoc_minus_lcdm"]) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=160)
    axes[0].plot(z_cut, lambdas, marker="o", color="#1d7f8c")
    axes[0].axhline(0, color="#9c4638", linewidth=1.0)
    axes[0].set_xlabel("redshift cutoff")
    axes[0].set_ylabel("lambda selected on train")
    axes[0].set_title("Heldout deformation parameter")
    axes[0].grid(True, alpha=0.22)

    axes[1].plot(z_cut, delta_chi2, marker="o", color="#d28f2d", label="holdout delta chi2")
    axes[1].plot(z_cut, delta_bic, marker="s", color="#6f5aa7", label="holdout delta BIC")
    axes[1].axhline(0, color="#9c4638", linewidth=1.0)
    axes[1].set_xlabel("redshift cutoff")
    axes[1].set_ylabel("holdout delta vs LCDM")
    axes[1].set_title("Heldout evaluation")
    axes[1].legend()
    axes[1].grid(True, alpha=0.22)

    fig.tight_layout()
    fig.savefig(AOC_HOLDOUT_PLOT_PATH)
    plt.close(fig)


def write_aoc_split_robustness_plot(aoc_split_robustness: list[dict[str, float | int]]) -> None:
    if not aoc_split_robustness:
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    rows = sorted(aoc_split_robustness, key=lambda row: float(row["z_cut"]))
    z_cut = [float(row["z_cut"]) for row in rows]
    median_bic = [float(row["median_holdout_delta_bic"]) for row in rows]
    p10_bic = [float(row["p10_holdout_delta_bic"]) for row in rows]
    p90_bic = [float(row["p90_holdout_delta_bic"]) for row in rows]
    frac_bic_below_zero = [float(row["frac_delta_bic_below_zero"]) for row in rows]
    frac_bic_below_minus_two = [float(row["frac_delta_bic_below_minus_two"]) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=160)
    axes[0].plot(z_cut, median_bic, marker="o", color="#1d7f8c", label="median delta BIC")
    axes[0].fill_between(z_cut, p10_bic, p90_bic, color="#1d7f8c", alpha=0.18, label="p10-p90")
    axes[0].axhline(0, color="#9c4638", linewidth=1.0)
    axes[0].axhline(-2, color="#d28f2d", linewidth=1.0, linestyle="--")
    axes[0].set_xlabel("redshift cutoff")
    axes[0].set_ylabel("holdout delta BIC")
    axes[0].set_title("Split-robust holdout BIC")
    axes[0].legend()
    axes[0].grid(True, alpha=0.22)

    axes[1].plot(z_cut, frac_bic_below_zero, marker="o", color="#6f5aa7", label="frac BIC < 0")
    axes[1].plot(z_cut, frac_bic_below_minus_two, marker="s", color="#d28f2d", label="frac BIC < -2")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].set_xlabel("redshift cutoff")
    axes[1].set_ylabel("fraction of splits")
    axes[1].set_title("Split support frequency")
    axes[1].legend()
    axes[1].grid(True, alpha=0.22)

    fig.tight_layout()
    fig.savefig(AOC_SPLIT_ROBUSTNESS_PLOT_PATH)
    plt.close(fig)


def main() -> None:
    rows, columns = load_rows(RAW_PATH)
    summary = summarize(rows, columns)
    bins = build_bins(rows)
    sweep = build_threshold_sweep(rows)
    residual_bins = build_lcdm_residual_bins(rows)
    cov = load_covariance(COV_PATH, len(rows))
    cov_info = covariance_summary(rows, cov)
    cov_k_sweep = build_covariance_diag_k_sweep(rows, cov)
    discriminability = build_model_discriminability(rows, cov)
    aoc_deformation = build_aoc_threshold_deformation(rows, cov)
    aoc_holdout = build_aoc_holdout_validation(rows, cov)
    aoc_split_robustness = build_aoc_split_robustness(rows, cov)
    summary["covariance"] = cov_info
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    COV_SUMMARY_PATH.write_text(json.dumps(cov_info, indent=2), encoding="utf-8")
    write_bins(BINS_PATH, bins)
    write_table(
        SWEEP_PATH,
        sweep,
        ["mu_err_max", "n_passing", "K_P", "z_at_K_P", "mu_err_at_K_P"],
    )
    write_table(
        RESIDUALS_PATH,
        residual_bins,
        ["bin", "z_lo", "z_hi", "n", "median_residual", "p10_residual", "p90_residual", "median_pull"],
    )
    if cov_k_sweep:
        write_table(
            COV_K_SWEEP_PATH,
            cov_k_sweep,
            ["mu_err_max", "n_passing", "K_P", "z_at_K_P", "cov_diag_sigma_at_K_P"],
        )
    if discriminability:
        write_table(
            DISCRIMINABILITY_PATH,
            discriminability,
            [
                "alternative",
                "z_cut",
                "K_cut",
                "n",
                "lcdm_chi2",
                "lcdm_offset",
                "alt_chi2",
                "alt_offset",
                "delta_chi2_alt_minus_lcdm",
                "delta_chi2_per_dof",
            ],
        )
    if aoc_deformation:
        write_table(
            AOC_DEFORMATION_PATH,
            aoc_deformation,
            [
                "z_cut",
                "K_cut",
                "n",
                "lambda_threshold",
                "lcdm_chi2",
                "lcdm_offset",
                "aoc_chi2",
                "aoc_offset",
                "delta_chi2_aoc_minus_lcdm",
                "delta_aic_aoc_minus_lcdm",
                "delta_bic_aoc_minus_lcdm",
                "best_lambda_for_cutoff",
                "best_delta_chi2_for_cutoff",
                "best_delta_aic_for_cutoff",
                "best_delta_bic_for_cutoff",
            ],
        )
    if aoc_holdout:
        write_table(
            AOC_HOLDOUT_PATH,
            aoc_holdout,
            [
                "split_rule",
                "z_cut",
                "K_cut",
                "n_train",
                "n_holdout",
                "best_lambda_train",
                "train_delta_chi2_aoc_minus_lcdm",
                "holdout_lcdm_chi2",
                "holdout_lcdm_offset",
                "holdout_aoc_chi2",
                "holdout_aoc_offset",
                "holdout_delta_chi2_aoc_minus_lcdm",
                "holdout_delta_aic_aoc_minus_lcdm",
                "holdout_delta_bic_aoc_minus_lcdm",
            ],
        )
    if aoc_split_robustness:
        write_table(
            AOC_SPLIT_ROBUSTNESS_PATH,
            aoc_split_robustness,
            [
                "z_cut",
                "K_cut",
                "n_splits",
                "median_lambda_train",
                "median_holdout_delta_chi2",
                "p10_holdout_delta_chi2",
                "p90_holdout_delta_chi2",
                "median_holdout_delta_bic",
                "p10_holdout_delta_bic",
                "p90_holdout_delta_bic",
                "frac_delta_bic_below_zero",
                "frac_delta_bic_below_minus_two",
            ],
        )
    write_report(
        summary,
        bins,
        sweep,
        residual_bins,
        cov_k_sweep,
        discriminability,
        aoc_deformation,
        aoc_holdout,
        aoc_split_robustness,
    )
    write_plot(rows, summary)
    write_sweep_plot(sweep)
    write_residual_plot(rows)
    write_discriminability_plot(discriminability)
    write_aoc_deformation_plot(aoc_deformation)
    write_aoc_holdout_plot(aoc_holdout)
    write_aoc_split_robustness_plot(aoc_split_robustness)
    print(f"Wrote {SUMMARY_PATH}")
    print(f"Wrote {COV_SUMMARY_PATH}")
    print(f"Wrote {BINS_PATH}")
    print(f"Wrote {SWEEP_PATH}")
    print(f"Wrote {RESIDUALS_PATH}")
    if COV_K_SWEEP_PATH.exists():
        print(f"Wrote {COV_K_SWEEP_PATH}")
    if DISCRIMINABILITY_PATH.exists():
        print(f"Wrote {DISCRIMINABILITY_PATH}")
    if AOC_DEFORMATION_PATH.exists():
        print(f"Wrote {AOC_DEFORMATION_PATH}")
    if AOC_HOLDOUT_PATH.exists():
        print(f"Wrote {AOC_HOLDOUT_PATH}")
    if AOC_SPLIT_ROBUSTNESS_PATH.exists():
        print(f"Wrote {AOC_SPLIT_ROBUSTNESS_PATH}")
    print(f"Wrote {REPORT_PATH}")
    if PLOT_PATH.exists():
        print(f"Wrote {PLOT_PATH}")
    if SWEEP_PLOT_PATH.exists():
        print(f"Wrote {SWEEP_PLOT_PATH}")
    if RESIDUAL_PLOT_PATH.exists():
        print(f"Wrote {RESIDUAL_PLOT_PATH}")
    if DISCRIMINABILITY_PLOT_PATH.exists():
        print(f"Wrote {DISCRIMINABILITY_PLOT_PATH}")
    if AOC_DEFORMATION_PLOT_PATH.exists():
        print(f"Wrote {AOC_DEFORMATION_PLOT_PATH}")
    if AOC_HOLDOUT_PLOT_PATH.exists():
        print(f"Wrote {AOC_HOLDOUT_PLOT_PATH}")
    if AOC_SPLIT_ROBUSTNESS_PLOT_PATH.exists():
        print(f"Wrote {AOC_SPLIT_ROBUSTNESS_PLOT_PATH}")


if __name__ == "__main__":
    main()
