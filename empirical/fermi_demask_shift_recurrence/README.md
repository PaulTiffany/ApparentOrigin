# Fermi Demask-Shift Recurrence Branch

Status: pre-run scaffold.

Purpose:

Test whether independent-enough Fermi gamma-ray sky reconstructions share a
directional motion under Galactic-plane mask transitions.

This branch inherits its discipline from the Planck operator-residue branch:

```text
same target -> multiple reconstruction operators -> stable or unstable residue
```

The Fermi version asks:

```text
same gamma-ray sky -> multiple residual-map voices -> mask/demask transition
-> shared or ordinary directional motion
```

Contract:

```text
docs/fermi_demask_shift_recurrence_contract.md
```

Initial metric scaffold:

```text
shared_shift_metric.py
voice_independence_ledger_template.csv
```

The metric script expects declared axis rows:

```text
voice,mask,band,x,y,z,grade
```

Example call:

```text
python empirical/fermi_demask_shift_recurrence/shared_shift_metric.py ^
  --axes-csv data/derived/fermi_demask_shift_recurrence/axes.csv ^
  --out-csv reports/fermi_demask_shift_recurrence/shared_shift_metrics.csv
```

Smoke-test call using the synthetic example rows:

```text
python empirical/fermi_demask_shift_recurrence/shared_shift_metric.py ^
  --axes-csv empirical/fermi_demask_shift_recurrence/example_axes.csv ^
  --transitions M0:M1 ^
  --out-csv reports/fermi_demask_shift_recurrence/example_shared_shift_metrics.csv
```

## Required Gates

1. The Planck positive-control detector must reproduce the prior Planck
   shared-shift / voice-leading pattern.
2. The Fermi voice-independence ledger must be frozen before live analysis.
3. The Fermi map family, energy bands, exposure treatment, diffuse models,
   source masks, and low-order extractor must be declared before evaluation.
4. Numeric SharedShift metrics and nulls must be reported before any
   sonification.

## Expected Files

Raw provenance:

```text
data/raw/fermi_demask_shift_recurrence/PROVENANCE.md
```

Future derived products:

```text
data/derived/fermi_demask_shift_recurrence/
```

Future reports:

```text
reports/fermi_demask_shift_recurrence/
```

## Allowed Claims

1. This branch defines a Fermi operator-residue experiment.
2. The target object is shared mask-induced motion before sound.
3. Fermi is an instrument-forward reconstruction domain.

## Forbidden Claims

1. Fermi validates AOC.
2. Gamma-ray residuals prove a cosmological recurrence.
3. Sonification proves the metric.
4. Endpoint clustering alone is success.
