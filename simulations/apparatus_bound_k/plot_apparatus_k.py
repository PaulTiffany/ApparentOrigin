"""Plot the apparatus-bound K toy sweep."""

from __future__ import annotations

import csv
from pathlib import Path


def read_sweep(path: Path) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [
            {
                "sigma_0": float(row["sigma_0"]),
                "K": float(row["K"]),
                "t_K": float(row["t_K"]),
            }
            for row in csv.DictReader(handle)
        ]


def main() -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("matplotlib is not installed; run apparatus_k.py for CSV output.") from exc

    root = Path(__file__).parent
    sweep_path = root / "apparatus_k_sweep.csv"
    if not sweep_path.exists():
        raise SystemExit("Run apparatus_k.py before plotting.")

    rows = read_sweep(sweep_path)
    sigma = [row["sigma_0"] for row in rows]
    k_values = [row["K"] for row in rows]
    t_values = [row["t_K"] for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=160)

    axes[0].plot(sigma, k_values, marker="o", color="#1d7f8c")
    axes[0].invert_xaxis()
    axes[0].set_xlabel("pipeline noise sigma_0")
    axes[0].set_ylabel("K")
    axes[0].set_title("Better pipeline -> larger K")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(sigma, t_values, marker="o", color="#d28f2d")
    axes[1].invert_xaxis()
    axes[1].set_xlabel("pipeline noise sigma_0")
    axes[1].set_ylabel("t_K")
    axes[1].set_title("Better pipeline -> earlier t_K")
    axes[1].grid(True, alpha=0.25)

    fig.tight_layout()
    output_path = root / "apparatus_k_sweep.png"
    fig.savefig(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

