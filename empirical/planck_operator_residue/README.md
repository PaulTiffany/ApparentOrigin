# Planck Operator-Residue Branch

Status: contract scaffold plus dependency-light low-ell analyzer.

Purpose:

Test an AOC-aligned question on public CMB data:

> When the same sky is reconstructed by different Planck component-separation
> operators, which low-order structures remain stable and which are
> operator-bound?

This branch is not a claim that CMB anomalies validate AOC. It is a controlled
operator-residue test.

## Why This Branch Exists

The Principia-aligned AOC frame says the clean first question is not:

```text
can one deformation shift every cosmological distance curve?
```

It is:

```text
same target -> different reconstruction operators -> stable or unstable residue
```

Planck is a good first target because the 2018 CMB products include four
component-separated maps of the same sky:

```text
Commander
NILC
SEVEM
SMICA
```

These are explicit reconstruction operators. That makes them a natural
laboratory for AOC's observer-operator discipline.

## Files

```text
planck_operator_residue_contract_v0.md
extract_planck_lowell.py
extract_planck_lowell_fallback.py
analyze_lowell_operator_residue.py
phase_null_operator_residue.py
requirements.txt
```

Raw provenance lives under:

```text
data/raw/planck_operator_residue/PROVENANCE.md
```

Expected derived coefficient table:

```text
data/derived/planck_operator_residue/planck_lowell_alm.csv
```

Expected report:

```text
reports/planck_operator_residue/planck_operator_residue_report.md
```

## Current Environment Note

This machine currently has `numpy`, but not `healpy` or `astropy`. Therefore
this branch starts at the low-ell coefficient layer. A later map-extraction
step should use `healpy` to read the Planck FITS maps, apply masks and
smoothing, and export a table with:

```text
operator,ell,m,alm_real,alm_imag
```

The provided analyzer runs on that table without needing FITS or HEALPix.

## Intended End-to-End Run

After downloading the four Planck PR3 full-mission maps into a local map
directory and installing `healpy`:

```text
python empirical/planck_operator_residue/extract_planck_lowell.py ^
  --map-dir data/raw/planck_operator_residue/maps ^
  --output data/derived/planck_operator_residue/planck_lowell_alm.csv
```

Then:

```text
python empirical/planck_operator_residue/analyze_lowell_operator_residue.py ^
  --input data/derived/planck_operator_residue/planck_lowell_alm.csv ^
  --outdir reports/planck_operator_residue
```

Fallback path if `healpy` is unavailable:

```text
py -3.11 empirical/planck_operator_residue/extract_planck_lowell_fallback.py ^
  --map-dir data/raw/planck_operator_residue/maps ^
  --output data/derived/planck_operator_residue/planck_lowell_alm_fallback.csv
```

The fallback uses `astropy`, `astropy-healpix`, and direct low-resolution
quadrature. Treat its outputs as approximate first-contact results, not final
Planck harmonic analysis.

## First Null Control

After exporting coefficients, run:

```text
py -3.11 empirical/planck_operator_residue/phase_null_operator_residue.py ^
  --input data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv ^
  --outdir reports/planck_operator_residue/phase_null_nside64
```

This preserves each operator's coefficient amplitudes and randomizes phase
alignment. It is a coefficient-level control, not a full CMB simulation.

## Allowed Claims

1. AOC can define an operator-residue contract on Planck component-separated
   maps.
2. The contract tests whether low-order CMB structures are stable across
   reconstruction operators.
3. Stable residue would be a candidate boundary-adjacent phenomenon requiring
   ordinary CMB controls.

## Forbidden Claims

1. Planck proves AOC.
2. Low-ell anomalies prove a false bottom.
3. Operator stability proves cosmic torque.
4. AOC refutes `LambdaCDM`.
