"""Plot the false-bottom projection toy model."""

from __future__ import annotations

from pathlib import Path

from false_bottom import sample_projection


def main() -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is not installed. Run false_bottom.py to generate CSV "
            "data, or install matplotlib to create the PNG plot."
        ) from exc

    rows = sample_projection()
    u = [row["u"] for row in rows]
    q = [row["observed_q"] for row in rows]
    floor = [row["epsilon_floor"] for row in rows]

    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=160)
    ax.plot(u, u, color="#8c8c8c", linewidth=1.2, linestyle="--", label="identity")
    ax.plot(u, q, color="#d28f2d", linewidth=2.4, label="observer quotient")
    ax.plot(u, floor, color="#1d7f8c", linewidth=1.2, label="epsilon floor")
    ax.fill_between(u, floor, q, where=[value < 1.4 for value in q], color="#d28f2d", alpha=0.16)

    ax.set_title("False-Bottom Projection Toy Model")
    ax.set_xlabel("underlying coordinate u")
    ax.set_ylabel("observed reconstruction q(u)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.22)

    output_path = Path(__file__).with_name("false_bottom_projection.png")
    fig.tight_layout()
    fig.savefig(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

