# Fermi Demask-Shift CI Runner Report

Mode: `axes_csv_url`.

Status: CI metric run. Smoke mode is not a Fermi result.

| transition | band | voices | valid r axes | D_op | D_motion MAD | R_axis | median Delta | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| M0->M1 | ell2 | 4 | 4 | 4.615 | 2.526 | 0.845 | 27.360 | numeric_only_no_nulls |
| M1->M2 | ell2 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M2->M3 | ell2 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M0->M2 | ell2 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M0->M4 | ell2 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M0->M1 | ell3 | 4 | 4 | 5.112 | 0.485 | 0.869 | 22.490 | numeric_only_no_nulls |
| M1->M2 | ell3 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M2->M3 | ell3 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M0->M2 | ell3 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |
| M0->M4 | ell3 | 0 | 0 | nan | nan | nan | nan | numeric_only_no_nulls |

## Allowed Claims

1. The CI runner executed the SharedShift metric.
2. The artifact is suitable for Desktop GPT inspection.

## Forbidden Claims

1. Smoke mode is not a Fermi detection.
2. Numeric-only output is not a calibrated null percentile.
3. Workflow success is not evidence for AOC.
