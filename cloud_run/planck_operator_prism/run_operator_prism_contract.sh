#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${MAP_DIR:-}" ]]; then
  echo "Set MAP_DIR to the directory containing the four Planck component-separated FITS maps." >&2
  exit 2
fi

if [[ -z "${MASK_PATH:-}" ]]; then
  echo "Set MASK_PATH to COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits." >&2
  exit 2
fi

OUT_ROOT="reports/planck_operator_residue/operator_prism_contract/healpy_official_mask"

python -m pip install -r cloud_run/planck_operator_prism/requirements.txt

python empirical/planck_operator_residue/extract_planck_lowell_healpy_morphology.py \
  --map-dir "$MAP_DIR" \
  --mask "$MASK_PATH" \
  --out-dir "$OUT_ROOT" \
  --nside-out 64 \
  --lmax 30

python empirical/planck_operator_residue/directional_residue_axis_octupole.py \
  --input "$OUT_ROOT/planck_lowell_healpy_official_mask_base.csv" \
  --outdir "$OUT_ROOT/base_ell3" \
  --nside 64

python empirical/planck_operator_residue/directional_residue_axis_octupole.py \
  --input "$OUT_ROOT/planck_lowell_healpy_official_mask_dilate1.csv" \
  --outdir "$OUT_ROOT/dilate1_ell3" \
  --nside 64

python empirical/planck_operator_residue/evaluate_operator_prism_contract.py \
  --contract-summary "base=$OUT_ROOT/base_ell3/directional_octupole_axis_summary.json" \
  --contract-summary "dilate1=$OUT_ROOT/dilate1_ell3/directional_octupole_axis_summary.json"
