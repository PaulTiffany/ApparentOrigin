#!/usr/bin/env bash
set -euo pipefail

MAP_DIR="data/raw/planck_operator_residue/maps"
MASK_DIR="data/raw/planck_operator_residue/masks"
mkdir -p "$MAP_DIR" "$MASK_DIR"

MAP_BASE="https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/cmb"
MASK_BASE="https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/masks"

download_if_needed() {
  local url="$1"
  local out="$2"
  local min_bytes="$3"

  if [[ -f "$out" ]]; then
    local size
    size="$(wc -c < "$out")"
    if [[ "$size" -ge "$min_bytes" ]]; then
      echo "Using cached $(basename "$out") ($size bytes)"
      return
    fi
    echo "Removing incomplete $(basename "$out") ($size bytes)"
    rm -f "$out"
  fi

  echo "Downloading $url"
  curl -L --fail --retry 5 --retry-delay 10 --continue-at - --output "$out" "$url"
}

download_if_needed \
  "$MAP_BASE/COM_CMB_IQU-commander_2048_R3.00_full.fits" \
  "$MAP_DIR/COM_CMB_IQU-commander_2048_R3.00_full.fits" \
  100000000

download_if_needed \
  "$MAP_BASE/COM_CMB_IQU-nilc_2048_R3.00_full.fits" \
  "$MAP_DIR/COM_CMB_IQU-nilc_2048_R3.00_full.fits" \
  100000000

download_if_needed \
  "$MAP_BASE/COM_CMB_IQU-sevem_2048_R3.00_full.fits" \
  "$MAP_DIR/COM_CMB_IQU-sevem_2048_R3.00_full.fits" \
  100000000

download_if_needed \
  "$MAP_BASE/COM_CMB_IQU-smica_2048_R3.00_full.fits" \
  "$MAP_DIR/COM_CMB_IQU-smica_2048_R3.00_full.fits" \
  100000000

download_if_needed \
  "$MASK_BASE/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits" \
  "$MASK_DIR/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits" \
  100000000

du -h data/raw/planck_operator_residue
