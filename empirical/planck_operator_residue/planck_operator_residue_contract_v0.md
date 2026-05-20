# Planck Operator-Residue Contract v0

Status: pre-data empirical contract.

Purpose:

Define the first AOC-aligned Planck test before inspecting Planck residuals.

## 1. Scientific Question

Plain English:

> If the same CMB sky is reconstructed by four different operators, do the
> largest-scale structures remain stable in a way that is stronger than
> ordinary pipeline variation?

AOC reading:

> Operator-stable low-order residue is a candidate signature of boundary
> structure in the observer reconstruction, not direct evidence of
> pre-boundary reality.

Standard cosmology reading:

> Low-ell features may arise from cosmic variance, foreground residuals,
> component-separation choices, masks, noise, or a posteriori statistic
> selection.

This contract must distinguish those readings before making any strong claim.

## 2. Data Products

Primary products:

```text
COM_CMB_IQU-commander_2048_R3.00_full.fits
COM_CMB_IQU-nilc_2048_R3.00_full.fits
COM_CMB_IQU-sevem_2048_R3.00_full.fits
COM_CMB_IQU-smica_2048_R3.00_full.fits
```

Primary field:

```text
I_STOKES
```

Initial multipole band:

```text
2 <= ell <= 30
```

Initial analysis layer:

```text
low-ell spherical harmonic coefficients a_lm
```

## 3. Predeclared Metrics

For each operator and multipole:

1. `C_ell`, using the real-map convention:

   ```text
   C_ell = (|a_l0|^2 + 2 * sum_{m>0} |a_lm|^2) / (2ell + 1)
   ```

2. Normalized spectral entropy:

   ```text
   H_ell / log(2ell + 1)
   ```

3. Odd/even low-ell parity ratio:

   ```text
   sum_{ell odd} C_ell / sum_{ell even} C_ell
   ```

Across operators:

4. Pairwise coefficient-distance by `ell`:

   ```text
   d_ij(ell) =
     sqrt(
       sum_m w_m |a_i,lm - a_j,lm|^2
       /
       sum_m w_m (|a_i,lm|^2 + |a_j,lm|^2) / 2
     )
   ```

   with `w_0 = 1` and `w_m = 2` for `m > 0`.

5. Operator-residue stability score:

   ```text
   median pairwise d_ij(ell) over 2 <= ell <= 30
   ```

## 4. Primary Outcome

The primary outcome is not whether an anomaly exists.

The primary outcome is:

```text
Does a predeclared low-ell residue remain stable across Commander, NILC, SEVEM,
and SMICA?
```

Possible outcomes:

1. **Stable across operators.**
   Candidate sky-level feature. Needs cosmic-variance and mask controls.

2. **Unstable across operators.**
   Likely component-separation or foreground-pipeline residue.

3. **Metric-dependent.**
   The statistic is not robust enough; revise the contract before further
   data contact.

4. **Inconclusive.**
   Dependency, masking, beam, or coefficient-extraction issues prevent a clean
   result.

## 5. Required Controls

Before any physical interpretation:

1. Compare full-sky/inpainted and masked coefficients where possible.
2. Repeat at multiple downgrade/smoothing choices.
3. Use simulations or phase-randomized nulls.
4. Check known low-ell anomaly literature before naming a new effect.
5. Confirm the statistic was chosen before seeing the result.

First null now implemented:

```text
empirical/planck_operator_residue/phase_null_operator_residue.py
```

This coefficient-level null preserves each operator's low-ell coefficient
amplitudes and randomizes cross-operator phases. It tests whether the measured
operator closeness depends on phase alignment rather than power alone.

## 6. AOC Interpretation Rule

Allowed:

> A stable operator residue is a candidate reconstruction-horizon observable
> worth testing against standard CMB controls.

Forbidden:

> A stable operator residue proves a torqued horizon, white-hole leakage,
> false-bottom cosmology, or AOC.

## 7. Failure Condition

This map fails as an AOC empirical target if:

1. the residue is dominated by one component-separation pipeline,
2. the result disappears under reasonable masks or smoothing,
3. the statistic only works after being tuned post hoc,
4. standard simulations produce comparable stability at ordinary rates.

## 8. Next Implementation Step

Export a coefficient table:

```text
operator,ell,m,alm_real,alm_imag
```

Then run:

```text
python empirical/planck_operator_residue/analyze_lowell_operator_residue.py ^
  --input data/derived/planck_operator_residue/planck_lowell_alm.csv ^
  --outdir reports/planck_operator_residue
```

The repo includes an extraction script for the coefficient table:

```text
empirical/planck_operator_residue/extract_planck_lowell.py
```

This script requires `healpy` and the actual Planck FITS maps. The current local
environment does not have `healpy`, so the contract is staged at the coefficient
table boundary until dependencies are installed.
