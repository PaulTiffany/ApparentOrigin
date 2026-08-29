# DESI DR2 BAO Empirical Branch

Status: first-pass external gate implemented.

Purpose:

Test whether AOC-style temporalization or threshold-deformation structure
survives contact with a non-supernova expansion-history probe.

This branch is deliberately separate from Pantheon+. Pantheon+ is a luminosity
distance probe with calibration and nuisance-parameter degeneracies. DESI DR2
BAO uses a different ruler and reports transverse/radial distance information
through BAO observables.

## Public Sources

Official DESI DR2 publication index:

```text
https://data.desi.lbl.gov/doc/papers/dr2/
```

DESI DR2 cosmology chains and data products announcement:

```text
https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/
```

DESI DR2 Results II supplementary data:

```text
https://zenodo.org/records/16644577
```

## First-Pass Data Policy

Do not start by downloading the full Zenodo archive or chains unless needed.
The first pass should extract a small BAO measurement table from official
DESI DR2 paper products or supplementary files:

```text
z_eff, observable, value, covariance_or_error
```

Target observables:

```text
D_M(z) / r_d
D_H(z) / r_d
D_V(z) / r_d
```

where `D_H(z) = c / H(z)`.

## Empirical Question

Does the deformation direction suggested by the Pantheon+ contracts remain
compatible with DESI DR2 BAO distances?

The question is not:

> Does DESI prove AOC?

The question is:

> Does a non-supernova ruler prefer, reject, or remain insensitive to the same
> class of observer-time deformation?

## Initial Comparison

Compare:

```text
flat LambdaCDM
flat LambdaCDM + T_theta / AOC threshold deformation
w0waCDM baseline where possible
```

The first useful result is not a large `Delta chi2`. It is stability:

```text
theta_Pantheon+ ~= theta_DESI
```

or a clear failure:

```text
DESI rejects the Pantheon+-favored deformation direction.
```

## Allowed Claims

1. DESI DR2 BAO is the next clean external probe after Pantheon+ because it
   tests expansion history with a different ruler.
2. AOC can define a predeclared BAO contract using `D_M`, `D_H`, and `D_V`.
3. A stable deformation direction across Pantheon+ and DESI would be stronger
   than a supernova-only signal.

## Forbidden Claims

1. DESI confirms AOC.
2. AOC explains evolving dark energy.
3. AOC explains the Hubble tension.
4. BAO portability proves universality.
5. AOC refutes `LambdaCDM`.

## Next Implementation Tasks

Completed first pass:

1. Located the compact official DESI DR2 Gaussian BAO likelihood inputs linked
   from the official DESI DR2 cosmology products page.
2. Recorded provenance and hashes under `data/raw/desi_dr2_bao/`.
3. Built a parser emitting a normalized table under
   `data/derived/desi_dr2_bao/`.
4. Implemented flat-`LambdaCDM` BAO predictions with a fitted global `alpha`
   nuisance scale.
5. Implemented frozen v0/v1 AOC deformation projections under two mappings:
   `derivative_dm` and `isotropic_scale`.

Current baseline-upgraded result:

DESI DR2 BAO does not support the carried-forward Pantheon+ deformation
direction after fitting a global BAO `alpha` nuisance and gridding `Omega_m`.
The `isotropic_scale` sensitivity map prefers near-zero deformation. The more
constrained `derivative_dm` map can improve chi2 in subsets only by flipping
the sign relative to Pantheon+ and often pushing `Omega_m` toward the upper
grid edge; the improvement does not reach BIC-level support. The
Pantheon+-amplitude deformation is therefore not portable to DESI under this
observable map.

Report:

```text
reports/desi_dr2_bao/desi_dr2_bao_report.md
```

Next tasks:

1. Decide whether AOC needs a different BAO temporalization map or whether the
   Pantheon+ signal should be treated as supernova/calibration-specific.
2. Add a DESI-recommended likelihood comparison or `w0wa` comparator only with
   equivalent parameter accounting.
3. Do not move to JWST/JADES as a tuning target until this BAO constraint is
   incorporated.
