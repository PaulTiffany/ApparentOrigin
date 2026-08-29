"""Two-pipeline apparatus-bound K simulation with explicit reconstruction.

This script extends the closed-form §3 toy in `apparatus_k.py` to the §5--§7
program in `docs/apparatus_bound_k_program.md`:

    section 5: noise instantiation under sigma_P(y) = sigma_0 * y**p
    section 6: two-pipeline ratio K_2 / K_1 = (sigma_{0,1} / sigma_{0,2})**(1/(p-1))
    section 7: atlas-coherence Gamma between two reconstruction charts of one pipeline

The structural point is that apparatus-bound K is a property of a reconstruction
pipeline, not of a static dataset. A test of the formalism therefore has to be
one in which the pipeline is fully specified by us: we generate the
observations under a known noise law, run an explicit reconstruction, and
measure K from the reconstruction. The §6 ratio prediction then becomes a real
internal check rather than a tautology against the closed form.

This is the simulation analog of the SRMF program-discipline lesson: the agent
that ascribes label authenticity has to be made explicit, and the cost of
doing so is paid at construction time. It does not contact real cosmological
data and does not claim to validate AOC against any observation.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class FRWChart:
    """Power-law FRW chart: a(t) = A t^alpha; y(t) = (1/A) t^(-alpha)."""

    A: float = 1.0
    alpha: float = 0.5

    def y_of_t(self, t: np.ndarray) -> np.ndarray:
        return (1.0 / self.A) * np.asarray(t, dtype=float) ** (-self.alpha)

    def t_of_y(self, y: np.ndarray) -> np.ndarray:
        return (self.A * np.asarray(y, dtype=float)) ** (-1.0 / self.alpha)


@dataclass(frozen=True)
class Pipeline:
    name: str
    sigma_0: float
    p: float

    def closed_form_K(self, eta: float) -> float:
        return (eta / self.sigma_0) ** (1.0 / (self.p - 1.0))

    def closed_form_sigma(self, y: np.ndarray) -> np.ndarray:
        return self.sigma_0 * np.asarray(y, dtype=float) ** self.p


# -----------------------------------------------------------------------------
# Forward model
# -----------------------------------------------------------------------------


def sample_observations(
    pipeline: Pipeline,
    chart: FRWChart,
    rng: np.random.Generator,
    n_obs: int,
    t_min: float,
    t_max: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample t uniformly in log, compute y_true, add y-dependent noise."""

    log_t = rng.uniform(math.log(t_min), math.log(t_max), size=n_obs)
    t = np.exp(log_t)
    y_true = chart.y_of_t(t)
    sigma = pipeline.closed_form_sigma(y_true)
    noise = rng.normal(loc=0.0, scale=sigma)
    y_obs = y_true + noise
    return t, y_true, y_obs


# -----------------------------------------------------------------------------
# Empirical sigma_hat(y) via binning
# -----------------------------------------------------------------------------


def empirical_sigma_per_y_bin(
    y_true: np.ndarray,
    y_obs: np.ndarray,
    y_edges: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bin the residuals in y_true and compute std per bin."""

    centers = 0.5 * (y_edges[:-1] + y_edges[1:])
    sigma_hat = np.full_like(centers, np.nan, dtype=float)
    counts = np.zeros_like(centers, dtype=int)
    residuals = y_obs - y_true
    for i in range(len(centers)):
        lo, hi = y_edges[i], y_edges[i + 1]
        mask = (y_true >= lo) & (y_true < hi)
        n = int(mask.sum())
        counts[i] = n
        if n >= 4:
            sigma_hat[i] = float(residuals[mask].std(ddof=1))
    return centers, sigma_hat, counts


def k_from_reconstruction(
    centers: np.ndarray,
    sigma_hat: np.ndarray,
    eta: float,
) -> float:
    """K via log-log interpolation of sigma_hat(y) crossing sigma_hat = eta * y."""

    finite = np.isfinite(sigma_hat) & (centers > 0.0) & (sigma_hat > 0.0)
    if finite.sum() < 2:
        return float("nan")
    log_y = np.log(centers[finite])
    log_sig = np.log(sigma_hat[finite])
    # We want the largest y where sigma_hat(y) = eta * y, i.e. log_sig - log_y = log eta.
    f = log_sig - log_y - math.log(eta)
    # The reliability floor is the largest y with f(y) <= 0; sigma_P ~ y^p with p>1
    # makes f monotone increasing, so look for the last sign change from <=0 to >0.
    order = np.argsort(log_y)
    log_y_s = log_y[order]
    f_s = f[order]
    # Largest index where f_s <= 0:
    le_zero = np.where(f_s <= 0.0)[0]
    if le_zero.size == 0:
        return float("nan")
    last = int(le_zero.max())
    if last == len(f_s) - 1:
        return float(np.exp(log_y_s[last]))
    # Linear interpolation in log-y between the bracket (last, last+1).
    f0, f1 = f_s[last], f_s[last + 1]
    if f1 == f0:
        return float(np.exp(log_y_s[last]))
    frac = -f0 / (f1 - f0)
    log_y_star = log_y_s[last] + frac * (log_y_s[last + 1] - log_y_s[last])
    return float(np.exp(log_y_star))


# -----------------------------------------------------------------------------
# Atlas-coherence: two reconstruction charts of the same observations
# -----------------------------------------------------------------------------


def chart_kernel(
    t_obs: np.ndarray,
    y_obs: np.ndarray,
    t_eval: np.ndarray,
    bandwidth_log_t: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Gaussian kernel smoother in log-t: returns y_hat and stderr of mean."""

    log_obs = np.log(t_obs)
    log_eval = np.log(t_eval)
    diff = log_obs[None, :] - log_eval[:, None]
    raw = np.exp(-0.5 * (diff / bandwidth_log_t) ** 2)
    norm = raw.sum(axis=1, keepdims=True)
    safe_norm = np.where(norm > 0.0, norm, 1.0)
    weights = raw / safe_norm
    y_hat = (weights * y_obs[None, :]).sum(axis=1)
    centered = y_obs[None, :] - y_hat[:, None]
    var = (weights * centered ** 2).sum(axis=1)
    eff_n = 1.0 / np.maximum((weights ** 2).sum(axis=1), 1e-12)
    stderr_mean = np.sqrt(np.maximum(var, 0.0) / np.maximum(eff_n, 1e-12))
    return y_hat, stderr_mean


def chart_binned_median(
    t_obs: np.ndarray,
    y_obs: np.ndarray,
    t_eval: np.ndarray,
    bin_width_log_t: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Binned median estimator in log-t: returns y_hat and stderr of median."""

    log_obs = np.log(t_obs)
    log_eval = np.log(t_eval)
    y_hat = np.full_like(t_eval, np.nan, dtype=float)
    stderr_mean = np.full_like(t_eval, np.nan, dtype=float)
    half = 0.5 * bin_width_log_t
    for i, le in enumerate(log_eval):
        mask = (log_obs >= le - half) & (log_obs <= le + half)
        n = int(mask.sum())
        if n < 4:
            continue
        bucket = y_obs[mask]
        med = float(np.median(bucket))
        # 1.4826 maps sample MAD to a Gaussian-equivalent sigma.
        mad = float(np.median(np.abs(bucket - med)))
        sigma = 1.4826 * mad
        # Standard error of the median for a roughly-Gaussian sample.
        stderr = 1.2533 * sigma / math.sqrt(n)
        y_hat[i] = med
        stderr_mean[i] = stderr
    return y_hat, stderr_mean


def gamma_atlas(
    y_hat_1: np.ndarray,
    se_1: np.ndarray,
    y_hat_2: np.ndarray,
    se_2: np.ndarray,
) -> np.ndarray:
    """Apparatus-bound atlas coherence Gamma(y) = |y1 - y2| / sqrt(se1^2 + se2^2)."""

    denom = np.sqrt(se_1 ** 2 + se_2 ** 2)
    out = np.full_like(denom, np.nan, dtype=float)
    finite = np.isfinite(y_hat_1) & np.isfinite(y_hat_2) & (denom > 0.0)
    out[finite] = np.abs(y_hat_1[finite] - y_hat_2[finite]) / denom[finite]
    return out


def k_with_atlas_cutoff(
    centers: np.ndarray,
    sigma_hat: np.ndarray,
    gamma: np.ndarray,
    eta: float,
    gamma_max: float,
) -> float:
    """K passing reliability AND atlas coherence, with log-log interpolation.

    The reliability floor is interpolated as in k_from_reconstruction. The
    atlas-coherence floor is the largest y where gamma(y) <= gamma_max, taken
    on the same evaluation grid. The joint K is the smaller of the two.
    """

    finite_rel = np.isfinite(sigma_hat) & (centers > 0.0) & (sigma_hat > 0.0)
    finite_gamma = np.isfinite(gamma) & (centers > 0.0)
    if finite_rel.sum() < 2 or finite_gamma.sum() < 1:
        return float("nan")
    k_rel = k_from_reconstruction(centers, sigma_hat, eta)
    atlas_passing = centers[finite_gamma][gamma[finite_gamma] <= gamma_max]
    if atlas_passing.size == 0 or not math.isfinite(k_rel):
        return float("nan")
    k_atlas = float(atlas_passing.max())
    return min(k_rel, k_atlas)


# -----------------------------------------------------------------------------
# Monte Carlo over seeds
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class MCConfig:
    n_seeds: int = 60
    n_obs: int = 4000
    t_min: float = 1e-4
    t_max: float = 100.0
    eta: float = 0.10
    gamma_max: float = 3.0
    n_y_bins: int = 30
    y_eval_points: int = 30
    kernel_bandwidth_log_t: float = 0.30
    bin_width_log_t: float = 0.60


def y_bin_edges(t_min: float, t_max: float, chart: FRWChart, n_bins: int) -> np.ndarray:
    y_lo = float(chart.y_of_t(np.array([t_max]))[0])
    y_hi = float(chart.y_of_t(np.array([t_min]))[0])
    # Use log-spaced edges in y because sigma_P(y) ~ y^p spans many decades.
    return np.exp(np.linspace(math.log(y_lo), math.log(y_hi), n_bins + 1))


def y_eval_grid(t_min: float, t_max: float, chart: FRWChart, n_eval: int) -> np.ndarray:
    y_lo = float(chart.y_of_t(np.array([t_max]))[0])
    y_hi = float(chart.y_of_t(np.array([t_min]))[0])
    return np.exp(np.linspace(math.log(y_lo), math.log(y_hi), n_eval))


def run_one_seed(
    pipeline: Pipeline,
    chart: FRWChart,
    cfg: MCConfig,
    rng: np.random.Generator,
    edges: np.ndarray,
    y_eval: np.ndarray,
) -> dict[str, float]:
    """One MC realization of one pipeline. Returns scalar summaries."""

    t, y_true, y_obs = sample_observations(
        pipeline, chart, rng, cfg.n_obs, cfg.t_min, cfg.t_max
    )

    # Reliability floor.
    centers, sigma_hat, counts = empirical_sigma_per_y_bin(y_true, y_obs, edges)
    k_emp = k_from_reconstruction(centers, sigma_hat, cfg.eta)
    k_closed = pipeline.closed_form_K(cfg.eta)
    t_k_emp = float((chart.A * k_emp) ** (-1.0 / chart.alpha)) if math.isfinite(k_emp) else float("nan")
    t_k_closed = float((chart.A * k_closed) ** (-1.0 / chart.alpha))

    # Atlas coherence: two charts of the same observations evaluated at y_eval.
    t_eval = chart.t_of_y(y_eval)
    y_hat_k, se_k = chart_kernel(t, y_obs, t_eval, cfg.kernel_bandwidth_log_t)
    y_hat_b, se_b = chart_binned_median(t, y_obs, t_eval, cfg.bin_width_log_t)
    gamma = gamma_atlas(y_hat_k, se_k, y_hat_b, se_b)

    # Re-bin sigma_hat at y_eval points so it lines up with gamma.
    sigma_hat_eval = np.interp(
        y_eval,
        centers[np.isfinite(sigma_hat)],
        sigma_hat[np.isfinite(sigma_hat)],
        left=np.nan,
        right=np.nan,
    )
    k_atlas = k_with_atlas_cutoff(y_eval, sigma_hat_eval, gamma, cfg.eta, cfg.gamma_max)

    return {
        "k_emp": k_emp,
        "k_closed": k_closed,
        "k_emp_minus_closed": k_emp - k_closed if math.isfinite(k_emp) else float("nan"),
        "t_k_emp": t_k_emp,
        "t_k_closed": t_k_closed,
        "k_atlas": k_atlas,
        "gamma_at_k_emp": float(np.interp(k_emp, y_eval, gamma)) if math.isfinite(k_emp) else float("nan"),
    }


def run_pipeline_mc(
    pipeline: Pipeline,
    chart: FRWChart,
    cfg: MCConfig,
    seed_root: int,
) -> list[dict[str, float]]:
    edges = y_bin_edges(cfg.t_min, cfg.t_max, chart, cfg.n_y_bins)
    y_eval = y_eval_grid(cfg.t_min, cfg.t_max, chart, cfg.y_eval_points)
    out: list[dict[str, float]] = []
    for seed in range(cfg.n_seeds):
        rng = np.random.default_rng(seed_root + seed)
        out.append(run_one_seed(pipeline, chart, cfg, rng, edges, y_eval))
    return out


def summarize_mc(results: list[dict[str, float]]) -> dict[str, float]:
    keys = [k for k in results[0].keys()]
    summary: dict[str, float] = {}
    for k in keys:
        values = np.array([row[k] for row in results], dtype=float)
        finite = values[np.isfinite(values)]
        if finite.size == 0:
            summary[f"{k}_median"] = float("nan")
            summary[f"{k}_p10"] = float("nan")
            summary[f"{k}_p90"] = float("nan")
            summary[f"{k}_n_finite"] = 0
            continue
        summary[f"{k}_median"] = float(np.median(finite))
        summary[f"{k}_p10"] = float(np.percentile(finite, 10))
        summary[f"{k}_p90"] = float(np.percentile(finite, 90))
        summary[f"{k}_n_finite"] = int(finite.size)
    return summary


# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------


ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "apparatus_k_two_pipeline_seeds.csv"
SUMMARY_PATH = ROOT / "apparatus_k_two_pipeline_summary.json"
RATIO_PATH = ROOT / "apparatus_k_two_pipeline_ratio.csv"
ATLAS_PATH = ROOT / "apparatus_k_two_pipeline_atlas.csv"
PLOT_PATH = ROOT / "apparatus_k_two_pipeline.png"


def write_seed_table(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_ratio_table(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with RATIO_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_atlas_table(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with ATLAS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def maybe_plot(
    pipelines: list[Pipeline],
    pipeline_seed_results: dict[str, list[dict[str, float]]],
    chart: FRWChart,
    cfg: MCConfig,
    representative_atlas: dict[str, np.ndarray],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4), dpi=150)

    # Panel 1: K_emp vs K_closed for both pipelines (MC scatter).
    for pipeline in pipelines:
        results = pipeline_seed_results[pipeline.name]
        k_emp = np.array([r["k_emp"] for r in results])
        k_closed = pipeline.closed_form_K(cfg.eta)
        axes[0].scatter(
            np.full_like(k_emp, k_closed), k_emp, s=14, alpha=0.55, label=pipeline.name
        )
    axes[0].plot(
        [1, 200], [1, 200], color="#9c4638", linewidth=1.0, linestyle="--", label="K_emp = K_closed"
    )
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("closed-form K")
    axes[0].set_ylabel("reconstructed K")
    axes[0].set_title("Reliability-floor K: closed form vs reconstruction")
    axes[0].legend()
    axes[0].grid(True, alpha=0.22)

    # Panel 2: ratio K_2/K_1 distribution vs theoretical line.
    name_lo, name_hi = pipelines[0].name, pipelines[1].name
    k_lo = np.array([r["k_emp"] for r in pipeline_seed_results[name_lo]])
    k_hi = np.array([r["k_emp"] for r in pipeline_seed_results[name_hi]])
    ratios = k_hi / k_lo
    theory = (pipelines[0].sigma_0 / pipelines[1].sigma_0) ** (1.0 / (pipelines[0].p - 1.0))
    axes[1].hist(ratios, bins=20, color="#1d7f8c", alpha=0.7)
    axes[1].axvline(theory, color="#9c4638", linewidth=1.4, label=f"theory K2/K1 = {theory:.3g}")
    axes[1].set_xlabel(f"K_emp({name_hi}) / K_emp({name_lo})")
    axes[1].set_ylabel("seeds")
    axes[1].set_title("Two-pipeline ratio prediction")
    axes[1].legend()
    axes[1].grid(True, alpha=0.22)

    # Panel 3: atlas-coherence Gamma(y) for pipeline_lo on a representative seed.
    y_eval = representative_atlas["y_eval"]
    gamma = representative_atlas["gamma"]
    axes[2].plot(y_eval, gamma, marker="o", markersize=3, linewidth=0.9, color="#1d7f8c")
    axes[2].axhline(cfg.gamma_max, color="#9c4638", linewidth=1.0, linestyle="--", label="gamma_max")
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("y = 1 + z analog")
    axes[2].set_ylabel("Gamma(y)")
    axes[2].set_title(f"Atlas coherence for {representative_atlas['pipeline']}")
    axes[2].legend()
    axes[2].grid(True, alpha=0.22)

    fig.tight_layout()
    fig.savefig(PLOT_PATH)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    chart = FRWChart(A=1.0, alpha=0.5)
    cfg = MCConfig()
    pipelines = [
        Pipeline(name="baseline", sigma_0=0.010, p=1.8),
        Pipeline(name="improved", sigma_0=0.003, p=1.8),
    ]

    seed_root = 20260426
    pipeline_seed_results: dict[str, list[dict[str, float]]] = {}
    flat_rows: list[dict[str, object]] = []
    for pipeline in pipelines:
        results = run_pipeline_mc(pipeline, chart, cfg, seed_root)
        pipeline_seed_results[pipeline.name] = results
        for seed_idx, r in enumerate(results):
            flat = {"pipeline": pipeline.name, "seed_idx": seed_idx}
            flat.update({k: v for k, v in r.items()})
            flat_rows.append(flat)

    # Two-pipeline ratio.
    name_lo, name_hi = pipelines[0].name, pipelines[1].name
    k_lo = np.array([r["k_emp"] for r in pipeline_seed_results[name_lo]])
    k_hi = np.array([r["k_emp"] for r in pipeline_seed_results[name_hi]])
    ratios = k_hi / k_lo
    theory_ratio = (pipelines[0].sigma_0 / pipelines[1].sigma_0) ** (1.0 / (pipelines[0].p - 1.0))
    ratio_summary = {
        "pipeline_lo": name_lo,
        "pipeline_hi": name_hi,
        "theory_K_hi_over_lo": theory_ratio,
        "median_K_hi_over_lo": float(np.median(ratios)),
        "p10_K_hi_over_lo": float(np.percentile(ratios, 10)),
        "p90_K_hi_over_lo": float(np.percentile(ratios, 90)),
        "n_seeds": cfg.n_seeds,
    }

    # Representative atlas snapshot (one seed of pipeline_lo).
    rng = np.random.default_rng(seed_root)
    edges = y_bin_edges(cfg.t_min, cfg.t_max, chart, cfg.n_y_bins)
    y_eval = y_eval_grid(cfg.t_min, cfg.t_max, chart, cfg.y_eval_points)
    t, y_true, y_obs = sample_observations(
        pipelines[0], chart, rng, cfg.n_obs, cfg.t_min, cfg.t_max
    )
    t_eval = chart.t_of_y(y_eval)
    y_hat_k, se_k = chart_kernel(t, y_obs, t_eval, cfg.kernel_bandwidth_log_t)
    y_hat_b, se_b = chart_binned_median(t, y_obs, t_eval, cfg.bin_width_log_t)
    gamma = gamma_atlas(y_hat_k, se_k, y_hat_b, se_b)
    atlas_rows = [
        {
            "pipeline": pipelines[0].name,
            "y_eval": float(y_eval[i]),
            "y_hat_kernel": float(y_hat_k[i]),
            "y_hat_binned_median": float(y_hat_b[i]),
            "stderr_kernel": float(se_k[i]),
            "stderr_binned_median": float(se_b[i]),
            "gamma": float(gamma[i]),
        }
        for i in range(len(y_eval))
    ]

    # Summaries.
    full_summary: dict[str, object] = {
        "contract": "two-pipeline apparatus-bound K simulation",
        "allowed_claim": (
            "The two-pipeline apparatus-bound mechanism produces the predicted "
            "K_2 / K_1 ratio under explicit forward-model noise, and the §7 atlas-"
            "coherence cutoff distinguishes a reliability floor from chart fracture."
        ),
        "forbidden_claim": (
            "This simulation validates AOC against any real cosmological dataset "
            "or proves apparatus-bound K as a property of nature."
        ),
        "chart": {"A": chart.A, "alpha": chart.alpha},
        "config": cfg.__dict__,
        "pipelines": [{"name": p.name, "sigma_0": p.sigma_0, "p": p.p} for p in pipelines],
        "per_pipeline": {
            p.name: summarize_mc(pipeline_seed_results[p.name]) for p in pipelines
        },
        "ratio": ratio_summary,
    }

    write_seed_table(flat_rows)
    write_ratio_table([ratio_summary])
    write_atlas_table(atlas_rows)
    SUMMARY_PATH.write_text(json.dumps(full_summary, indent=2), encoding="utf-8")
    maybe_plot(
        pipelines,
        pipeline_seed_results,
        chart,
        cfg,
        {"y_eval": y_eval, "gamma": gamma, "pipeline": pipelines[0].name},
    )

    print(f"Wrote {RESULTS_PATH}")
    print(f"Wrote {RATIO_PATH}")
    print(f"Wrote {ATLAS_PATH}")
    print(f"Wrote {SUMMARY_PATH}")
    if PLOT_PATH.exists():
        print(f"Wrote {PLOT_PATH}")
    print()
    print(
        f"theory K_hi/K_lo = {theory_ratio:.4g}, "
        f"median empirical K_hi/K_lo = {np.median(ratios):.4g} "
        f"(p10={np.percentile(ratios, 10):.4g}, p90={np.percentile(ratios, 90):.4g})"
    )


if __name__ == "__main__":
    main()
