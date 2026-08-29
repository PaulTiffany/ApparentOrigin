#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${MAP_DIR:-}" ]]; then
  echo "MAP_DIR is required" >&2
  exit 2
fi

if [[ -z "${MASK_PATH:-}" ]]; then
  echo "MASK_PATH is required" >&2
  exit 2
fi

NSIDE_OUT="${NSIDE_OUT:-64}"
LMAX="${LMAX:-30}"
OUT_ROOT="reports/planck_operator_residue/operator_prism_contract/healpy_official_mask"

python empirical/planck_operator_residue/extract_planck_lowell_healpy_morphology.py \
  --map-dir "$MAP_DIR" \
  --mask "$MASK_PATH" \
  --out-dir "$OUT_ROOT" \
  --nside-out "$NSIDE_OUT" \
  --lmax "$LMAX"

python empirical/planck_operator_residue/directional_residue_axis_octupole.py \
  --input "$OUT_ROOT/planck_lowell_healpy_official_mask_base.csv" \
  --outdir "$OUT_ROOT/base_ell3" \
  --nside "$NSIDE_OUT"

python empirical/planck_operator_residue/directional_residue_axis_octupole.py \
  --input "$OUT_ROOT/planck_lowell_healpy_official_mask_dilate1.csv" \
  --outdir "$OUT_ROOT/dilate1_ell3" \
  --nside "$NSIDE_OUT"

python empirical/planck_operator_residue/evaluate_operator_prism_contract.py \
  --contract-summary "base=$OUT_ROOT/base_ell3/directional_octupole_axis_summary.json" \
  --contract-summary "dilate1=$OUT_ROOT/dilate1_ell3/directional_octupole_axis_summary.json"
