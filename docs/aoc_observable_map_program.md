# AOC Observable Map Program

Status: canonical next-step program after the DESI DR2 BAO first pass.

Purpose:

Define how Apparent-Origin Cosmology moves from a reconstruction-horizon
thesis to probe-specific empirical predictions without assuming shared time,
shared distance, shared amplitude, or shared observer frame across instruments.

This document exists because the first DESI DR2 BAO gate rejected a simple
portability assumption:

```text
Pantheon+ distance deformation -> same BAO distance deformation
```

That rejection is useful. It says the naive cross-probe map is not the theory.

## 1. Core Rule

No AOC deformation may be exported from one observable to another without an
explicit observable map.

An observable map must specify:

1. the standard observable,
2. the observer or pipeline that reconstructs it,
3. the AOC variable being introduced,
4. the nuisance parameters it may be degenerate with,
5. the controls that would remove a false signal,
6. the second-order signature expected if the map is right,
7. the result that would count against the map.

Canonical sentence:

> AOC does not get a universal deformation for free; each observable must earn
> its own map from the reconstruction horizon to measured quantities.

## 2. Prohibited Assumptions

Do not assume any of the following unless explicitly derived:

1. **Shared time.**
   A redshift variable, cosmic time coordinate, observer time, and pipeline
   reconstruction time are not automatically the same object.

2. **Shared distance.**
   Luminosity distance, angular-diameter distance, comoving transverse distance,
   radial BAO distance, and inferred age are not interchangeable.

3. **Shared amplitude.**
   A `lambda_K` fitted in Pantheon+ does not automatically set the amplitude in
   DESI, Planck, JWST, or Fermi.

4. **Shared observer frame.**
   A supernova light-curve pipeline, BAO standard-ruler pipeline, CMB
   component-separation pipeline, and high-redshift galaxy pipeline may have
   different effective observer quotients.

5. **Shared nuisance structure.**
   Calibration drift, `M_B`, `H0`, `r_d`, `Omega_m`, `w0/wa`, dust, stellar
   population modeling, and selection effects are not the same nuisance.

## 3. Probe Map Table

| Probe | Standard observable | Naive AOC assumption | Proper AOC question | Current status |
| --- | --- | --- | --- | --- |
| Pantheon+ SNe | `mu(z)`, `D_L(z)` | AOC is a distance-modulus shift | Is there a pipeline-bound luminosity reconstruction floor or calibration-like boundary effect? | v0/v1 exploratory contracts exist |
| DESI BAO | `D_M/r_d`, `D_H/r_d`, `D_V/r_d` | Same distance deformation as Pantheon+ | Does the BAO standard-ruler pipeline imply a separate radial/transverse observer quotient? | first naive portability test rejected |
| Planck/CMB | acoustic angle, peaks, maps, component separation | Move or blur the Big Bang boundary | Which features are stable across reconstruction operators, masks, and likelihood choices? | guardrail only |
| JWST/JADES | high-`z` redshifts, ages, masses, luminosity functions | Early mature galaxies prove false bottom | Does a predeclared boundary-compression map relax inferred maturity without tuning astrophysics? | holdout |
| Hubble tension | early/late inference mismatch | AOC explains the tension | Can apparatus-bound `K` predict sign/order of pipeline disagreement before fitting? | long-term shape only |
| Fermi / gamma-ray | catalogs, energy bands, GRBs, diffuse background | high-energy data reveals origin structure | Can a clean instrument pipeline define a calculable apparatus-bound `K`? | apparatus case study |

## 4. Pantheon+ Map

Current map:

```text
delta_mu_AOC(z; lambda_K, p) = lambda_K * (1 + z)^(p - 1)
```

Scope:

This is a distance-modulus map for supernova analysis. It is not a universal
cosmological time law.

Allowed use:

1. Test whether a proof-derived deformation shape improves Pantheon+ residuals.
2. Run power tests and covariance sensitivity.
3. Treat the result as a candidate luminosity-pipeline effect.

Forbidden use:

1. Export `lambda_K` directly to BAO as the same physical amplitude.
2. Treat a supernova residual as a direct origin-boundary detection.
3. Use Pantheon+ to tune a JWST or CMB map.

Open map question:

> Is the Pantheon+ signal a luminosity-distance reconstruction effect, a
> calibration/population effect, or a real expansion-history effect?

DESI currently pushes against the third interpretation under the first simple
projection.

## 5. DESI BAO Map

Current first-pass map:

```text
D_M^AOC(z) = D_M^LCDM(z) * s(z)
D_H^AOC(z) = d D_M^AOC / dz
s(z) = 10^(lambda_K g(z) / 5)
```

Sensitivity map:

```text
D_M^AOC(z) = D_M^LCDM(z) * s(z)
D_H^AOC(z) = D_H^LCDM(z) * s(z)
```

Result:

DESI DR2 BAO prefers near-zero deformation across the reported subsets after
fitting a global BAO `alpha` nuisance scale. The Pantheon-amplitude deformation
does not port to BAO under this map.

Interpretation:

This rejects direct distance-shift portability. It does not yet test all AOC BAO
possibilities.

Possible next BAO maps, to be chosen before fitting:

1. **Null BAO map.**
   AOC affects supernova luminosity reconstruction but preserves BAO rulers.

2. **Radial/transverse split map.**
   AOC predicts a constrained mismatch between `D_H` and `D_M`, not a common
   scaling.

3. **Alpha-only observer map.**
   The observer quotient appears as an effective reconstruction scale or ruler
   calibration, not as a redshift-dependent distance shape.

4. **Covariance/atlas map.**
   AOC predicts increased chart-tension or covariance structure across
   tracers, not a mean-vector deformation.

5. **No current BAO signature.**
   BAO remains a guardrail rather than a positive AOC target until a native map
   is derived.

Required next BAO control:

Before any new AOC BAO fit, upgrade the baseline to include at least an
`Omega_m` grid and explicit `alpha` marginalization. Add `w0wa` only when
parameter accounting is comparable.

## 6. Planck / CMB Map

Current role:

Guardrail, not target.

AOC must preserve:

1. CMB blackbody spectrum,
2. acoustic peak structure,
3. anisotropy constraints,
4. consistency of component-separated sky maps,
5. relationship to BAO and structure growth.

First safe map:

Use Planck component-separation pipelines as explicit observer operators:

```text
Commander
NILC
SEVEM
SMICA
```

Question:

> Which features are stable across reconstruction operators, and which features
> are pipeline-bound?

Forbidden shortcut:

> Do not claim the CMB is "just" a projection artifact.

## 7. JWST / JADES Map

Current role:

Holdout and conceptual payoff, not tuning target.

AOC-relevant question:

> If a reconstruction horizon compresses depth near the apparent origin, does a
> predeclared map relax inferred high-redshift galaxy maturity?

Required controls:

1. stellar population modeling,
2. dust,
3. IMF assumptions,
4. selection effects,
5. lensing magnification,
6. photometric-redshift contamination,
7. spectroscopic confirmation.

Forbidden shortcut:

> Do not say early massive galaxies prove a false bottom.

Allowed future test:

Fit no parameters on JWST. Use an expansion-side or boundary-side map frozen
from Pantheon+/DESI/Planck discipline, then test whether the same map reduces
age/mass tension.

## 8. Hubble-Tension Map

Current role:

Long-term shape only.

Better question:

> Does apparatus-bound `K` predict the sign and order of disagreement between
> early-universe and late-universe inference pipelines?

Forbidden claim:

> AOC explains the Hubble tension.

Allowed work:

1. Build a pipeline mismatch triangle.
2. Identify which boundary assumptions differ across early/late inference.
3. Ask whether a calculable `K` shift predicts the direction before fitting.

## 9. Fermi / Instrument-Forward Map

Current role:

Apparatus-bound `K` practice, not origin cosmology.

Good target shape:

```text
instrument threshold -> reconstruction budget -> catalog boundary
```

Useful because Fermi products have explicit:

1. energy ranges,
2. exposure,
3. detection thresholds,
4. source catalogs,
5. transient pipelines,
6. caveats.

Allowed claim:

> Fermi can help calibrate apparatus-bound reconstruction floors.

Forbidden claim:

> Fermi currently supports AOC.

## 10. Pre-Fit Checklist

Before running any new empirical AOC fit, write down:

1. Observable:
   `mu`, `D_L`, `D_M`, `D_H`, `theta_*`, age, mass, catalog threshold, etc.

2. Observer/pipeline:
   instrument, selection, reconstruction algorithm, masks, calibration, and
   nuisance model.

3. AOC map:
   exact equation from reconstruction-horizon variable to observable.

4. Frozen parameters:
   which parameters are fixed before fitting and why.

5. Nuisance parameters:
   which standard cosmology or astrophysics parameters are allowed to move.

6. Baseline:
   `LambdaCDM`, `w0wa`, instrument-only model, or published likelihood.

7. Failure mode:
   what result rejects the map.

8. Allowed claim:
   one sentence.

9. Forbidden claim:
   one sentence.

## 11. Immediate Next Work

The next proper technical deliverable is not another dataset. It is one of:

1. **DESI baseline upgrade.**
   Add an `Omega_m` grid and explicit `alpha` marginalization to determine
   whether the near-zero result is stable against baseline freedom.

2. **Native BAO map derivation.**
   Decide whether AOC predicts no BAO deformation, a radial/transverse split,
   an alpha-only observer effect, or an atlas/covariance signature.

3. **Pantheon interpretation split.**
   Separate the Pantheon+ signal into three hypotheses:
   supernova-pipeline effect, calibration/population effect, or expansion
   history effect. DESI currently weakens the expansion-history reading.

Recommended order:

```text
observable map -> baseline upgrade -> frozen rerun -> only then new data
```

