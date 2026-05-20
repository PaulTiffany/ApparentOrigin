"""Evaluate readiness for the lambda_K Planck operator-prism contract.

This is a contract gate, not a discovery script. It may compute the
operator-prism coordinate for existing full summaries, but those retrospective
numbers do not count as the live contract result unless the extractor and mask
state match the predeclared contract.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from itertools import combinations
from pathlib import Path
from statistics import median
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
D_ISO_DEG = 57.0
OPERATORS = ("Commander", "NILC", "SEVEM", "SMICA")

DEFAULT_OUT = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "operator_prism_contract"
)
DEFAULT_MORPHOLOGY_AXES = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_official_mask_morphology"
    / "directional_axis_official_mask_morphology_axes.csv"
)
DEFAULT_RETROSPECTIVE_SUMMARIES = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_nside64"
    / "directional_octupole_axis_summary.json",
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_nside64_galcut20"
    / "directional_octupole_axis_summary.json",
)


def parse_label_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected LABEL=PATH")
    label, path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise argparse.ArgumentTypeError("empty label")
    return label, Path(path)


def lb_to_cart(l_deg: float, b_deg: float) -> tuple[float, float, float]:
    lon = math.radians(l_deg)
    lat = math.radians(b_deg)
    return (
        math.cos(lon) * math.cos(lat),
        math.sin(lon) * math.cos(lat),
        math.sin(lat),
    )


def axial_angle_deg(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> float:
    dot = abs(a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
    dot = min(1.0, max(-1.0, dot))
    return math.degrees(math.acos(dot))


def median_pairwise_axis_dispersion(axes: dict[str, dict[str, float]]) -> float | None:
    if len(axes) < 2:
        return None
    vectors = {
        name: lb_to_cart(float(axis["l_deg"]), float(axis["b_deg"]))
        for name, axis in axes.items()
    }
    distances = [
        axial_angle_deg(vectors[left], vectors[right])
        for left, right in combinations(vectors, 2)
    ]
    return float(median(distances))


def coordinate_from_dispersions(d_op: float | None, d_res: float | None) -> dict[str, Any]:
    if d_op is None or d_res is None:
        return {
            "complete": False,
            "d_op_deg": d_op,
            "d_res_deg": d_res,
            "s_op": None if d_op is None else 1.0 - d_op / D_ISO_DEG,
            "s_res": None if d_res is None else 1.0 - d_res / D_ISO_DEG,
            "c_axis": None,
        }
    s_op = 1.0 - d_op / D_ISO_DEG
    s_res = 1.0 - d_res / D_ISO_DEG
    return {
        "complete": True,
        "d_op_deg": d_op,
        "d_res_deg": d_res,
        "s_op": s_op,
        "s_res": s_res,
        "c_axis": s_op - s_res,
    }


def coordinate_from_full_summary(path: Path, label: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    summary = data.get("summary", {})
    d_op = summary.get("operator_axis_dispersion_deg", {}).get("median")
    d_res = summary.get("pair_residual_axis_dispersion_deg", {}).get("median")
    coord = coordinate_from_dispersions(d_op, d_res)
    coord.update(
        {
            "label": label,
            "path": str(path),
            "ell": data.get("ell"),
            "input": data.get("input"),
            "phase": "retrospective_context_only",
            "claim_status": "does_not_confirm_contract",
        }
    )
    return coord


def read_morphology_operator_axes(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {
            label: {
                "complete": False,
                "d_op_deg": None,
                "d_res_deg": None,
                "s_op": None,
                "s_res": None,
                "c_axis": None,
                "mask_label": label,
                "ell": 3,
                "operator_axes_present": [],
                "missing_operators": list(OPERATORS),
                "missing_contract_inputs": [
                    f"morphology operator axes file: {path}",
                    f"official-mask ell=3 pair-residue axes for {label}",
                ],
                "claim_status": "blocked_missing_morphology_axes",
            }
            for label in ("base", "dilate1")
        }

    rows_by_mask: dict[str, dict[str, dict[str, float]]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if int(row["ell"]) != 3:
                continue
            mask_label = row["mask_label"]
            operator = row["operator"]
            rows_by_mask.setdefault(mask_label, {})[operator] = {
                "l_deg": float(row["l_deg"]),
                "b_deg": float(row["b_deg"]),
            }

    targets: dict[str, dict[str, Any]] = {}
    for mask_label in ("base", "dilate1"):
        axes = rows_by_mask.get(mask_label, {})
        missing_operators = [op for op in OPERATORS if op not in axes]
        d_op = median_pairwise_axis_dispersion(axes) if not missing_operators else None
        coord = coordinate_from_dispersions(d_op=d_op, d_res=None)
        coord.update(
            {
                "mask_label": mask_label,
                "ell": 3,
                "operator_axes_present": sorted(axes),
                "missing_operators": missing_operators,
                "missing_contract_inputs": [
                    "official-mask ell=3 pair-residue axes",
                    "D_res(ell=3, official-mask-%s)" % mask_label,
                ],
                "claim_status": "blocked_missing_pair_residue_axes",
            }
        )
        targets[mask_label] = coord
    return targets


def merge_contract_summaries(
    targets: dict[str, dict[str, Any]],
    summary_specs: list[tuple[str, Path]] | None,
) -> dict[str, dict[str, Any]]:
    if not summary_specs:
        return targets
    merged = dict(targets)
    for label, path in summary_specs:
        if label not in ("base", "dilate1"):
            raise ValueError(f"unsupported contract label: {label}")
        coord = coordinate_from_full_summary(path, f"official_mask_{label}")
        coord.update(
            {
                "mask_label": label,
                "claim_status": "live_contract_input_present",
                "phase": "live_contract_input",
                "missing_contract_inputs": [],
            }
        )
        merged[label] = coord
    return merged


def live_verdict(targets: dict[str, dict[str, Any]]) -> str:
    required = ("base", "dilate1")
    if any(not targets.get(label, {}).get("complete") for label in required):
        return "blocked_missing_required_contract_inputs"
    if all(targets[label]["c_axis"] > 0.0 for label in required):
        return "contract_success_if_inputs_were_predeclared"
    return "contract_failure_if_inputs_were_predeclared"


def render_report(result: dict[str, Any]) -> str:
    complete_live = result["live_verdict"] != "blocked_missing_required_contract_inputs"
    lines = [
        "# lambda_K Operator-Prism Contract Gate",
        "",
        "Status: executable readiness gate for the Episode 4 Planck operator-prism contract.",
        "",
        "Phase: TTCS contract readiness. This report is not an observed-value claim and does not turn Episode 3 into a prediction.",
        "",
        "Contract coordinate:",
        "",
        "```text",
        "C_axis = (D_res - D_op) / 57 deg",
        "```",
        "",
        "Live predeclared target:",
        "",
        "```text",
        "C_axis(ell=3, official-mask-base) > 0",
        "and remains > 0 for official-mask-dilate1.",
        "```",
        "",
        "## Live Contract Gate",
        "",
        f"Verdict: `{result['live_verdict']}`.",
        "",
        "| mask | D_op | D_res | C_axis | status |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for label in ("base", "dilate1"):
        row = result["contract_targets"][label]
        d_op = "missing" if row["d_op_deg"] is None else f"{row['d_op_deg']:.3f}"
        d_res = "missing" if row["d_res_deg"] is None else f"{row['d_res_deg']:.3f}"
        c_axis = "missing" if row["c_axis"] is None else f"{row['c_axis']:.6f}"
        lines.append(
            f"| `{label}` | {d_op} | {d_res} | {c_axis} | `{row['claim_status']}` |"
        )

    if complete_live:
        lines.extend(
            [
                "",
                "The required official-mask ell=3 operator axes and pair-residue",
                "axes are present for both live masks. The verdict above is therefore",
                "an evaluation of the predeclared operator-prism channel contract.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "The official-mask morphology run currently supplies ell=3 operator axes,",
                "so `D_op` is computable. It does not yet supply the official-mask",
                "pair-residue axes required for `D_res`, so the live contract is not",
                "evaluated here.",
            ]
        )

    lines.extend(
        [
            "",
            "## Retrospective Context",
            "",
            "These rows use existing full summaries. They are coordinate checks only;",
            "they do not confirm the contract because they were not the predeclared",
            "official-mask base/dilate1 pair-residue run.",
            "",
            "| label | ell | D_op | D_res | C_axis | claim status |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["retrospective_contexts"]:
        d_op = "missing" if row["d_op_deg"] is None else f"{row['d_op_deg']:.3f}"
        d_res = "missing" if row["d_res_deg"] is None else f"{row['d_res_deg']:.3f}"
        c_axis = "missing" if row["c_axis"] is None else f"{row['c_axis']:.6f}"
        lines.append(
            f"| `{row['label']}` | {row.get('ell', '')} | {d_op} | {d_res} | {c_axis} | `{row['claim_status']}` |"
        )

    lines.extend(
        [
            "",
            "## Next Required Artifact",
            "",
            (
                "Archive the cloud artifact locally and run an independent replication "
                "or sensitivity check."
                if complete_live
                else "Run or implement official-mask pair-residue extraction for ell=3 at "
                "`base` and `dilate1`, with the extractor, mask family, sky fractions, "
                "and quality controls stated before evaluation."
            ),
            "",
            "## Allowed Claims",
            "",
            "1. The operator-prism coordinate has an executable readiness gate.",
            (
                "2. The live official-mask `base -> dilate1` run satisfies the sign "
                "condition for this Planck operator-prism channel."
                if complete_live
                else "2. Existing fallback summaries can be projected into the same coordinate for context."
            ),
            (
                "3. This is a channel-contract success, not an AOC confirmation."
                if complete_live
                else "3. The live Episode 4 contract remains blocked until official-mask pair-residue axes exist."
            ),
            "",
            "## Forbidden Claims",
            "",
            "1. The retrospective rows confirm `lambda_K`.",
            "2. A positive `C_axis` is AOC evidence.",
            "3. The missing `D_res` value may be inferred from operator-axis survival alone.",
            "4. Contract success derives an observed `lambda_K` amplitude.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--morphology-axes", type=Path, default=DEFAULT_MORPHOLOGY_AXES)
    parser.add_argument(
        "--retrospective-summary",
        type=Path,
        action="append",
        default=None,
        help="Full directional summary with operator and pair-residue dispersions.",
    )
    parser.add_argument(
        "--contract-summary",
        type=parse_label_path,
        action="append",
        default=None,
        metavar="LABEL=PATH",
        help="Live official-mask directional summary for base or dilate1.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    retrospective_paths = args.retrospective_summary or list(DEFAULT_RETROSPECTIVE_SUMMARIES)

    targets = merge_contract_summaries(
        read_morphology_operator_axes(args.morphology_axes),
        args.contract_summary,
    )
    contexts = []
    for path in retrospective_paths:
        if not path.exists():
            continue
        label = path.parent.name
        contexts.append(coordinate_from_full_summary(path, label))

    result = {
        "status": "lambda_K Planck operator-prism contract gate",
        "phase": "TTCS contract readiness, not observed-value derivation",
        "d_iso_deg": D_ISO_DEG,
        "morphology_axes_path": str(args.morphology_axes),
        "contract_targets": targets,
        "retrospective_contexts": contexts,
        "live_verdict": live_verdict(targets),
    }

    summary_path = args.out_dir / "operator_prism_contract_gate_summary.json"
    report_path = args.out_dir / "operator_prism_contract_gate_report.md"
    summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "live_verdict": result["live_verdict"],
                "summary": str(summary_path),
                "report": str(report_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
