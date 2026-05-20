"""Plot pair-count histograms for Sprint D voice-leading sim-null.

Reads the four main batch summaries plus the four sensitivity batches and
produces side-by-side histograms with the observed Planck value (6 pairs at
ell=3, 2 pairs at ell=2) marked.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SIM_NULL = ROOT / "reports" / "planck_operator_residue" / "voice_leading_sim_null"


def load(rel: str) -> dict:
    return json.loads((SIM_NULL / rel).read_text())


def dist_array(d: dict) -> np.ndarray:
    counts = d["parallel_fifths_pair_counts_distribution"]
    return np.array([counts.get(str(k), 0.0) for k in range(7)])


def plot_panel(
    ax,
    arrays: list[tuple[str, np.ndarray, str]],
    observed: int,
    title: str,
) -> None:
    x = np.arange(7)
    width = 0.27
    offsets = np.linspace(-(len(arrays) - 1) / 2, (len(arrays) - 1) / 2, len(arrays))
    for i, (label, arr, color) in enumerate(arrays):
        ax.bar(
            x + offsets[i] * width,
            arr,
            width=width,
            label=label,
            color=color,
            edgecolor="#222",
            linewidth=0.4,
        )
    ax.axvline(observed, color="#c43c3c", linestyle="--", linewidth=1.4,
               label=f"observed Planck ({observed})")
    ax.set_xlabel("# voice pairs triggering parallel-fifths")
    ax.set_ylabel("fraction of 1000 realizations")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.3, linewidth=0.4)


def main() -> None:
    main_g3 = load("main/galcut20_ell3/voice_leading_sim_null_summary.json")
    main_n3 = load("main/none_ell3/voice_leading_sim_null_summary.json")
    main_g2 = load("main/galcut20_ell2/voice_leading_sim_null_summary.json")
    main_n2 = load("main/none_ell2/voice_leading_sim_null_summary.json")

    sens_g3_05 = load("sensitivity/galcut20_ell3_n0p5/voice_leading_sim_null_summary.json")
    sens_g3_20 = load("sensitivity/galcut20_ell3_n2p0/voice_leading_sim_null_summary.json")
    sens_n3_05 = load("sensitivity/none_ell3_n0p5/voice_leading_sim_null_summary.json")
    sens_n3_20 = load("sensitivity/none_ell3_n2p0/voice_leading_sim_null_summary.json")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    plot_panel(
        axes[0, 0],
        [
            ("galcut20 (n=1.0x)", dist_array(main_g3), "#3358c4"),
            ("none (n=1.0x)", dist_array(main_n3), "#c4a833"),
        ],
        observed=6,
        title="ell=3 main run (noise_scale=1.0)",
    )
    plot_panel(
        axes[0, 1],
        [
            ("galcut20 (n=1.0x)", dist_array(main_g2), "#3358c4"),
            ("none (n=1.0x)", dist_array(main_n2), "#c4a833"),
        ],
        observed=2,
        title="ell=2 main run (noise_scale=1.0)",
    )
    plot_panel(
        axes[1, 0],
        [
            ("n=0.5x", dist_array(sens_g3_05), "#5c8de0"),
            ("n=1.0x", dist_array(main_g3), "#3358c4"),
            ("n=2.0x", dist_array(sens_g3_20), "#1d3a8a"),
        ],
        observed=6,
        title="ell=3 galcut20 sensitivity sweep",
    )
    plot_panel(
        axes[1, 1],
        [
            ("n=0.5x", dist_array(sens_n3_05), "#e0c25c"),
            ("n=1.0x", dist_array(main_n3), "#c4a833"),
            ("n=2.0x", dist_array(sens_n3_20), "#8a751d"),
        ],
        observed=6,
        title="ell=3 no-mask sensitivity sweep",
    )

    fig.suptitle(
        "Sprint D voice-leading sim-null: parallel-fifths pair-count distribution\n"
        "1000 LCDM low-ell realizations + surrogate operator noise; "
        "observed Planck = 6/6 at ell=3 galcut20",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_path = SIM_NULL / "voice_leading_sim_null_histogram_ell3.png"
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
