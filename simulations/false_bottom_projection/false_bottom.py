"""Toy false-bottom projection model.

This module intentionally uses only the Python standard library so it can run in
minimal environments. It writes CSV data for the shifted-softplus observer
quotient used in the canonical proof spine.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


DEFAULT_EPSILON = 1.0
DEFAULT_DELTA = 0.12
DEFAULT_MIN_U = -3.0
DEFAULT_MAX_U = 5.0
DEFAULT_STEPS = 400


def shifted_softplus(u: float, epsilon: float, delta: float) -> float:
    """Return epsilon + delta * log(1 + exp((u - epsilon) / delta)).

    The implementation is numerically stable for large positive and negative
    arguments.
    """

    if delta <= 0:
        raise ValueError("delta must be positive")

    x = (u - epsilon) / delta
    if x > 50:
        return epsilon + delta * x
    if x < -50:
        return epsilon
    return epsilon + delta * math.log1p(math.exp(x))


def sample_projection(
    epsilon: float = DEFAULT_EPSILON,
    delta: float = DEFAULT_DELTA,
    min_u: float = DEFAULT_MIN_U,
    max_u: float = DEFAULT_MAX_U,
    steps: int = DEFAULT_STEPS,
) -> list[dict[str, float]]:
    """Sample the underlying coordinate and observed quotient."""

    if steps < 2:
        raise ValueError("steps must be at least 2")
    if max_u <= min_u:
        raise ValueError("max_u must exceed min_u")

    rows: list[dict[str, float]] = []
    for i in range(steps + 1):
        u = min_u + (max_u - min_u) * i / steps
        q = shifted_softplus(u, epsilon, delta)
        rows.append(
            {
                "u": u,
                "observed_q": q,
                "epsilon_floor": epsilon,
                "residue": q - u,
            }
        )
    return rows


def write_csv(rows: list[dict[str, float]], output_path: Path) -> None:
    """Write sampled rows to CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["u", "observed_q", "epsilon_floor", "residue"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    output_path = Path(__file__).with_name("false_bottom_samples.csv")
    rows = sample_projection()
    write_csv(rows, output_path)
    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()

