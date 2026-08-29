#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-smoke}"
AXES_CSV_URL="${2:-}"
TRANSITIONS="${3:-M0:M1,M1:M2,M2:M3,M0:M2,M0:M4}"

python cloud_run/fermi_demask_shift/fermi_shared_shift_runner.py \
  --mode "${MODE}" \
  --axes-csv-url "${AXES_CSV_URL}" \
  --transitions "${TRANSITIONS}" \
  --out-dir reports/fermi_demask_shift_recurrence/ci_runner

