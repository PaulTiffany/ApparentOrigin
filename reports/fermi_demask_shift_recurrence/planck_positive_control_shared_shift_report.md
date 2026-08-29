# Planck Positive-Control SharedShift Run

Status: executed positive-control run for the Fermi demask-shift recurrence
contract.

Phase: empirical-control bridge. This is a Planck positive-control execution,
not a Fermi result.

Inputs:

```text
reports/planck_operator_residue/directional_axis_nside64/
reports/planck_operator_residue/directional_axis_nside64_galcut20/
```

Generated axis table:

```text
data/derived/fermi_demask_shift_recurrence/planck_positive_control_axes.csv
```

Metric output:

```text
reports/fermi_demask_shift_recurrence/planck_positive_control_shared_shift.csv
```

Command:

```text
python empirical/fermi_demask_shift_recurrence/build_planck_positive_control_axes.py
python empirical/fermi_demask_shift_recurrence/shared_shift_metric.py \
  --axes-csv data/derived/fermi_demask_shift_recurrence/planck_positive_control_axes.csv \
  --transitions M0:M1 \
  --out-csv reports/fermi_demask_shift_recurrence/planck_positive_control_shared_shift.csv
```

Here:

```text
M0 = Planck unmasked fallback nside64 directional axes
M1 = Planck galcut20 fallback nside64 directional axes
```

## Result

| transition | band | voices | valid r axes | D_op | D_motion MAD | R_axis | median Delta | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| M0 -> M1 | ell2 | 4 | 4 | 4.615 deg | 2.526 deg | 0.845 | 27.360 deg | numeric only, no nulls |
| M0 -> M1 | ell3 | 4 | 4 | 5.112 deg | 0.485 deg | 0.869 | 22.490 deg | numeric only, no nulls |

Readout:

1. The Planck positive-control adapter reproduces the expected demask-shift
   shape: all four operator voices move nontrivially under `unmasked ->
   galcut20`.
2. The ell=3 motion is the cleaner positive-control signal: motion magnitudes
   are tightly matched (`D_motion MAD = 0.485 deg`) and rotation axes are
   concentrated (`R_axis = 0.869`).
3. The ell=2 motion is still coherent but less block-like: SEVEM carries a
   larger motion, which raises `D_motion MAD` to `2.526 deg`.

This supports using the Planck lane as a positive-control detector for the
future Fermi run. It does not provide a Fermi verdict.

## Relation to Counterpoint Rerun

The same execution also reran:

```text
empirical/planck_operator_residue/counterpoint_voice_leading.py
```

Output:

```text
reports/planck_operator_residue/counterpoint_voice_leading_rerun_2026_05_20/
```

The rerun preserved the prior qualitative read: all six ell=3 voice pairs
trigger the parallel-fifths diagnostic, while ell=2 is partly independent with
SEVEM as the larger-motion outlier.

## Allowed Claims

1. The generic SharedShift detector runs on the Planck demask positive-control
   axis rows.
2. The Planck positive-control reproduces coherent shared motion, especially
   at ell=3.
3. The result is a readiness gate for the Fermi branch.

## Forbidden Claims

1. This is not a Fermi detection.
2. This does not prove AOC.
3. This does not convert the sonification or light rendering into evidence.
4. The numeric-only verdict is not a calibrated null percentile.

