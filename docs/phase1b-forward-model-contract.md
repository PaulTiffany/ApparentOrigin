# Phase 1B — dense-envelope forward-model contract (preflight, not a result)

Status: **PRE-IMPLEMENTATION CONTRACT — INCOMPLETE PARAMETER TRANSCRIPTION; SCIENTIFIC EXECUTION BLOCKED**.

Issue: [#2](https://github.com/PaulTiffany/ApparentOrigin/issues/2).
Primary source: Naidu et al. (2026), *Nature* 656, 329–333, DOI [10.1038/s41586-026-10846-4](https://doi.org/10.1038/s41586-026-10846-4), Methods (“Cloudy modelling”), Extended Data Table 3, Extended Data Fig. 3.

This document freezes the **question, independent observables, selection logic and failure interpretation** before executing the forward model. It does **not** claim that the paper's complete grid has been recovered, that Cloudy has run, or that any mass has been measured. Phase 0's structured Gaussian fit is not an envelope model.

## Question and competing reconstructions

Can a minimal, explicitly declared *physical* dense-gas envelope model recover the source's broad line and continuum constraints, without undocumented tuning, and subsequently change the interpretation of an Hβ virial estimate?

- **E (envelope)** is a Cloudy-generated spectrum given explicit illuminating SED, composition, gas density, column, ionization, turbulence, geometry, viewing/output component, dust screen and normalization.
- **V (virial-like)** remains the local scaling estimator as implemented in Phase 1A. V is an estimator being tested, not a reference truth.
- **COLT scattering** is a distinct, downstream radiative-transfer hypothesis from the source paper; it is not silently supplied by Cloudy or by the Gaussian surrogate.

The *first* gate tests reproducibility/feasibility of E. It must not fit a mass residue, adjust V, or claim the origin of the line while E has not passed.

## Source-backed requirements to hold fixed

The paper's Methods describe a power-law/big-bump intrinsic AGN SED, a gas envelope specified by density, column density, metallicity, turbulence and ionization parameter, and **a uniform dust screen applied only in post-processing**, with A_V from 0 to 3 mag. Its displayed fiducial neighborhood includes:

| Quantity | Paper's fiducial neighborhood (not a full grid) |
| --- | --- |
| n_H | 10^11 cm^-3 |
| N_H | 10^25.8 cm^-2 |
| turbulent velocity | 500 km s^-1 |
| post-process dust A_V | about 0.15 mag |
| source redshift | 7.7569 |

The paper evaluates the **net transmitted** continuum + lines (attenuated incident plus diffuse transmitted flux), **not the total spectrum with reflected emission added**. Choosing a different output component constitutes a different model and must be labeled, never silently substituted.

### Selection contract — conjunctive, strict boundaries

A physically generated candidate passes the paper's reported broad observational filters only if all of these pass:

1. Net Hβ equivalent width: **30 Å < EW(Hβ) < 45 Å** (emission positive).
2. Hγ equivalent width: **−5 Å < EW(Hγ) < 0 Å** (absorption negative).
3. Observed-frame continuum flux-density ratios (same f_lambda units):
   - **f_lambda(4.5 μm) / f_lambda(1.8 μm) > 6**
   - **f_lambda(4.5 μm) / f_lambda(2.8 μm) > 3**.
4. **Each** included MIRI band synthetic flux lies within **2σ** of its observational comparator; bandpass integration, units, error terms and selected bands must be declared before checking candidates.
5. The source's strong Balmer break, UV weakness and detailed continuum morphology are **additional inspection/validation targets**. The simple numerical filters do not themselves establish these features.

The inequalities above are the published broad screening criteria, not a new fitted threshold and not a guarantee of a unique model. Record every candidate's per-filter pass/fail and counts; never report only the best-looking accepted spectrum.

## Mandatory pre-execution locks (currently unresolved)

The next contribution must fill these before any *science* workflow runs:

- Transcribe **every** row/axis/value of Extended Data Table 3 with its source location, units, discrete/continuous meaning and transcription verification. Do not invent unreported spacing, SED slopes, temperature, metallicity, ionization parameter or geometry.
- Pin the **exact Cloudy source commit, release and build receipt**. The publicly available upstream Cloudy `c25.00` release is a **candidate reproducibility baseline** (upstream tag available at https://gitlab.nublado.org/cloudy/cloudy/-/tags/c25.00), **not asserted to be the version used by Naidu et al.** Capture compiler flags, environment and model input deck in Actions.
- Declare minimal-grid cell identities and their complete input decks *before* examining whether their spectral outputs match. If any of the paper's options are unreported or ambiguous, enumerate explicit alternative branches; do not quietly optimize.
- Freeze the output extraction path: net transmitted rather than total flux; rest/observed wavelength mapping; EW windows and continuum definitions; filter transmission curves; exact NIRCam normalization rule and observation epoch; dust attenuation prescription; all line/band uncertainties.
- Resolve public observation products for **all MIRI bands needed**, their units, covariance/uncertainty treatment, source IDs, upstream URLs and SHA-256 receipts. The Phase 0/1A G395M file alone is not a substitute for MIRI photometry or the prism SED.
- Declare any continuum-shape comparator, missing-data rule, upper-limit treatment, numerical tolerance and stopping rule *before* evaluating predictions. Missing/undefined inputs mean **INVALID/UNEXECUTED**, never a failed astrophysical model.

## Controlled run protocol

1. **Acquisition/identity check:** clean GitHub Actions runner retrieves only public upstream products; validates target/epochs; emits checksums and machine-readable metadata; raw telescope products remain ephemeral.
2. **Model generation:** pinned Cloudy source and frozen model-input deck(s); archive input decks, compile receipt, generated model identifiers and hashes, not a hidden cache or hand-selected million-model surrogate.
3. **Forward-observable calculation:** transform *each* model's net-transmitted spectrum into declared rest/observed-frame EWs, continuum ratios and band-integrated fluxes using the identical frozen selection operator; retain all candidate outcomes.
4. **Fiducial contact:** report distance (in declared observable coordinates) between published fiducial neighborhood and the successful/unsuccessful models. Do not tune input SED or dust after inspecting success to force agreement.
5. **Only after success:** freeze the envelope family and compare E against V on the same source and, in a separate preregistration, under a declared observer-access thinning operator.

**CI convention:** physical non-reproduction is a valid **green** scientific outcome with status `NO_CANDIDATE_PASSES_DECLARED_GRID`; invalid identity, missing source, missing mandatory parameter, runtime failure or unrecorded choices are **red** execution failures. A software unit-test pass is *not* a physical-model success.

## Outcome and claim boundary

| Outcome | Allowed claim | Forbidden claim |
| --- | --- | --- |
| No declared candidates pass | The *declared minimal grid* did not reproduce the screening conditions, with per-filter receipts. | Dense-envelope physics is excluded or the paper is disproved. |
| Some candidates pass | That particular reproducible model family satisfies the declared broad filters. | Envelope geometry/true BH mass/scattering mechanism is uniquely established. |
| Incomplete grid, source or output contracts | Phase 1B has not reached an interpretable scientific test. | `Negative result`, `replication`, `confirmed`, or comparison to V. |
| Later E–V disagreement | Conditional reconstruction discrepancy under the two specified physical/inferential operators. | Either operator is the ground-truth mass. |

### Scientific log entry to write at execution

Record UTC time, Git SHA, Actions run URL, paper/table extraction version, all source and model hashes, declared input domain, software provenance, normalization/photometry choices, counts at *each* filter, uncertainty/covariance assumptions, permitted claim, forbidden claim, and whether any exploratory changes require a **new** preregistered run.

## Why this gate matters

Phase 0 confirmed observer-access dependence of *model distinguishability*; Phase 1A rejected the preregistered large resolution-induced *virial mass drift*. Phase 1B tests a different physical model class. Do not reframe a failure of the Gaussian route as positive evidence for an envelope, scattering, AOC, or an apparent cosmological origin.
