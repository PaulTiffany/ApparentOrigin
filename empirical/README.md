# Empirical Branches

This directory contains executable empirical contracts.

Each branch should include:

1. a data provenance note,
2. a download script where possible,
3. a parser/analysis script,
4. a report generator,
5. explicit allowed and forbidden claims.

The goal is not to prove AOC in one step. The goal is to make each contact with
real data auditable.

## Current Branches

1. `pantheon_plus/`
   - First real-data distance-modulus branch.
   - Includes v0/v1 deformation tests, heldout checks, and covariance
     sensitivity.
2. `desi_dr2_bao/`
   - Next primary external-validation branch.
   - Uses DESI DR2 BAO as a non-supernova expansion-history gate.
   - First contract implemented: test whether frozen Pantheon+ deformation
     families are compatible, rejected, or inconclusive under BAO observables.
   - Current baseline-upgraded result: after fitted BAO `alpha` and an
     `Omega_m` grid, DESI does not support the Pantheon+ deformation direction.
     Isotropic maps prefer near-zero deformation; derivative maps only improve
     chi2 by flipping sign and do not achieve BIC-level support.
3. `planck_operator_residue/`
   - First Principia-aligned operator-residue branch.
   - Uses Planck component-separated CMB maps as different reconstruction
     operators on the same sky: Commander, NILC, SEVEM, and SMICA.
   - Current state: pre-data contract plus dependency-light low-ell coefficient
     analyzer. A synthetic example run verifies the metric pipeline; no Planck
     result has been claimed.
4. `fermi_demask_shift_recurrence/`
   - Fermi gamma-ray operator-residue branch.
   - Tests whether independent-enough residual-map voices share directional
     motion under Galactic-plane mask transitions.
   - Current state: pre-run contract and provenance scaffold. Fermi
     interpretation is blocked until the Planck positive-control detector
     passes under its declared mask/extractor contract.

## Current Priority

Prioritize `planck_operator_residue/` as the positive-control gate for the
Fermi demask-shift recurrence branch. DESI remains a restrictive
distance-ruler constraint; Planck and Fermi now form an operator-residue lane
that tests observer-horizon framing by comparing multiple reconstruction
operators on the same target before any sonification claim is allowed.
