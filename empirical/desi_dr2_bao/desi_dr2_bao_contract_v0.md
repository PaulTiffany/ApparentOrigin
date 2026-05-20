# DESI DR2 BAO Contract v0

Status: draft external-validation contract.

Execution note:

The first pass has been implemented in:

```text
empirical/desi_dr2_bao/analyze_desi_dr2_bao.py
reports/desi_dr2_bao/desi_dr2_bao_report.md
```

Initial result: DESI DR2 BAO does not support the frozen Pantheon+ deformation
direction after fitting a global BAO scale nuisance and gridding `Omega_m`. The
`isotropic_scale` sensitivity map prefers near-zero deformation. The
`derivative_dm` map can improve chi2 only by flipping sign relative to Pantheon+
and, in subsets, pushing `Omega_m` toward the upper grid edge; the improvement
does not reach BIC-level support. This is theory feedback, not a program
failure.

Purpose:

Define the next empirical gate after Pantheon+: test AOC-style deformation
against DESI DR2 BAO distance measurements without silently retuning the model
on supernova data.

## Rationale

Pantheon+ is informative but degenerate:

```text
distance modulus = cosmology + calibration + nuisance model + H0/M_B choices
```

DESI DR2 BAO probes expansion history with a different ruler. It is therefore
the next primary target before JWST/JADES and before raw Planck/CMB work.

## Fixed Inputs from Existing AOC Work

The first DESI pass should carry forward the already-frozen Pantheon+ contracts:

```text
empirical/aoc_threshold_contract_v0.md
empirical/aoc_proof_derived_contract_v1.md
```

Do not create a new deformation shape after seeing DESI residuals.

Primary v1 shape:

```text
delta_mu_AOC(z; lambda_K, p) = lambda_K * (1 + z)^(p - 1)
p = 1.8
```

Robustness v1 shape:

```text
p = 2.0
```

The BAO mapping must translate the same observer-time or distance-deformation
parameter into BAO observables. If this translation is ambiguous, the ambiguity
must be stated before fitting.

## Target BAO Observables

Use official DESI DR2 BAO measurements for:

```text
D_M(z) / r_d
D_H(z) / r_d
D_V(z) / r_d
```

where:

```text
D_H(z) = c / H(z)
```

If the published products include covariance, use it. If the first pass uses
diagonal errors only, the report must be labeled diagonal-only exploratory.

## Baselines

Minimum baseline:

```text
flat LambdaCDM
H0 = 70 km/s/Mpc
Omega_m = 0.3
r_d fixed to the value used by the selected DESI product or explicitly stated
```

Preferred baseline:

Use the DESI-recommended BAO likelihood or covariance product with published
fiducial conventions.

Comparator:

```text
w0waCDM
```

Only include `w0waCDM` when the implementation can do so with parameter
accounting comparable to the AOC deformation.

## Primary Test

Fit or evaluate the AOC deformation parameter on DESI DR2 BAO using the same
deformation family already frozen by the Pantheon+ contracts.

Primary question:

```text
theta_DESI compatible with theta_Pantheon+?
```

Outcomes:

1. Compatible direction and magnitude:
   - stronger external signal,
   - still not confirmation.
2. Compatible direction but weaker magnitude:
   - possible cross-probe hint,
   - requires joint fit and systematics work.
3. Opposite direction or strong rejection:
   - Pantheon+ deformation likely SN-specific, calibration-like, or wrong
     observable signature.
4. No sensitivity:
   - BAO first pass is inconclusive; need better likelihood or different
     observable.

## Success Criteria

The first DESI gate succeeds if it produces:

1. official data provenance,
2. a normalized BAO measurement table,
3. an auditable baseline prediction,
4. a predeclared AOC mapping,
5. a clear compatible/rejected/inconclusive outcome,
6. explicit allowed and forbidden claims.

The first DESI gate fails if:

1. the deformation is re-shaped after seeing DESI,
2. the result is framed as proof,
3. covariance or fiducial conventions are ignored without disclosure,
4. `w0waCDM` is used as a rhetorical comparison without equivalent parameter
   accounting.

## Allowed Claims

1. DESI DR2 BAO is the correct next external gate after Pantheon+.
2. Cross-probe stability would be more meaningful than further same-dataset
   Pantheon+ sharpening.
3. DESI rejection of the Pantheon+ deformation would be useful and should be
   treated as theory feedback, not failure of the whole program.

## Forbidden Claims

1. DESI confirms AOC.
2. DESI proves the false-bottom model.
3. AOC explains dark energy evolution.
4. AOC explains the Hubble tension.
5. `LambdaCDM` is refuted by this first pass.

## Deferred Targets

JWST/JADES:

Use only after Pantheon+ plus DESI fix or reject a deformation. JWST high-z
galaxy maturity is astrophysically messy and should be a holdout, not a tuning
target.

Planck/CMB:

Use initially as a guardrail. Do not start with raw CMB maps or low-ell anomaly
fishing.
