# DESI DR2 BAO Baseline-Upgraded AOC Gate

Status: baseline-upgraded exploratory gate.

This report uses the compact DESI DR2 Gaussian BAO likelihood input
files from the Cobaya BAO data repository linked by the official DESI
DR2 cosmology products page. It fits a global `alpha` scale for every
model and now grids over `Omega_m`, so the comparison is about
redshift-dependent shape after a stronger `LambdaCDM` baseline.

## Baseline

| Subset | Points | Best Omega_m | Fitted alpha | Baseline chi2 |
| --- | ---: | ---: | ---: | ---: |
| all | 13 | 0.297 | 1.013652 | 10.273918 |
| galaxy_no_lya | 11 | 0.299 | 1.014815 | 10.176113 |
| pantheon_overlap_z_le_1 | 7 | 0.310 | 1.020699 | 8.517187 |

Baseline cosmology: flat `LambdaCDM`, `H0=70.0`, `r_d=147.09 Mpc`,
`Omega_m` grid `0.15` to `0.45`;
each subset fits its own global `alpha`.

## AOC Shape Gate

| Subset | Shape | Mapping | Best Omega_m | Best lambda | Pantheon ref | Delta chi2 | Delta BIC | Classification | Ref delta chi2 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| all | v0_log | derivative_dm | 0.321 | +0.027 | -0.130 | -0.267 | +2.298 | opposite_direction | +5.958 |
| all | v0_log | isotropic_scale | 0.301 | +0.009 | -0.130 | -0.060 | +2.505 | desi_prefers_near_zero | +11.802 |
| all | v1_pow_p1.8 | derivative_dm | 0.310 | +0.009 | -0.150 | -0.276 | +2.289 | desi_prefers_near_zero | +61.029 |
| all | v1_pow_p1.8 | isotropic_scale | 0.303 | +0.010 | -0.150 | -0.146 | +2.419 | desi_prefers_near_zero | +31.591 |
| all | v1_pow_p2.0 | derivative_dm | 0.308 | +0.005 | -0.110 | -0.261 | +2.304 | desi_prefers_near_zero | +102.381 |
| all | v1_pow_p2.0 | isotropic_scale | 0.303 | +0.007 | -0.110 | -0.161 | +2.403 | desi_prefers_near_zero | +37.870 |
| galaxy_no_lya | v0_log | derivative_dm | 0.450 | +0.184 | -0.130 | -2.441 | -0.043 | opposite_direction | +1.354 |
| galaxy_no_lya | v0_log | isotropic_scale | 0.300 | +0.003 | -0.130 | -0.002 | +2.396 | desi_prefers_near_zero | +5.991 |
| galaxy_no_lya | v1_pow_p1.8 | derivative_dm | 0.412 | +0.112 | -0.150 | -2.793 | -0.395 | opposite_direction | +8.397 |
| galaxy_no_lya | v1_pow_p1.8 | isotropic_scale | 0.303 | +0.011 | -0.150 | -0.050 | +2.348 | desi_prefers_near_zero | +11.622 |
| galaxy_no_lya | v1_pow_p2.0 | derivative_dm | 0.398 | +0.069 | -0.110 | -2.751 | -0.353 | opposite_direction | +10.861 |
| galaxy_no_lya | v1_pow_p2.0 | isotropic_scale | 0.303 | +0.008 | -0.110 | -0.068 | +2.330 | desi_prefers_near_zero | +12.755 |
| pantheon_overlap_z_le_1 | v0_log | derivative_dm | 0.450 | +0.185 | -0.130 | -1.511 | +0.435 | opposite_direction | +0.442 |
| pantheon_overlap_z_le_1 | v0_log | isotropic_scale | 0.307 | -0.010 | -0.130 | -0.023 | +1.922 | desi_prefers_near_zero | +2.796 |
| pantheon_overlap_z_le_1 | v1_pow_p1.8 | derivative_dm | 0.450 | +0.162 | -0.150 | -3.086 | -1.141 | opposite_direction | +2.772 |
| pantheon_overlap_z_le_1 | v1_pow_p1.8 | isotropic_scale | 0.308 | -0.005 | -0.150 | -0.006 | +1.940 | desi_prefers_near_zero | +4.473 |
| pantheon_overlap_z_le_1 | v1_pow_p2.0 | derivative_dm | 0.450 | +0.115 | -0.110 | -3.356 | -1.410 | opposite_direction | +3.411 |
| pantheon_overlap_z_le_1 | v1_pow_p2.0 | isotropic_scale | 0.309 | -0.002 | -0.110 | -0.003 | +1.942 | desi_prefers_near_zero | +4.671 |

## Interpretation

This is still not a confirmation test. The correct read is whether a
Pantheon+-motivated deformation survives contact with a non-supernova
ruler under a predeclared map after giving the `LambdaCDM` baseline
basic `Omega_m` freedom.

The subset split is part of the control discipline. `all` includes
Ly-alpha at `z=2.33`; `galaxy_no_lya` removes that extrapolation;
`pantheon_overlap_z_le_1` restricts DESI to the redshift range closest
to the Pantheon+ deformation fit.

Current read: compare the best `lambda_K` and penalized statistics
against the Pantheon reference amplitudes. Any result that improves
`chi2` but not BIC is treated as insufficient shape evidence.

In the baseline-upgraded run, the `isotropic_scale` sensitivity map
continues to prefer near-zero deformation. The `derivative_dm` map
can improve chi2 in subsets only by flipping sign relative to the
Pantheon+ deformation direction and, in some cases, by moving
`Omega_m` to the upper grid edge. This is not evidence for
Pantheon-amplitude portability.

Allowed claim:

> DESI DR2 BAO now has a baseline-upgraded external gate for the
> frozen AOC observable maps.

Forbidden claim:

> DESI confirms AOC, explains dark energy evolution, or solves the
> Hubble tension.
