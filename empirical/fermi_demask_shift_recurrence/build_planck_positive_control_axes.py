"""Build SharedShift axis rows from the landed Planck demask-shift summaries.

This is the positive-control adapter for the Fermi demask-shift recurrence
contract. It does not touch Fermi data. It converts the already-landed Planck
unmasked and galcut20 low-ell operator axes into the generic axis CSV expected
by `shared_shift_metric.py`.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = (
    ROOT
    / "data"
    / "derived"
    / "fermi_demask_shift_recurrence"
    / "planck_positive_control_axes.csv"
)

INPUTS = {
    "M0": {
        "ell2": ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64"
        / "directional_quadrupole_mlmax_summary.json",
        "ell3": ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64"
        / "directional_octupole_axis_summary.json",
    },
    "M1": {
        "ell2": ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64_galcut20"
        / "directional_quadrupole_mlmax_summary.json",
        "ell3": ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64_galcut20"
        / "directional_octupole_axis_summary.json",
    },
}

OPERATORS = ["Commander", "NILC", "SEVEM", "SMICA"]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def lb_to_cart(l_deg: float, b_deg: float) -> tuple[float, float, float]:
    lon = math.radians(l_deg)
    lat = math.radians(b_deg)
    return (
        math.cos(lat) * math.cos(lon),
        math.cos(lat) * math.sin(lon),
        math.sin(lat),
    )


def build_rows() -> list[dict[str, str | float]]:
    rows: list[dict[str, str | float]] = []
    for mask, band_paths in INPUTS.items():
        for band, path in band_paths.items():
            payload = load_json(path)
            for operator in OPERATORS:
                axis = payload["operator_axes"][operator]
                x, y, z = lb_to_cart(float(axis["l_deg"]), float(axis["b_deg"]))
                rows.append(
                    {
                        "voice": operator,
                        "mask": mask,
                        "band": band,
                        "x": x,
                        "y": y,
                        "z": z,
                        "grade": "A",
                    }
                )
    return rows


def write_rows(path: Path, rows: list[dict[str, str | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["voice", "mask", "band", "x", "y", "z", "grade"]
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    rows = build_rows()
    write_rows(args.out_csv, rows)
    print(f"wrote {len(rows)} Planck positive-control axis rows to {args.out_csv}")


if __name__ == "__main__":
    main()

