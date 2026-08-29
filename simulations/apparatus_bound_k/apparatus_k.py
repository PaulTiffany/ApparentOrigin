"""Toy apparatus-bound K calculation.

This script implements the first calculable AOC K model:

    sigma_P(y) = sigma_0 * y**p
    K_P = (eta / sigma_0)**(1 / (p - 1))
    t_K = (A * K_P)**(-1 / alpha)

It intentionally avoids real cosmological data. The goal is to make the K
parameter operational in a controlled toy setting.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Pipeline:
    name: str
    sigma_0: float
    p: float


@dataclass(frozen=True)
class CosmologyChart:
    A: float = 1.0
    alpha: float = 0.5


def k_from_relative_error(sigma_0: float, p: float, eta: float) -> float:
    """Return K = (eta / sigma_0) ** (1 / (p - 1))."""

    if sigma_0 <= 0:
        raise ValueError("sigma_0 must be positive")
    if p <= 1:
        raise ValueError("p must exceed 1")
    if eta <= 0:
        raise ValueError("eta must be positive")
    return (eta / sigma_0) ** (1.0 / (p - 1.0))


def t_k_from_k(k_value: float, chart: CosmologyChart) -> float:
    """Return t_K = (A * K) ** (-1 / alpha)."""

    if k_value <= 0:
        raise ValueError("k_value must be positive")
    if chart.A <= 0:
        raise ValueError("A must be positive")
    if chart.alpha <= 0:
        raise ValueError("alpha must be positive")
    return (chart.A * k_value) ** (-1.0 / chart.alpha)


def evaluate_pipeline(pipeline: Pipeline, chart: CosmologyChart, eta: float) -> dict[str, float | str]:
    """Compute K and t_K for one pipeline."""

    k_value = k_from_relative_error(pipeline.sigma_0, pipeline.p, eta)
    t_k = t_k_from_k(k_value, chart)
    return {
        "pipeline": pipeline.name,
        "sigma_0": pipeline.sigma_0,
        "p": pipeline.p,
        "eta": eta,
        "A": chart.A,
        "alpha": chart.alpha,
        "K": k_value,
        "t_K": t_k,
    }


def write_rows(path: Path, rows: list[dict[str, float | str]]) -> None:
    """Write rows to CSV."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("rows cannot be empty")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def default_pipeline_rows() -> list[dict[str, float | str]]:
    """Return a small two-pipeline comparison."""

    chart = CosmologyChart(A=1.0, alpha=0.5)
    eta = 0.1
    pipelines = [
        Pipeline(name="baseline", sigma_0=0.010, p=1.8),
        Pipeline(name="improved", sigma_0=0.003, p=1.8),
    ]
    return [evaluate_pipeline(pipeline, chart, eta) for pipeline in pipelines]


def sweep_rows() -> list[dict[str, float | str]]:
    """Sweep sigma_0 to show how reconstruction quality changes K and t_K."""

    chart = CosmologyChart(A=1.0, alpha=0.5)
    eta = 0.1
    p = 1.8
    sigma_values = [0.030, 0.020, 0.010, 0.007, 0.005, 0.003, 0.002, 0.001]
    rows: list[dict[str, float | str]] = []
    for sigma_0 in sigma_values:
        rows.append(evaluate_pipeline(Pipeline(f"sigma_{sigma_0:g}", sigma_0, p), chart, eta))
    return rows


def main() -> None:
    root = Path(__file__).parent
    results_path = root / "apparatus_k_results.csv"
    sweep_path = root / "apparatus_k_sweep.csv"
    write_rows(results_path, default_pipeline_rows())
    write_rows(sweep_path, sweep_rows())
    print(f"Wrote {results_path}")
    print(f"Wrote {sweep_path}")


if __name__ == "__main__":
    main()

