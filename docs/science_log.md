# Science Log

## 2026-05-20: Fermi Demask-Shift Recurrence Contract Added

Added:

```text
docs/fermi_demask_shift_recurrence_contract.md
empirical/fermi_demask_shift_recurrence/README.md
data/raw/fermi_demask_shift_recurrence/PROVENANCE.md
data/derived/fermi_demask_shift_recurrence/
empirical/fermi_demask_shift_recurrence/shared_shift_metric.py
empirical/fermi_demask_shift_recurrence/voice_independence_ledger_template.csv
empirical/fermi_demask_shift_recurrence/example_axes.csv
reports/fermi_demask_shift_recurrence/
```

Reason:

The user and Desktop GPT proposed a single central experiment: freeze a
recurrence detector from the Planck demask-shift work, apply it blindly to
Fermi residual maps across Galactic-plane mask transitions and null
simulations, then sonify only the pre-measured shared-shift geometry.

Phase:

```text
near-cousin / empirical-control bridge
```

The contract makes the target explicit:

```text
shared mask-induced directional motion before sound
```

not:

```text
the heard note as evidence
```

Human-authorial note:

The user explicitly overrode a prior Desktop GPT qualifier via human agency.
This has been recorded as authorship of bounds: permission to proceed with the
experiment lane, not permission to waive controls, nulls, or forbidden-claim
discipline.

Frozen structure:

1. Planck positive-control gate first.
2. Fermi voice-independence ledger before live analysis.
3. Mask ladder `M0, |b|>10, |b|>20, |b|>30, official/source/diffuse variant`.
4. Low-order axial signature `u[v,M,L]`.
5. Demask motion magnitude `Delta[v,Ma->Mb,L]`.
6. Nondegenerate rotation axis `r[v,Ma->Mb,L]`.
7. SharedShift report with `D_op`, `D_motion` as MAD, `R_axis`, median
   `Delta`, null percentile, and verdict.
8. Sonification only after numeric recurrence is measured.

Allowed claim:

> This freezes a Fermi operator-residue experiment that tests shared
> mask-induced motion across reconstruction voices before sound.

Forbidden claim:

> Fermi currently supports AOC, a heard note proves recurrence, or a shared
> demask shift proves a physical spin operator.

## 2026-05-20: Planck Positive-Control SharedShift Run and Newton-Light Rendering

Executed:

```text
python empirical/fermi_demask_shift_recurrence/build_planck_positive_control_axes.py
python empirical/fermi_demask_shift_recurrence/shared_shift_metric.py \
  --axes-csv data/derived/fermi_demask_shift_recurrence/planck_positive_control_axes.csv \
  --transitions M0:M1 \
  --out-csv reports/fermi_demask_shift_recurrence/planck_positive_control_shared_shift.csv
python empirical/planck_operator_residue/counterpoint_voice_leading.py \
  --out-dir reports/planck_operator_residue/counterpoint_voice_leading_rerun_2026_05_20
python empirical/planck_operator_residue/render_voice_drift_newton_light.py
```

Added:

```text
empirical/fermi_demask_shift_recurrence/build_planck_positive_control_axes.py
empirical/planck_operator_residue/render_voice_drift_newton_light.py
data/derived/fermi_demask_shift_recurrence/planck_positive_control_axes.csv
reports/fermi_demask_shift_recurrence/planck_positive_control_shared_shift.csv
reports/fermi_demask_shift_recurrence/planck_positive_control_shared_shift_report.md
reports/planck_operator_residue/counterpoint_voice_leading_rerun_2026_05_20/
reports/planck_operator_residue/newton_voice_drift_light/
```

SharedShift positive-control result:

| transition | band | voices | valid r axes | D_op | D_motion MAD | R_axis | median Delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| M0 -> M1 | ell2 | 4 | 4 | 4.615 deg | 2.526 deg | 0.845 | 27.360 deg |
| M0 -> M1 | ell3 | 4 | 4 | 5.112 deg | 0.485 deg | 0.869 | 22.490 deg |

Readout:

The Planck positive-control detector reproduces the expected demask-shift
shape. Ell=3 is the cleaner block-motion control: all four voices move by
nearly the same amount and around concentrated rotation axes. Ell=2 remains
coherent but has a larger SEVEM outlier component.

Newton-light rendering:

The existing Planck voice-drift WAV mapping was re-rendered as an Opticks /
Newton light instrument:

```text
reports/planck_operator_residue/newton_voice_drift_light/
```

WAV audit:

```text
sample_rate = 44100 Hz
duration = 27.0 s
channels = 2
peak_abs_pcm16 = 0.7087
rms_pcm16 = 0.1655
```

Spectral readout under the declared sound-to-light inspection map:

| mask state | mean wavelength | range | Newton-band counts |
| --- | ---: | ---: | --- |
| unmasked | 503.0 nm | 493.5-527.2 nm | blue:7, green:1 |
| galcut20 | 474.0 nm | 455.6-489.3 nm | indigo:8 |

The masked state shifts by `-29.0 nm` toward shorter, bluer/violetter
wavelengths under this explicit rendering. This is an inspection artifact over
already-measured Planck demask geometry, not new evidence.

Allowed claim:

> The Planck positive-control detector runs and reproduces the expected shared
> demask-shift shape; the same voice-drift mapping can be rendered as Newton
> light rather than heard as audio.

Forbidden claim:

> The Newton-light rendering is evidence, or the Planck positive control is a
> Fermi detection.

## 2026-04-30: Episode 4 (Final-For-Now) Packet Shipped

Packet:

```text
notebooklm/upload_packet_2026-04-30/
```

Contents (17 numbered files plus instructions). Reading order anchors
on the Episode 3 hand-off (lambda_K Kerr-interior seed, Sprint D voice-
leading sim-null, P1 prediction evaluation), then walks the Episode 4
arc: Sprint E prismatic decomposition rigor, lambda_K observable-
feasibility first pass, lambda_K SRMF invariant card, lambda_K Planck
operator-prism contract, the live PASS gate report, Sprint F1 D_iso
audit, Sprint F2 C_axis null baseline, Sprint F3 CI LLM compute
leverage methodology note. Closes with one frozen open question.

Frame: this is the final episode for now. Episode 4 is not a
publication-class artifact; the closest is the operator-prism gate
live report whose verdict string carries `if_inputs_were_predeclared`
by design.

Reading discipline preserved across the packet:

> Boundary of reconstruction, not beginning of being.

## 2026-04-30: Sprint F3 CI LLM Compute Leverage Methodology Note

Added:

```text
docs/ci_llm_compute_leverage.md
```

Names the methodology pattern by which a CI-side LLM agent (GPT
working through OpenAI Codex) staged a private GitHub repository and
workflow YAML to run the live operator-prism contract on
GitHub-hosted Linux compute when the local Windows environment did
not have `healpy` available. Predeclaration discipline ran forward:
the contract document and gate code were committed locally before
the workflow ran; large data inputs were treated as fetched data
not Git-tracked source; the small workflow artifact pulled back into
the local repo as canonical state.

Allowed claim:

> The CI-LLM-as-compute-broker pattern is a reusable tool choice when
> the local environment cannot install a required library and the
> contract is already frozen.

Forbidden claim:

> The CI LLM did the science.

## 2026-04-30: Sprint F2 C_axis Null Baseline

Added:

```text
empirical/planck_operator_residue/operator_prism_c_axis_null.py
reports/planck_operator_residue/operator_prism_c_axis_null/
  c_axis_null_ell3_unmasked_samples.csv
  c_axis_null_ell3_galcut20_samples.csv
  operator_prism_c_axis_null_summary.json
  operator_prism_c_axis_null_report.md
```

Local-machine surrogate null using the Sprint D scaffolding. n=500
realizations per condition, ell=3, noise_scale=1.0. Both unmasked and
synthetic galcut20 conditions.

Result (n=500):

```text
ell3_unmasked   median C_axis = +0.532, frac_positive = 0.904
ell3_galcut20   median C_axis = +0.550, frac_positive = 0.918

live (official-mask-base, C_axis = 0.281)    sits at 26.4 / 22.2 percentile
live (official-mask-dilate1, C_axis = 0.426) sits at 39.4 / 34.8 percentile
```

Methodologically substantive finding: the contract's sign condition
`C_axis > 0` is **trivially satisfied** under the surrogate cartoon
(about 90% of realizations). In a shared-sky-plus-small-noise model
pair-residues reduce to `noise_i - noise_j`, whose m=ell-maximizing
axes are nearly uniform on S^2 (D_res near 60 deg), while operator
axes track the shared sky (D_op small), giving D_res - D_op broadly
positive by construction.

The live values sit *below* the surrogate null bulk: real Planck
pair-residues are more aligned than uniform-random predicts, with
shared structure the cartoon omits.

Frozen open question (closes Episode 4):

> The proper null for the live operator-prism contract requires
> another GitHub Actions run -- isotropic LambdaCDM through the
> official Planck common mask with the same `healpy.map2alm`
> extractor.

Allowed claim:

> Sprint F2 establishes that the contract's sign-only verdict is a
> weak ordinal claim under any shared-sky cartoon and clarifies the
> open question.

Forbidden claim:

> Sprint F2 confirms or refutes the operator-prism contract.

## 2026-04-30: Sprint F1 D_iso First-Principles Calibration

Added:

```text
empirical/planck_operator_residue/calibrate_d_iso.py
reports/planck_operator_residue/d_iso_calibration/
  d_iso_calibration_summary.json
  d_iso_calibration_report.md
```

Audits the gate's hardcoded `D_iso = 57 deg` constant. For two uniform
unit vectors on S^2, the axial angle has CDF `1 - cos(theta)`, so the
median is exactly 60 deg. Monte Carlo (n_realizations = 100,000) places
the n=4 reference at:

```text
median of per-realization median pairwise axial angle = 60.03 deg
mean = 59.51 deg, std = 11.23 deg
p25 = 52.60, p75 = 67.62 deg
```

The hardcoded 57 deg sits within the bulk of the per-realization
distribution but is ~3 deg below the empirical median, well outside
Monte Carlo noise. The hardcoded value is **not retroactively modified**
in the gate code, because the contract was frozen at that value before
the live run. Future contracts should cite this calibration and use
60 deg.

Under D_iso = 60 the live magnitudes become:

```text
C_axis(base, D_iso=60)    = (20.133 - 4.088) / 60 = 0.267
C_axis(dilate1, D_iso=60) = (25.625 - 1.363) / 60 = 0.404
```

Both remain positive; the predeclared sign condition is unchanged.

Allowed claim:

> The hardcoded D_iso = 57 deg is consistent with the bulk of the
> first-principles distribution but is below its median.

Forbidden claim:

> D_iso may be retroactively modified to flip a verdict.

## 2026-04-30: GitHub Actions Operator-Prism Live Contract Run

GitHub runner:

```text
https://github.com/PaulTiffany/planck-operator-prism-contract
```

Run:

```text
https://github.com/PaulTiffany/planck-operator-prism-contract/actions/runs/25146431898
```

Local artifact updated:

```text
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_summary.json
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md
reports/planck_operator_residue/operator_prism_contract/healpy_official_mask/
```

Result:

```text
live_verdict = contract_success_if_inputs_were_predeclared
```

Coordinates:

```text
official-mask base:
  D_op   = 4.087821 deg
  D_res  = 20.133156 deg
  C_axis = 0.281497

official-mask dilate1:
  D_op   = 1.363235 deg
  D_res  = 25.624889 deg
  C_axis = 0.425643
```

Reading:

The predeclared sign condition was:

```text
C_axis(ell=3, official-mask-base) > 0
and remains > 0 for official-mask-dilate1.
```

The GitHub Linux `healpy` run satisfies this sign condition for the Planck
operator-prism channel.

Allowed claim:

> The live official-mask `base -> dilate1` run satisfies the predeclared
> operator-prism sign condition for this channel.

Forbidden claim:

> This confirms AOC, derives an observed `lambda_K` amplitude, or refutes
> LambdaCDM.

## 2026-04-30: GitHub Actions Harness for Operator-Prism Contract

Added:

```text
.github/workflows/planck_operator_prism.yml
cloud_run/github_actions/README.md
cloud_run/github_actions/download_planck_pr3.sh
cloud_run/github_actions/run_planck_operator_prism.sh
```

Purpose:

Staged a small GitHub-hosted runner for the live Planck operator-prism
contract. The workflow uses Ubuntu, installs `healpy`, downloads the four
Planck PR3 component-separated maps plus the official common mask from the IRSA
Planck mirror, runs the `base -> dilate1` extraction, evaluates the contract
gate, and uploads the small report directory as an artifact.

Data discipline:

The large FITS files are not committed to Git. They are fetched inputs and may
be cached by GitHub Actions under:

```text
planck-pr3-component-maps-common-mask-v1
```

This treats GitHub as compute/cache, not as a scientific data archive.

Allowed claim:

> The repo now has a private-GitHub-compatible way to run the live Linux
> `healpy` contract without dividing the local Windows machine.

Forbidden claim:

> GitHub Actions completion is itself evidence for AOC, `lambda_K`, or an
> observed CMB amplitude.

## 2026-04-30: Cloud Run Packet for Operator-Prism Contract

Added:

```text
cloud_run/planck_operator_prism/README.md
cloud_run/planck_operator_prism/requirements.txt
cloud_run/planck_operator_prism/run_operator_prism_contract.sh
empirical/planck_operator_residue/extract_planck_lowell_healpy_morphology.py
```

Updated:

```text
empirical/planck_operator_residue/evaluate_operator_prism_contract.py
```

Purpose:

Made the `healpy`/Windows dilemma optional by staging a Linux/cloud execution
packet for the missing official-mask `base -> dilate1` pair-residue inputs.

The new extractor uses `healpy.map2alm` on low-resolution official-mask
morphology states and writes coefficient CSVs for the existing ell=3
directional-axis analyzer. The contract gate can now accept live summaries via:

```text
--contract-summary base=PATH
--contract-summary dilate1=PATH
```

Local status:

```text
live_verdict = blocked_missing_required_contract_inputs
```

This is unchanged until the cloud run produces official-mask pair-residue
summaries.

Allowed claim:

> The repo now contains a reproducible cloud path for the live operator-prism
> contract inputs.

Forbidden claim:

> Merely moving extraction to cloud changes the theory status.

## 2026-04-30: lambda_K Operator-Prism Contract Gate

Added:

```text
empirical/planck_operator_residue/evaluate_operator_prism_contract.py
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_summary.json
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md
```

Purpose:

Turned the Episode 4 Planck operator-prism contract into an executable
readiness gate without requiring Python/healpy environment churn.

Result:

```text
live_verdict = blocked_missing_required_contract_inputs
```

The current official-mask morphology run supplies ell=3 operator axes, so
`D_op` is available:

```text
base:    D_op = 4.530 deg
dilate1: D_op = 1.363 deg
```

It does not yet supply official-mask ell=3 pair-residue axes, so `D_res` and
`C_axis` are deliberately left missing for the live contract.

Retrospective coordinate checks:

```text
fallback nside64:          C_axis = 0.523253
fallback nside64 galcut20: C_axis = 0.886067
```

These are context only. They do not confirm the contract because they are not
the predeclared official-mask base/dilate1 pair-residue run.

Allowed claim:

> The operator-prism coordinate now has an executable readiness gate, and the
> live Episode 4 contract is blocked on official-mask pair-residue extraction.

Forbidden claim:

> The retrospective positive `C_axis` rows confirm `lambda_K`, AOC, or an
> observed CMB amplitude.

## 2026-04-30: lambda_K Planck Operator-Prism Contract

Added:

```text
docs/lambda_k_planck_operator_prism_contract.md
```

Purpose:

Converted the `lambda_K` SRMF invariant card into one concrete TTCS candidate
map for the Planck operator prism.

Coordinate:

```tex
C_{axis}(\ell,m)
=
\frac{D_{res}(\ell,m)-D_{op}(\ell,m)}{57^\circ}
```

where `D_op` is median operator-axis dispersion and `D_res` is median
pair-residue-axis dispersion.

Candidate map:

```text
If Kerr-side axial feasibility has a Planck operator-prism channel, shared
operator-axis survival should exceed pair-residue-axis survival.
```

Next-run prediction:

```text
C_axis(ell=3, official-mask-base) > 0
```

and it remains positive under at least one adjacent official-mask morphology
step, recommended first as `base -> dilate1`.

Phase:

Near-cousin / candidate theory contract. It is not a claim that Episode 3
confirmed `lambda_K`; Episode 3 only exposed the coordinate family that makes
this future contract possible.

Allowed claim:

> The `lambda_K` lane now has a judge-free Planck operator-prism coordinate and
> a future-facing survival prediction.

Forbidden claim:

> `C_axis > 0` confirms AOC or derives an observed `lambda_K` amplitude.

## 2026-04-30: lambda_K SRMF Invariant Card

Added:

```text
docs/lambda_k_srmf_invariant_card.md
```

Purpose:

Imported the SRMF six-invariant discipline from
`C:\src\principia\Invariants\SRMF_INVARIANT_MAP.md` into the Episode 4
`lambda_K` lane.

Core move:

The `lambda_K` lane is currently at the TTIE -> TTCS boundary. The theory has
integrated a feasible Kerr spin-horizon kernel and apparatus-bound `K_P`; the
next valid move is a constrained candidate map for one Sprint E prism, not an
observed-value claim.

The card defines:

1. state invariant,
2. budget invariant,
3. coherence invariant,
4. diagnostic invariant,
5. transition invariant,
6. falsification invariant.

It also names the main "oopsie" sites where AOC could smuggle black-box
judgment or false assumptions:

```text
black-box judgment, observed/observable type mismatch, cross-probe portability,
unbounded-observer leak, hidden channel fitting, zero-order violation.
```

Allowed claim:

> The `lambda_K` theory lane now has an invariant card that keeps the work
> judge-free, type-safe, and zero-order-respecting before moving into
> second-order boundary claims.

Forbidden claim:

> The invariant card derives `lambda_K` or permits AOC to bypass zero-order
> controls.

## 2026-04-30: lambda_K Observable-Feasibility First Pass

Added:

```text
docs/lambda_k_observable_feasibility_first_pass.md
```

Purpose:

First theory-side pass on the Kerr-interior `lambda_K` lane, corrected by the
observable-versus-observed type distinction from the feasibility-band / ICML
rebuttal discipline.

Result:

The document derives a Kerr spin-horizon feasibility kernel:

```tex
h_K(\chi)=\frac{1-\sqrt{1-\chi^2}}{1+\sqrt{1-\chi^2}}
```

and a finite-budget horizon-normal interior floor:

```tex
r_K = r_- + (r_+-r_-)/K_P.
```

This yields a first admissible scale:

```tex
\Lambda_K^{adm}(\chi,K_P)=h_K(\chi)/K_P.
```

Phase:

This is a near-cousin / feasibility derivation, not an observed-number
derivation and not an instantiation. It derives an observable-feasibility
kernel, not a measured amplitude.

Key guardrail:

> Observable / feasible structure is not the same type as observed dataset
> value.

Allowed claim:

> Kerr supplies a closed-form spin-horizon feasibility kernel and a
> finite-budget interior floor chart.

Forbidden claim:

> Kerr predicts the Episode 3 Planck ell=3 lockstep or an observed Pantheon+ /
> DESI / Planck `lambda_K` value.

## 2026-04-30: Sprint E Prismatic Decomposition Rigor Seed

Added:

```text
docs/prismatic_decomposition_rigor.md
```

Purpose:

Sprint E is now landed as the instrumentation-side complement to the
Episode 4 `lambda_K` lane. It is methodological / epistemological, not
new evidence.

The document defines a three-prism robustness grammar for carrying
Episode 3 operator-residue features forward:

1. multipole prism,
2. mask / sky-partition prism,
3. operator prism.

It applies the grammar to three landed Episode 3 objects:

1. the P1/P2/P3 Q-O recomposition cliff,
2. the Sprint D ell=3 parallel-fifths lockstep feature,
3. the Sprint C-prime per-operator duet sonification.

Handshake with Claude's `lambda_K` lane:

> Sprint E does not derive `lambda_K`; it defines the decomposition contract a
> future `lambda_K` prediction would have to survive.

Allowed claim:

> Sprint E defines a robustness grammar for distinguishing multipole-local,
> mask-sensitive, operator-bound, and shared-target-residue-candidate features.

Forbidden claim:

> Triple-prism survival confirms AOC or refutes LambdaCDM.

## 2026-04-29: Episode 3 — Sim-Null Calibration + Cross-Modal Companion + λ_K Hand-off

Day 1 of the Episode 3 release window (target packet ship 2026-05-01).
Plan: `C:\Users\paulc\.claude\plans\encapsulated-singing-hinton.md`. The
distinguishing move of Episode 3 vs Episode 2 (which was methodological-
class) is that frozen prediction contracts paid off (P1 PASS, P2 leakage
rejected, P3 PASS — all completed in the prior session) and a
calibrated ΛCDM null calibrates the Episode 2 parallel-fifths headline.

### Pipeline Independence Postulate canonicalized

NotebookLM Episode 2 output coined the term as the standard reading
this work tests. Adopted into the repo glossary:

```text
docs/glossary.md
```

The entry frames the postulate as the field's default assumption that
Sprint A flagged at ell=3 (parallel-fifths in 6/6 pairs under masking),
explicitly does NOT claim the postulate has been refuted, and credits
the external coinage.

### Sprint D — voice-leading sim-null

```text
empirical/planck_operator_residue/voice_leading_sim_null.py
empirical/planck_operator_residue/plot_sim_null_histograms.py
reports/planck_operator_residue/voice_leading_sim_null/voice_leading_sim_null_report.md
reports/planck_operator_residue/voice_leading_sim_null/voice_leading_sim_null_histogram_ell3.png
reports/planck_operator_residue/voice_leading_sim_null/main/{galcut20,none}_ell{2,3}/voice_leading_sim_null_summary.json
reports/planck_operator_residue/voice_leading_sim_null/sensitivity/{galcut20,none}_ell3_n{0p5,2p0}/voice_leading_sim_null_summary.json
```

Calibration of the Episode 2 finding (all 6/6 voice pairs of the four
Planck PR3 algorithms triggered the parallel-fifths analog at ell=3
under galcut20). 1000 ΛCDM low-ell realizations per condition,
surrogate operator-noise added to four independent "pipelines" on the
same underlying sky. Detector parameters frozen from Episode 2 and
imported verbatim from `counterpoint_voice_leading.py`.

Headline at noise=1.0x:

| condition | P(≥6 pairs) | observed Planck percentile | median rot-axis disp |
| --- | ---: | ---: | ---: |
| galcut20, ell=3 | 0.0% (0/1000) | 100.0 | 42.8° |
| none, ell=3 | 0.0% (0/1000) | 100.0 | 38.3° |
| galcut20, ell=2 | 0.0% (0/1000) | bulk (P(2)=4.0%) | 37.8° |
| none, ell=2 | 0.0% (0/1000) | bulk | 41.6° |

Sensitivity sweep at ell=3 across noise=0.5x/1.0x/2.0x:

| condition | noise=0.5x | noise=1.0x | noise=2.0x |
| --- | ---: | ---: | ---: |
| galcut20 P(≥6) | **1.4%** (14/1000) | 0.0% | 0.0% |
| none P(≥6) | 0.2% (2/1000) | 0.0% | 0.0% |

Two readings: (a) the headline survives across noise scales — observed
Planck 6/6-pair pattern at ell=3 galcut20 sits at 98.6-100.0 percentile
across all three; (b) at noise=0.5x (closest match to Episode 2's
observed rotation-axis dispersion ~12°), galcut20 produces 7× more
≥6-pair events than the no-mask baseline. Mask geometry alone, in this
surrogate model, contributes meaningfully to lockstep but is not
sufficient to reproduce the observed pattern.

The ell=2 observed value (2/6 pairs from Episode 2) is not anomalous
against this null — confirms Episode 2's read that the headline
anomaly is specifically at ell=3.

Forbidden claims (also stated in the report):

> The null does not refute the Pipeline Independence Postulate (we
> test surrogates, not real Planck pipelines). ΛCDM is not ruled out.
> AOC is not confirmed by Sprint D — the AOC-positive Episode 4 work
> is the Kerr-interior λ_K derivation.

### Sprint C-prime — per-operator octave-pair duet sonification

```text
empirical/planck_operator_residue/sonify_octave_pair_duets.py
reports/planck_operator_residue/sonification_octave_pair_duets/{commander,nilc,sevem,smica}_duet.wav
reports/planck_operator_residue/sonification_octave_pair_duets/all_pipelines_sequential.wav
reports/planck_operator_residue/sonification_octave_pair_duets/sonification_octave_pair_duets_score.png
reports/planck_operator_residue/sonification_octave_pair_duets/sonification_octave_pair_duets_report.md
```

Auditory companion to Sprint D. Each operator's ell=2 + ell=3 pair as
a 2-voice duet (~13s) with mask transition. The Episode 2 8-voice
sonification chord-fused at ell=2 and obscured per-pipeline Q-O
detuning; the duet form isolates that feature.

Per-operator Q-O detuning (cross-octave alignment angle, unmasked →
galcut20 → delta):

| operator | unmasked | galcut20 | delta |
| --- | ---: | ---: | ---: |
| Commander | 17.5° | 30.6° | +13.1° |
| NILC | 5.6° | 28.3° | **+22.8°** |
| SEVEM | 16.3° | 35.1° | +18.8° |
| SMICA | 7.4° | 26.4° | +19.0° |

NILC has the cleanest before/after reading (near-octave 5.6° unmasked
→ clearly detuned 28.3° galcut20). All four loosen monotonically
under masking. ~80% confidence the duet voicing makes per-pipeline
Q-O detuning more inspectable than the 8-voice voicing; not dramatic
on a casual listen.

### λ_K Kerr-interior strategy seed doc (gesture/near-cousin class)

```text
docs/lambda_k_kerr_interior_strategy.md
```

178 lines. Phase tag at top: "near-cousin / gesture, NOT derivation,
NOT instantiation." Five chip-able open milestones framed as
questions, including: "Does the Kerr-interior near-cousin predict the
parallel-fifths-at-ell=3 block-motion finding, or is it orthogonal to
interior dynamics?" and "What is the minimal first-pass derivation
that lands a number for λ_K from apparatus-bound K of one live
pipeline without fitting-then-evaluating on the same data?"

~60% confidence on Kerr-interior structural similarity to AOC's
gesture (40% reservation: bounded observer not yet pinned to interior
observer of compact rotating object; Kerr is vacuum vs reconstruction-
frame; other near-cousins carry partial ingredients). Five
phase-line-risk reminders embedded as inline comments, with the
highest-risk passage (mention of v0 fitted numbers) explicitly
labeled to prevent a future agent reading exploratory fits as a
derivation.

This is the Episode 3 → Episode 4 hand-off. λ_K derivation work is
deferred to Episode 4 by design.

### What this lands

Three publication-grade artifacts (Sprint D report, Sprint C-prime
report, λ_K seed doc); one canonical glossary entry; one strategy
doc (`docs/music_paint_technique_strategy.md` from Episode 2 still
applies and lists Sprint D as the empirical-class extension landed
here).

Episode 3 hits four classes:
- **Empirical**: Sprint D + the prior session's P1/P2/P3 contract pay-off (frozen-then-tested predictions).
- **Methodological**: Sprint D detector imported and frozen; sim-null framework cast in voice-leading language.
- **Communication**: per-operator duet sonification + Pipeline Independence Postulate canonicalized.
- **Epistemological**: λ_K seed doc opens the gesture-to-near-cousin engagement target for Episode 4.

Sprint E (prismatic decomposition rigor) deferred to Episode 4 by user decision.

## 2026-04-28: Music/Paint Technique Import — Three Parallel Sprints

Added three cross-modal artifacts over the corrected ell=2/ell=3 directional
operator-residue axes, executed by parallel agents under a music-and-paint
technique-import strategy. Strategy doc:
`docs/music_paint_technique_strategy.md`. Framework license: the AOC
primitive that geometricity originates from observer measurement (so paint
and music technique imports are inheriting crystallized observer-discipline,
not decoration).

Phase tag for all three: composition / methodology import, not new evidence.
Allowed/forbidden claims sections explicit in each report.

### Sprint B — Opticks v2 (saturation/value extension)

```text
empirical/planck_operator_residue/build_opticks_axis_residue_map_v2.py
reports/planck_operator_residue/opticks_axis_residue_map_v2/opticks_axis_residue_map_v2_report.md
reports/planck_operator_residue/opticks_axis_residue_map_v2/opticks_axis_residue_map_v2.svg
reports/planck_operator_residue/opticks_axis_residue_map_v2/opticks_axis_residue_map_v2.csv
reports/planck_operator_residue/opticks_axis_residue_map_v2/opticks_axis_residue_map_v2_summary.json
```

Saturation = per-multipole-normalized score amplitude with 0.18 floor for
legibility. Value held in reserve at 1.0 (deliberate under-use; flagged in
the conversion contract). Non-obvious finding: galcut20 marks are uniformly
desaturated (sat 0.34-0.43) while unmasked has full range (0.41-1.00). The
mask is visibly *flattening* score amplitudes across operators, not just
shifting their positions. ~95% confidence on saturation-as-faithful-encoding
of score amplitude.

### Sprint C — Sonification of voice drift

```text
empirical/planck_operator_residue/sonify_voice_drift.py
reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift.wav
reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift_score.png
reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift_report.md
reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift_summary.json
```

Four operators -> four sine voices, longitude -> exponential pitch sweep
within an octave (220-440 Hz for ell=2, 440-880 Hz for ell=3), latitude ->
equal-power stereo pan, mask state -> piece-time (12s + 3s crossfade + 12s).
27 seconds total, 44.1 kHz stereo.

Honest null on the strong claim: the dominant audible feature is the
*opposite* of what the original brief framed. The ell=2 chord goes from a
118-cent rough cluster (unmasked) to a 34-cent near-unison (galcut20) — i.e.
the four voices *fuse* under masking, matching operator-axis dispersion
dropping from 14.1° to 4.6°. The cross-octave Q-O detuning per operator
(11.9° -> 29.5°) is encoded faithfully but is not the dominant audible
feature in this 8-voice voicing. ~30% confidence sonification reveals
patterns visual doesn't on this dataset; ~95% the methodology import is
well-formed. Methodological lesson: compositional structure determines which
feature is audible; a per-operator octave-pair duet voicing would surface
Q-O detuning more clearly than the simultaneous 8-voice chord.

### Sprint A — Counterpoint voice-leading (substantive read)

```text
empirical/planck_operator_residue/counterpoint_voice_leading.py
reports/planck_operator_residue/counterpoint_voice_leading/counterpoint_voice_leading_report.md
reports/planck_operator_residue/counterpoint_voice_leading/counterpoint_voice_leading_summary.json
reports/planck_operator_residue/counterpoint_voice_leading/voice_leading_score_ell2.png
reports/planck_operator_residue/counterpoint_voice_leading/voice_leading_score_ell3.png
```

Four operators as four spherical voices; unmasked → galcut20 transition as a
two-chord progression. Per-voice Δ = arccos(|<u_unmasked, u_galcut>|).
Forbidden-motion rules adapted for sphere geometry: parallel-fifths analog
(matched Δ within 5° + rotation axes within 15°), voice crossing
(self-motion exceeds unmasked pair separation), hidden unison (arrival
within 5° from >15° starting separation).

Voice-leading distance matrix:

| voice | Δ at ell=2 (deg) | Δ at ell=3 (deg) |
| --- | ---: | ---: |
| Commander | 23.3 | 22.1 |
| NILC | 28.3 | 22.9 |
| SEVEM | 42.3 | 26.3 |
| SMICA | 26.4 | 21.9 |

Forbidden-motion findings:

| rule | ell=2 | ell=3 |
| --- | ---: | ---: |
| parallel_fifths | 2 pairs | **all 6 pairs** |
| voice_crossing | 11 directed | 12 directed |
| hidden_unison | 2 (both SEVEM) | 0 |

Headline read: at ell=3 every voice pair triggers parallel-fifths (matched
Δ within 5°, rotation axes aligned within 12°). The four pipelines move as
a single block under masking, not as four independent recoveries. This is a
music-theoretic restatement of "the galcut20 transformation is shared
across pipelines, not pipeline-independent verification." That has
methodological weight: pipeline-agreement under masking may be tautological
rather than confirmatory at ell=3.

At ell=2 the chord is partly independent (only 2/6 parallel-fifths), with
SEVEM as the rule-violating outlier (Δ=42°). The two hidden-unison flags
both involve SEVEM rejoining the cluster under the cut — a music-theoretic
restatement of the SEVEM-as-outlier fact already in the parent directional
report.

Confidence on the import-strategy: ~80% the rule-set captures structurally
relevant patterns; ~60% the specific numeric thresholds would survive
calibration against a CMB-only null simulation. Rules more confident than
numbers attached to them.

### What this lands

Three publication-grade artifacts; one strategy doc; one auto-memory
primitive (geometricity originates from observer measurement); one feedback
memory (cross-modal inspection layers are legitimate). The technique-import
demonstrates the geometricity-from-observation primitive cuts something
real: paint and music technique stacks port cleanly into directional-axis
analysis, with one substantive methodological insight (block-motion at
ell=3) and two honest nulls (sonification doesn't out-perform visual on
this dataset; counterpoint thresholds are uncalibrated).

Next moves (not in-session):

- Sprint D: forbidden-motion null cast in voice-leading language. Sim-level
  null on the parallel-fifths block-motion finding at ell=3 — the
  empirical-class test.
- Sprint C-prime: per-operator octave-pair sonification (one voice + its
  octave-mate) to surface Q-O detuning that the 8-voice chord obscured.
- Sprint E: prismatic decomposition rigor as triple-prism robustness
  framing.

## 2026-04-28: P3 Official-Mask Morphology Sweep

Downloaded the official Planck 2018 Component Separation common temperature
mask and ran the first P3 official-mask morphology control:

```text
data/raw/planck_operator_residue/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
docs/planck_p3_official_mask_contract.md
empirical/planck_operator_residue/directional_axis_official_mask_morphology.py
reports/planck_operator_residue/directional_axis_official_mask_morphology/
```

Exact source:

```text
https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
```

Frozen morphology family: conservative `nside=64` downgrade, then
`erode2, erode1, base, dilate1, dilate2`. Frozen decision threshold:
`max adjacent Q-O jump >= 30 deg` means official-mask morphology preserves a
cliff-like recomposition in this first sprint control.

Result:

| mask | f_sky | median Q-O |
| --- | ---: | ---: |
| erode2 | 0.1144 | 82.8 |
| erode1 | 0.3358 | 38.1 |
| base | 0.6670 | 27.7 |
| dilate1 | 0.8084 | 18.6 |
| dilate2 | 0.8386 | 13.3 |

Largest adjacent jump: `44.7 deg` at `erode2 -> erode1`, above the frozen
`30 deg` decision threshold. P3 first-pass result:
`official_morphology_preserves_cliff_like_recomposition`.

Forbidden-claims discipline: this is not AOC evidence, not a Planck
likelihood, and not a full official-mask null. The largest jump involves a
very severe erosion (`f_sky=0.1144`), so the next official-mask control should
use a less extreme morphology grid and an isotropic null on the same official
mask family.

## 2026-04-28: P2 High-Ell Leakage Threshold Null

Ran the second frozen prediction/control from the Planck directional threshold
contract:

```text
empirical/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null.py
reports/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null/
```

This extends the galcut threshold-sweep null from ell=2/3-only skies to
isotropic Gaussian skies through `ell=30`, then extracts pseudo ell=2/3 across
the same synthetic cut family.

Frozen P2 boundary:

```text
tail(max_adjacent_jump_deg >= 51.51 deg) > 0.05
  -> simple high-ell leakage plausibly explains the cliff under this control
tail <= 0.05
  -> simple high-ell leakage does not explain the cliff under this control
```

Headline from 1000 seeds:

| metric | observed | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `jump_20_25_deg` | 51.51 | 5.02 | 0.29-22.40 | 0.004 |
| `max_adjacent_jump_deg` | 51.51 | 13.21 | 4.71-43.22 | 0.021 |

Verdict: P2 returns `leakage_does_not_explain_under_control`. High-ell leakage
broadens the look-elsewhere null slightly relative to the low-ell-only sweep
(`0.017 -> 0.021`) but remains below the frozen `0.05` decision boundary.

Forbidden-claims discipline: this is not AOC evidence and not a Planck
likelihood. It only says that simple isotropic high-ell leakage, under this
synthetic-mask/fallback-extractor control, does not make the observed adjacent
recomposition cliff ordinary. Next meaningful test: P3 official-mask
specificity and/or extractor robustness.

## 2026-04-28: P1 Fine-Cut Prediction Evaluation

Ran the first frozen prediction from the Planck directional threshold contract:

```text
py -3.11 empirical/planck_operator_residue/directional_axis_galcut_sweep.py \
  --cuts 20,21,22,23,24,25 \
  --out-dir reports/planck_operator_residue/directional_axis_galcut_fine_sweep
```

P1 predicted that the coarse `20 -> 25 deg` Q-O cliff would localize inside
`22 -> 25 deg`, would not distribute evenly across one-degree steps, and would
show coherent ell=2 sector recomposition in at least three of four operators.

Result:

| step | Q-O change |
| --- | ---: |
| `20 -> 21` | `3.06 deg` |
| `21 -> 22` | `1.07 deg` |
| `22 -> 23` | `7.40 deg` |
| `23 -> 24` | `38.87 deg` |
| `24 -> 25` | `1.10 deg` |

The largest adjacent jump is `23 -> 24 deg`, inside the predeclared
localization window. Ell=2 sector recomposition across that step is coherent
in three of four operators: Commander, NILC, and SMICA move from G to F; SEVEM
stays in G.

Verdict: P1 is supported under the fallback extractor and synthetic
latitude-cut contract. This supports the narrower interpretation that the
coarse cliff is not just five-degree binning, but it is not AOC evidence and
does not remove the high-ell leakage or official-mask controls.

## 2026-04-28: Planck Directional Threshold Prediction Contract

Froze the next-run prediction contract before running further threshold
controls:

```text
docs/planck_directional_threshold_prediction_contract.md
```

The contract converts the observed galcut sweep into predeclared next tests
rather than post-hoc interpretation. Core theory-shaped forecast: if the
threshold feature is a feasibility-boundary recomposition rather than smooth
mask drift, the next controls should expose a localized adjacent cliff, not a
uniform deformation.

Frozen predictions:

1. Fine-cut localization over `20, 21, 22, 23, 24, 25 deg`: largest adjacent
   Q-O jump should localize inside `22 -> 25 deg`, with at least three of four
   operators participating in the ell=2 sector recomposition.
2. High-ell leakage threshold null: leakage should broaden the null. If it
   fully explains the Planck cliff, the look-elsewhere tail for a `51.51 deg`
   jump should rise above `0.05`; if not, it should remain below `0.05`.
3. Official-mask specificity: a purely synthetic-latitude artifact should not
   reproduce a comparable adjacent cliff under official-mask morphology; an
   instrumentation-bound recomposition may reappear at a different sky fraction
   or threshold.

Forbidden-claims discipline: this is not AOC evidence and not an
instantiation-grade axis prediction. It is a frozen next-control contract that
prevents the next sprint from quietly moving the target after seeing results.

## 2026-04-28: Directional Axis Galcut Sweep Null

Added the isotropic low-ell threshold-sweep null for the synthetic galactic-cut
directional curve:

```text
empirical/planck_operator_residue/directional_axis_galcut_sweep_null.py
reports/planck_operator_residue/directional_axis_galcut_sweep_null/
```

This controls the Opticks-induced hypothesis from the previous artifact and
the observed Planck sweep: does the `20 -> 25 deg` Q-O cliff occur commonly
under isotropic ell=2/ell=3 skies with the same synthetic mask family?

Headline from 1000 seeds:

| metric | observed | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `jump_20_25_deg` | 51.51 | 3.87 | 0.00-16.62 | 0.002 |
| `max_adjacent_jump_deg` | 51.51 | 8.54 | 3.18-38.55 | 0.017 |

Readout: the `cut=25 deg` Q-O value alone is not the core signal
(`tail >= observed = 0.118`). The rare object is the adjacent recomposition:
the observed curve stays in a controlled G-to-A drift through `20 deg`, then
jumps by `51.5 deg` at `25 deg`. Under this low-ell isotropic sweep null,
that named cliff is uncommon, and a cliff this large anywhere in the seven-cut
sweep remains uncommon at the ~1.7% level.

Forbidden-claims discipline: this is not evidence for AOC, not a full Planck
likelihood, and not a component-separation or foreground simulation. Next
control: repeat the threshold-sweep null with high-ell leakage and/or official
Planck masks to test whether the cliff is a mask/leakage artifact of the
fallback contract.

## 2026-04-28: Directional Axis Galcut Sweep

Added a synthetic galactic-cut threshold sweep for the corrected ell=2/ell=3
directional statistic:

```text
empirical/planck_operator_residue/directional_axis_galcut_sweep.py
reports/planck_operator_residue/directional_axis_galcut_sweep/
```

This was motivated by the Opticks artifact: unmasked axes occupied one
color/note sector, while the `|b|>20 deg` extraction pushed the octupole into
the next sector. The sweep tests whether that was merely visual compression or
whether it tracks a measurable mask-threshold response.

Readout over synthetic cuts `0, 5, 10, 15, 20, 25, 30 deg`: from `0` to
`20 deg`, the axes drift coherently from the G sector toward A and the Q-O
angle weakens from `8.6 deg` to `29.5 deg`. Between `20` and `25 deg`, the
median Q-O angle jumps to `81.0 deg`, ell=2 recomposes into F, and ell=3 moves
toward A/B. This is the first concrete threshold-sweep signature of the mask
contract changing the directional chart.

Forbidden-claims discipline: this is not evidence for AOC, not an official
Planck mask analysis, and not a cosmological phase-transition claim. It is a
fallback-extractor synthetic-mask response curve. Next control: run an
isotropic masked-sky threshold-sweep null to ask whether the `20 -> 25 deg`
jump is typical under the same mask family.

## 2026-04-28: Opticks Axis-Residue Map

Added the first Opticks-style composition layer over the Planck low-ell
directional-axis products:

```text
empirical/planck_operator_residue/opticks_axis_residue_map.py
reports/planck_operator_residue/opticks_axis_residue_map/
```

The conversion contract is explicit: galactic longitude becomes hue, galactic
latitude becomes radial distance from the galactic north pole, and a sevenfold
note label is assigned by hue sector. This preserves circular order, operator
clustering, Q-O separation, and mask-state shift while discarding physical
wavelength identity, exact pitch, and statistical force.

Readout: the artifact visually recovers the same empirical structure as the
directional reports. The unmasked axes compose into a nearby hue/radius
neighborhood with median Q-O alignment `11.9 deg`; the synthetic `|b|>20 deg`
cut shifts both multipoles and weakens the composition to `29.5 deg`.

Allowed claim: this is disciplined media/composition instrumentation over
existing directional products. Forbidden claim: it is not evidence for AOC,
not a physical music measurement, and not a substitute for the null controls.

## 2026-04-28: Directional Axis High-Ell Leakage Null

Extended the masked-sky directional null by adding Gaussian multipoles through
`ell=30` before applying the synthetic galactic cut:

```text
empirical/planck_operator_residue/directional_axis_high_ell_leakage_null.py
reports/planck_operator_residue/directional_axis_high_ell_leakage_null/
```

This tests whether high-ell leakage through the mask changes the feasibility
contract for interpreting the low-ell Q-O alignment shift. It still does not
simulate Planck component separation, beam, detector noise, foregrounds,
inpainting, or an official Planck mask.

Headline from 1000 seeds:

| metric | observed | null median | tail |
| --- | ---: | ---: | ---: |
| unmasked Q-O angle | 11.9 deg | 60.0 deg | 0.020 |
| masked Q-O angle | 29.5 deg | 56.6 deg | 0.854 |
| mask-state Q-O delta | +17.6 deg | -1.9 deg | 0.165 |
| joint: unmasked <= 11.9 deg and delta >= 17.6 deg | observed thresholds | -- | 0.012 |

Readout: extending the feasible contract from low-ell-only mask geometry to
high-ell leakage increases the out-of-contract band from ~11% to 16.5%.
That is the important discipline: the pivot-regime number is contract-
dependent, not universal. The invariant is that structured residue outside
the current routing contract forces recomposition before interpretation. The
joint event remains uncommon (~1.2%), but the mask-delta alone is increasingly
explained by mask/leakage mechanics rather than by anything AOC-specific.

Next empirical control: replace the simple `1/[ell(ell+1)]` power law with a
fiducial LambdaCDM `C_ell` and, if available, replace the synthetic galactic
cut with an official Planck common mask.

## 2026-04-28: Directional Axis Masked-Sky Null

Added the first direct mask-geometry null for the corrected ell=2/ell=3
directional statistic:

```text
empirical/planck_operator_residue/directional_axis_masked_sky_null.py
reports/planck_operator_residue/directional_axis_masked_sky_null/
```

This null draws isotropic ell=2 and ell=3 Gaussian skies with
`C_ell proportional to 1/[ell(ell+1)]`, synthesizes a map, applies the
same synthetic galactic cut (`|b|>20 deg`, `f_sky=0.6580`), extracts
mean-subtracted direct pseudo-alms, and reruns the m=ell-maximizing
axis statistic. It tests mask geometry directly, without component
separation, beam, noise, high-ell leakage, or official Planck masks.

Headline from 1000 seeds:

| metric | observed | null median | tail |
| --- | ---: | ---: | ---: |
| unmasked Q-O angle | 11.9 deg | 59.0 deg | 0.020 |
| masked Q-O angle | 29.5 deg | 54.3 deg | 0.836 |
| mask-state Q-O delta | +17.6 deg | -2.4 deg | 0.113 |
| joint: unmasked <= 11.9 deg and delta >= 17.6 deg | observed thresholds | -- | 0.008 |

Readout: mask geometry alone can produce Q-O weakening of this size in
roughly 11% of restricted low-ell isotropic draws. In the ICML/Principia
language, this is not "the pivot" and not mere uncertainty; it is
out-of-contract residue. The current smooth continuation contract says mask
geometry should not drive this much Q-O recomposition, and ~11% of restricted
draws violate that contract. That residue forces recomposition into a richer
control contract rather than supporting either dismissal or anomaly-claiming.
The joint event remains uncommon (~0.8%): first get an already-tight unmasked
Q-O alignment, then have the mask weaken it by at least the observed amount.

Forbidden-claims discipline: this is not evidence for AOC, not a refutation
of LambdaCDM, and not a full Planck likelihood control. The next empirical
control is high-ell Gaussian content plus official Planck/common masks, so
leakage and mask specificity can be tested rather than assumed.

## 2026-04-28: Directional Axis Coefficient-Space Null

Added the first simulation-level control for the corrected ell=2/ell=3
directional statistic:

```text
empirical/planck_operator_residue/directional_axis_null_sim.py
reports/planck_operator_residue/directional_axis_null_coeffspace/
```

This is a coefficient-space isotropic common-sky null, not a full Planck
component-separation or masked-sky simulation. Each seed draws one common
isotropic ell=2 and ell=3 sky, then gives four mock operators independent
coefficient noise calibrated from the observed pairwise coefficient distances.
The unmasked and galcut20 conditions share the same synthetic sky and differ
only by calibrated operator-noise level.

Calibration (`C_noise / C_sky`):

| condition | ell=2 | ell=3 |
| --- | ---: | ---: |
| unmasked | 0.0737 | 0.0123 |
| galcut20 | 0.00267 | 0.0134 |

Headline from 1000 seeds:

| metric | observed | null median | tail |
| --- | ---: | ---: | ---: |
| unmasked median Q-O angle | 11.9 deg | 59.2 deg | 0.007 |
| galcut20 median Q-O angle | 29.5 deg | 58.4 deg | 0.134 |
| mask-state Q-O delta | +17.6 deg | -0.3 deg | 0.025 |
| unmasked ell=3 operator-axis dispersion | 3.34 deg | 5.72 deg | 0.119 |
| galcut20 ell=2 operator-axis dispersion | 4.62 deg | 3.67 deg | 0.657 |

Readout: the unmasked Q-O alignment is atypically tight under this
coefficient-space isotropic null. The mask-state weakening is also unlikely
if the two conditions differ only by calibrated operator noise. This supports
the earlier interpretation that the mask operation itself is load-bearing.

Forbidden-claims discipline: this is not evidence for AOC, not a refutation
of LambdaCDM, and not a full CMB likelihood control. It narrows the next
empirical move: replace the coefficient-space null with a masked-sky CMB null
using Gaussian skies, the synthetic galactic cut or official Planck common
mask, pseudo-alm extraction, and the same m=ell-max axis statistic.

## 2026-04-29: Planck Operator-Residue Directional Analysis at ell=2

Added a directional (axial) test of the operator-residue handle at ell=2.
Quadrupole tensor decomposition of each operator's own alms and each
pair's residual alms, principal-axis extraction, comparison across
operators and pairs, comparison against published low-ell anomaly axes.

Tests the *axial* feature of the gestural conjecture under a self-
similarity reading: physical (operator quadrupole) and epistemic (pair
residue) manifolds should share preferred-axis structure if bounded-
observer cosmology holds.

Added:

```text
empirical/planck_operator_residue/directional_residue_axis.py
reports/planck_operator_residue/directional_axis_nside64/
reports/planck_operator_residue/directional_axis_nside64_galcut20/
reports/planck_operator_residue/directional_axis_comparison.md
```

Headline:

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| operator-axis median pairwise dispersion (deg) | 41.3 | **1.6** |
| pair-residue-axis median pairwise dispersion (deg) | 81.2 | 43.6 |

On the clean sky (galcut20, `f_sky=0.66`), the four Planck PR3 component-
separation operators independently reconstruct the same ell=2
quadrupole axis to within **1.6°** of each other at galactic
`(l≈68°, b≈58°)`. SEVEM joins the cluster once the galactic plane is
removed (it was the unmasked outlier).

Self-similarity readout: at ell=2 in this realization, physical
(operator quadrupole) and epistemic (pair residue) preferred axes do
**not** coherently align. The physical axis is well-determined; the
epistemic axes are dispersed (43.6° median), with two of six pair
residues clustering near the published axis-of-evil direction (both
involving NILC; not significant under look-elsewhere correction).

Status: this is a near-cousin-phase test that produces real data on the
axial feature. The strongest finding is the operator-axis convergence;
the self-similarity test returns null at ell=2 in this single
realization. It is not a refutation — cosmic variance at ell=2 is
enormous, and residual power is small enough that sub-leading structure
may dominate the residual axis even if a deeper axial feature exists.

Forbidden-claims discipline preserved in the comparison report.

Next directional moves flagged: ell=3 (octupole) tensor analysis;
simulation-level null on the directional statistic; theory-derived
axis prediction from the proof spine.

## 2026-04-29 (later): Octupole + methodology correction

Added ell=3 m=ℓ-maximizing axis search and re-did ell=2 with the same
m=ℓ-max methodology (the original tensor-largest-|eigenvalue| can flip
~90° depending on eigenvalue sign — three of four operators had
largest-|eigenvalue| negative in the unmasked case).

Headline:

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| operator-axis dispersion (ell=2 m=ℓ-max) | 14.1° | 4.6° |
| operator-axis dispersion (ell=3 m=ℓ-max) | 3.3° | 5.1° |
| **Median quadrupole-octupole alignment** | **11.9°** | **29.5°** |

The published axis-of-evil / Q-O alignment phenomenon is **reproduced
in our unmasked operator-residue framework**: ell=3 axis at galactic
`(243°, 64°)`, within 3° of the Schwarz 2004 reference and 9° of the
Land-Magueijo 2005 reference, with median Q-O alignment 11.9° (within
the published 5-15° band). Masking weakens the alignment to ~30°,
consistent with one common reading of the literature (alignment
partly foreground-driven).

Status: methodological validation that the operator-residue framework
reads the data correctly. **Not** evidence for AOC — reproducing a
known phenomenon doesn't distinguish AOC from any other observer-
bounded reconstruction framework. Self-similarity at the operator
level (physical axis vs epistemic pair-residue axis) is not supported
in either mask state at either ell=2 or ell=3 in this single-
realization measurement.

Forbidden-claims discipline preserved.

Added:

```text
empirical/planck_operator_residue/directional_residue_axis_octupole.py
empirical/planck_operator_residue/directional_residue_axis_quadrupole_mlmax.py
reports/planck_operator_residue/directional_axis_nside64/directional_octupole_axis_summary.json
reports/planck_operator_residue/directional_axis_nside64/directional_quadrupole_mlmax_summary.json
reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_octupole_axis_summary.json
reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_quadrupole_mlmax_summary.json
```

Updated `reports/planck_operator_residue/directional_axis_comparison.md`
with octupole, methodology-corrected ell=2, joint Q-O alignment, and
updated allowed/forbidden claims.

## 2026-04-28: Planck Operator-Residue Mask-Aware Phase Null

Added a second null control on the Planck operator-residue handle: a
mask-aware phase-randomized null using a synthetic galactic-plane cut
`|b|>20°` (`f_sky=0.6615`).

Added:

```text
empirical/planck_operator_residue/extract_planck_lowell_fallback_masked.py
data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.manifest.json
reports/planck_operator_residue/phase_null_nside64_galcut20/
reports/planck_operator_residue/phase_null_nside64_galcut20/mask_aware_comparison.md
```

Updated:

```text
reports/planck_operator_residue/planck_operator_residue_first_contact.md
reports/README.md
```

Headline (`2 <= ell <= 30`, 1000 phase-randomized seeds, seed 20260428):

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| observed median pairwise distance | 0.337761 | 0.041244 |
| null median | 1.414070 | 1.414207 |
| fraction null <= observed | 0 / 1000 | 0 / 1000 |

Plain English:

> Removing the galactic plane drives observed cross-operator distance *down*
> by an order of magnitude. The phase-randomized null is essentially
> unchanged. The four pipelines agree more tightly outside the plane, not
> less. The unmasked SEVEM-vs-others gap is dominated by galactic-plane
> disagreement and disappears outside the plane.

Status: this is a mask-aware control win for the operator-residue handle.
It rules out the "the alignment is just a galactic-plane artifact"
hypothesis. It does NOT separate "shared cosmic sky" from "operator-bound
apparatus signal" — that separation requires a simulation-level null with
a controlled input sky. Forbidden-claims discipline preserved in
`mask_aware_comparison.md`.

Cross-band split (added in same sprint): `2 <= ell <= 10` and `11 <= ell <= 30`
re-runs of the phase null on both unmasked and galcut20 alms.

| band | unmasked observed | galcut20 observed |
| --- | ---: | ---: |
| `2 <= ell <= 10`  | 0.246507 | 0.039510 |
| `11 <= ell <= 30` | 0.377989 | 0.041605 |
| `2 <= ell <= 30`  | 0.337761 | 0.041244 |

The galcut20 distance is band-flat. The unmasked band structure (worse at
high ell) tracks foreground residuals, not multipole physics. Analytic
reading: implied noise-to-signal variance ratio `Cn/Cs ~ distance^2 / 2`
gives `~0.08%` on the clean sky and `~5.7%` unmasked.

Next controls flagged: official Planck PR3 common-Int mask; CMB-only
simulation null with external pipeline-noise spec (the shared-fraction
analytic does not separate "no apparatus signal" from "apparatus signal
buried under pipeline noise floor"; only the simulation null can).

## 2026-04-28: Principia Alignment Guardrail Added

Added:

```text
docs/aoc_principia_alignment_audit.md
```

Updated:

```text
README.md
docs/glossary.md
docs/repo_operating_loop.md
```

Reason:

The program had begun to drift toward treating AOC primarily as a
distance-deformation model. The updated entry points now restore the
Principia-aligned orientation:

```text
observer horizon -> escape horizon -> observable-specific empirical map
```

Canonical correction:

> The Big Bang is treated as a candidate observer-relative escape horizon, not
> as a denied event or a directly inspectable pre-boundary state.

Practical consequence:

The next aligned empirical target is operator-residue analysis: compare
multiple reconstruction operators on the same target, then ask what stable
boundary-adjacent structure survives the operator change. The first candidate
is Planck component-separated CMB maps (`Commander`, `NILC`, `SEVEM`, `SMICA`).

## 2026-04-28: Planck Operator-Residue Branch Started

Added:

```text
empirical/planck_operator_residue/README.md
empirical/planck_operator_residue/planck_operator_residue_contract_v0.md
empirical/planck_operator_residue/extract_planck_lowell.py
empirical/planck_operator_residue/extract_planck_lowell_fallback.py
empirical/planck_operator_residue/analyze_lowell_operator_residue.py
empirical/planck_operator_residue/requirements.txt
data/raw/planck_operator_residue/PROVENANCE.md
```

Generated verification artifacts:

```text
data/derived/planck_operator_residue/example_lowell_alm.csv
reports/planck_operator_residue/example_run/
```

Purpose:

Define the first operator-residue contract for AOC using Planck
component-separated CMB maps as explicit reconstruction operators:

```text
Commander, NILC, SEVEM, SMICA
```

Predeclared input layer:

```text
operator, ell, m, alm_real, alm_imag
```

Predeclared metrics:

1. low-ell `C_ell`,
2. normalized spectral entropy,
3. odd/even low-ell parity ratio,
4. pairwise coefficient distance across operators,
5. median pairwise distance as operator-residue stability score.

Environment note:

The local Python environment has `numpy` but not `healpy` or `astropy`, so the
current executable layer starts from exported low-ell coefficients rather than
directly reading Planck FITS maps. The synthetic example run verifies the metric
pipeline only; it is not a Planck result.

Update:

`healpy` failed to install cleanly on the local Windows Python stack because it
attempted a native `cfitsio` build. The branch now includes a fallback extractor
using `astropy`, `astropy-healpix`, and direct low-resolution quadrature. This
fallback is acceptable for first contact but not final CMB harmonic claims.

Allowed claim:

> AOC now has a predeclared Planck operator-residue contract and a runnable
> low-ell metric pipeline.

Forbidden claim:

> The example run says anything about the real CMB, Planck anomalies, torque,
> white-hole leakage, or AOC.

## 2026-04-28: Planck Operator-Residue First Contact

Downloaded:

```text
data/raw/planck_operator_residue/maps/COM_CMB_IQU-commander_2048_R3.00_full.fits
data/raw/planck_operator_residue/maps/COM_CMB_IQU-nilc_2048_R3.00_full.fits
data/raw/planck_operator_residue/maps/COM_CMB_IQU-sevem_2048_R3.00_full.fits
data/raw/planck_operator_residue/maps/COM_CMB_IQU-smica_2048_R3.00_full.fits
```

Generated:

```text
data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside32.csv
data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv
reports/planck_operator_residue/fallback_nside32/
reports/planck_operator_residue/fallback_nside64/
reports/planck_operator_residue/planck_operator_residue_first_contact.md
```

First-contact result:

| run | median pairwise coefficient distance | Commander parity | NILC parity | SEVEM parity | SMICA parity |
| --- | ---: | ---: | ---: | ---: | ---: |
| fallback nside32 | 0.342372 | 1.424730 | 1.469643 | 1.406000 | 1.455541 |
| fallback nside64 | 0.337761 | 1.420728 | 1.467259 | 1.403465 | 1.453378 |

Interpretation:

The nside32 and nside64 fallback runs agree closely, which is a useful
resolution sanity check. NILC and SMICA are very close under the pairwise
coefficient metric; SEVEM is farther from the other operators. The lowest
multipoles are more operator-stable than much of the upper `ell <= 30` band.

Allowed claim:

> A real Planck operator-residue first contact has been executed locally, using
> four component-separated maps and a fallback low-resolution harmonic
> extractor.

Forbidden claim:

> This supports AOC, proves a false bottom, proves torque, or refutes
> `LambdaCDM`.

## 2026-04-28: Planck Phase-Randomized Null Control

Added:

```text
empirical/planck_operator_residue/phase_null_operator_residue.py
reports/planck_operator_residue/phase_null_nside64/
```

Null:

Preserve each operator's low-ell coefficient amplitudes and randomize
cross-operator phase alignment.

Result:

| metric | value |
| --- | ---: |
| observed median pairwise distance | 0.337761 |
| null median | 1.414070 |
| null q05 | 1.386992 |
| null q95 | 1.441485 |
| fraction null <= observed | 0 / 1000 |

Interpretation:

The observed cross-operator closeness is not explained by each operator's
low-ell amplitudes alone. The four component-separated maps share aligned
low-ell structure that phase randomization destroys.

Allowed claim:

> The Planck low-ell operator-residue result survives a coefficient-level
> phase-randomized null control.

Forbidden claim:

> This proves AOC, a false bottom, cosmic torque, or a physical
> origin-boundary effect.

## 2026-04-26: First Real-Data Empirical Contract

Branch:

```text
empirical/pantheon_plus
```

Data:

```text
Pantheon+SH0ES distance table
https://github.com/PantheonPlusSH0ES/DataRelease
```

Local provenance:

```text
data/raw/pantheon_plus/PROVENANCE.md
```

Result:

```text
n_rows = 1701
threshold mu_err_max = 0.20
n_passing = 643
K_P = 1.78928
z_at_K_P = 0.78928
mu_err_at_K_P = 0.165559
```

Interpretation:

This is the first successful computation of a provisional apparatus-bound
`K_P` on a real public cosmology dataset.

Allowed claim:

> AOC's `K` formalism can be computed on a real supernova distance dataset.

Forbidden claim:

> AOC explains cosmic acceleration.

Report:

```text
reports/pantheon_plus/pantheon_k_report.md
```

Figure:

```text
reports/pantheon_plus/pantheon_k_uncertainty.png
```

Next technical improvement:

Replace threshold-only `K_P` with a likelihood-aware or covariance-aware
pipeline estimate, then compare against a baseline `LambdaCDM` distance
relation.

## 2026-04-26: Pantheon+ Threshold Sensitivity and Baseline Residuals

Branch:

```text
empirical/pantheon_plus
```

Added:

1. threshold sweep for `mu_err_max`,
2. simple flat-`LambdaCDM` residual instrument,
3. binned residual table,
4. threshold-sensitivity figure,
5. residual figure.

Threshold sensitivity:

| `mu_err_max` | rows passing | `K_P` | `z_at_K_P` |
| ---: | ---: | ---: | ---: |
| 0.12 | 3 | 1.37153 | 0.37153 |
| 0.15 | 116 | 1.64962 | 0.64962 |
| 0.18 | 414 | 1.78928 | 0.78928 |
| 0.20 | 643 | 1.78928 | 0.78928 |
| 0.22 | 861 | 1.97423 | 0.97423 |
| 0.25 | 1104 | 2.54901 | 1.54901 |
| 0.30 | 1382 | 3.26137 | 2.26137 |

Interpretation:

`K_P` is threshold-sensitive, as expected. This is good: it confirms that `K`
is a pipeline/contract quantity, not a hidden universal constant in this
apparatus-bound framing.

Baseline residual caveat:

The flat-`LambdaCDM` residual plot uses fixed `H0=70` and `Omega_m=0.3` only as
a comparison instrument. It is not a fit and does not use the covariance matrix.

Next technical improvement:

Implement a covariance-aware distance likelihood or use published Pantheon+
cosmology products before making any claim about model comparison.

## 2026-04-26: Pantheon+ Covariance-Aware Diagnostic

Downloaded:

```text
data/raw/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov
```

Provenance:

```text
data/raw/pantheon_plus/PROVENANCE.md
```

Covariance diagnostic:

```text
shape = 1701 x 1701
median sqrt(diag(C)) = 0.155560
median MU_SH0ES_ERR_DIAG = 0.218994
median difference = -0.060976
max absolute difference = 1.33821
```

Baseline residual diagnostic:

```text
model = flat LambdaCDM, H0=70, Omega_m=0.3
constant offset marginalized = -0.105936 mag
chi2 after offset = 1764.19
dof = 1700
chi2/dof = 1.03776
```

Interpretation:

The covariance file makes the branch materially stronger: we can now compute
covariance-aware residual diagnostics. It also shows that table-diagonal and
covariance-diagonal uncertainty definitions are not interchangeable, so both
must be reported separately.

Covariance-diagonal `K_P` sweep:

| sigma threshold | rows passing | `K_P` | `z_at_K_P` |
| ---: | ---: | ---: | ---: |
| 0.12 | 299 | 1.76932 | 0.76932 |
| 0.15 | 783 | 1.97423 | 0.97423 |
| 0.18 | 1150 | 2.54901 | 1.54901 |
| 0.20 | 1310 | 2.54901 | 1.54901 |
| 0.22 | 1430 | 3.26137 | 2.26137 |

Allowed claim:

> AOC's empirical contract can distinguish different reconstruction operators
> or uncertainty definitions on the same public dataset.

Forbidden claim:

> The covariance diagnostic validates AOC over LambdaCDM.

Next technical improvement:

Use the covariance matrix to define `K_P` through a degradation of
model-discriminability or likelihood curvature, not only through diagonal
thresholds.

## 2026-04-26: Pantheon+ Model-Discriminability K

Added:

```text
data/derived/pantheon_plus/pantheon_model_discriminability.csv
reports/pantheon_plus/pantheon_model_discriminability.png
```

Method:

Compare simple alternative distance operators against the fixed flat
`LambdaCDM` baseline over increasing redshift cutoffs. For each cutoff and
model, use the full covariance submatrix and marginalize a constant magnitude
offset. Report:

```text
Delta chi2 = chi2(alternative) - chi2(flat LambdaCDM)
```

The alternatives are comparison instruments, not AOC models:

1. coasting distance law,
2. low-z linear Hubble law extended beyond its valid regime.

Observed pattern:

1. At very low redshift, crude alternatives remain weakly distinguishable after
   offset marginalization.
2. The low-z linear law breaks strongly by approximately `z_cut=0.2`.
3. The coasting law separates more weakly, becoming positive around
   `z_cut=0.35`.

Representative values:

| alternative | `z_cut` | `K_cut` | `Delta chi2` |
| --- | ---: | ---: | ---: |
| linear_low_z | 0.20 | 1.20 | 110.64 |
| linear_low_z | 0.35 | 1.35 | 629.61 |
| coasting | 0.35 | 1.35 | 26.80 |
| coasting | 2.50 | 3.50 | 60.84 |

Interpretation:

This is the first likelihood-shaped `K` instrument in the repo. Instead of
asking only "how far does the diagonal uncertainty remain below a threshold?",
it asks "how deep in redshift does the dataset discriminate one reconstruction
operator from another?"

Allowed claim:

> AOC's empirical contract can define observer depth through
> model-discriminability using a real covariance matrix.

Forbidden claim:

> These comparison alternatives establish or refute AOC.

Next technical improvement:

Replace the placeholder alternatives with an AOC-motivated distance operator
or a one-parameter threshold deformation, then predeclare the comparison rule.

## 2026-04-26: First AOC-Style Threshold Deformation

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_threshold_deformation.csv
reports/pantheon_plus/pantheon_aoc_threshold_deformation.png
```

Probe:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

Properties:

1. `lambda = 0` recovers the fixed flat-`LambdaCDM` baseline exactly.
2. Positive `lambda` makes high-redshift distances dimmer.
3. Negative `lambda` makes high-redshift distances brighter.
4. The form is phenomenological and threshold-shaped; it is not claimed as the
   final AOC distance law.

Best grid values:

| `z_cut` | `K_cut` | best `lambda` | best `Delta chi2` |
| ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.20 | -10.26 |
| 0.35 | 1.35 | -0.15 | -7.39 |
| 0.50 | 1.50 | -0.10 | -9.37 |
| 0.75 | 1.75 | -0.15 | -16.87 |
| 1.00 | 2.00 | -0.10 | -17.47 |
| 1.50 | 2.50 | -0.10 | -11.58 |
| 2.50 | 3.50 | -0.10 | -11.91 |

Interpretation:

The coarse grid prefers a small negative threshold deformation across most
redshift cutoffs. This is interesting but not yet a model-comparison result:
the run does not fit `H0`/`Omega_m`, does not penalize the extra parameter, and
does not pre-register this deformation.

Allowed claim:

> A one-parameter AOC-style threshold deformation can be evaluated against real
> Pantheon+ data with the full covariance matrix.

Forbidden claim:

> Pantheon+ currently supports AOC over `LambdaCDM`.

Next technical improvement:

Add a parameter penalty / information criterion and a finer optimizer for
`lambda`, or predeclare a physically motivated deformation from the AOC proof
spine before further data contact.

## 2026-04-26: Penalized AOC Threshold-Deformation Pass

Updated:

```text
empirical/pantheon_plus/analyze_pantheon_k.py
```

Change:

1. refined `lambda` grid to `[-0.30, 0.30]` in steps of `0.01`,
2. added `Delta AIC`,
3. added `Delta BIC`,
4. updated threshold-deformation figure to show BIC penalty.

Best penalized values:

| `z_cut` | `K_cut` | best `lambda` | `Delta chi2` | `Delta AIC` | `Delta BIC` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.30 | -11.70 | -9.70 | -4.85 |
| 0.35 | 1.35 | -0.13 | -7.65 | -5.65 | -0.46 |
| 0.50 | 1.50 | -0.11 | -9.45 | -7.45 | -2.14 |
| 0.75 | 1.75 | -0.13 | -17.51 | -15.51 | -10.10 |
| 1.00 | 2.00 | -0.12 | -18.11 | -16.11 | -10.69 |
| 1.50 | 2.50 | -0.09 | -11.61 | -9.61 | -4.18 |
| 2.50 | 3.50 | -0.09 | -11.97 | -9.97 | -4.53 |

Interpretation:

After a one-parameter BIC penalty, the threshold deformation remains strongest
around `z_cut=0.75` to `1.00`. This is hypothesis-forming only: the deformation
was introduced after seeing the Pantheon+ branch, so it must not be sold as a
confirmed prediction.

Added preregistration stub:

```text
empirical/pantheon_plus/PREREG_NEXT.md
```

Allowed claim:

> The AOC-style threshold-deformation probe remains evaluable under AIC/BIC
> penalties and shows its strongest exploratory signal near `z_cut=0.75-1.00`.

Forbidden claim:

> This is confirmed evidence for AOC.

Next technical improvement:

Run the predeclared rule on a genuinely separate dataset, a held-out split, or
DESI BAO products.

## 2026-04-26: Exploratory Pantheon+ Heldout Check

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_holdout_validation.csv
reports/pantheon_plus/pantheon_aoc_holdout_validation.png
```

Method:

Use a deterministic object-level split:

```text
split = sha256(CID) first-byte parity
```

For each redshift cutoff, select `lambda` for the AOC-style threshold
deformation on the train side, then evaluate that selected value once on the
holdout side. Repeated rows for the same `CID` stay on the same side.

Holdout result:

| `z_cut` | `K_cut` | train `lambda` | holdout `Delta chi2` | holdout `Delta BIC` |
| ---: | ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.18 | -8.84 | -2.69 |
| 0.35 | 1.35 | -0.12 | -5.74 | 0.74 |
| 0.50 | 1.50 | -0.10 | -6.91 | -0.29 |
| 0.75 | 1.75 | -0.12 | -12.60 | -5.89 |
| 1.00 | 2.00 | -0.13 | -12.04 | -5.32 |
| 1.50 | 2.50 | -0.11 | -6.26 | 0.48 |
| 2.50 | 3.50 | -0.10 | -7.53 | -0.79 |

Interpretation:

The heldout pass is materially better discipline than same-sample reporting:
the same qualitative region remains strongest, around `z_cut=0.75` to `1.00`,
but the BIC improvement is weaker. This is still exploratory because the
deformation form was selected after prior Pantheon+ contact.

Implementation note:

The analyzer now reuses the covariance solve across the whole `lambda` grid for
each subset. This preserves the same statistic while reducing the full
Pantheon+ analysis runtime from roughly `344s` to roughly `14s` on this
machine.

Allowed claim:

> The first AOC-style threshold deformation survives a deterministic Pantheon+
> holdout check as a weak exploratory pattern, with its strongest heldout signal
> near `z_cut=0.75-1.00`.

Forbidden claim:

> The heldout check confirms AOC or explains cosmic acceleration.

Next technical improvement:

Commit a new deformation rule before data contact, then evaluate it on a
separate public dataset or a truly blinded split.

## 2026-04-26: Covariance-Sensitivity Sweep for v0 + v1

Added:

```text
empirical/pantheon_plus/cov_sensitivity_sweep.py
data/derived/pantheon_plus/pantheon_cov_sweep.csv
data/derived/pantheon_plus/pantheon_cov_sweep_summary.json
reports/pantheon_plus/pantheon_cov_sweep.png
```

Motivation:

The v0 and v1 entries above are conditional on the Pantheon+ covariance
being correct. This sweep tests how much that conditioning bites: what if
the analyst should have used a uniformly rescaled covariance `sCov`? Under
this scenario both the fit and the null draw are computed under `sCov`
consistently, so Wilks predicts the null `Delta BIC` distribution stays
centered near `+log(n) - 1 ~ +6.4` independently of `s`, while the
actual-data `Delta BIC` scales as `Delta chi2_observed / s + log(n)`.

Method:

For `s in {0.7, 0.85, 1.0, 1.15, 1.3, 1.5}` and each spec
(`v0_log`, `v1_pow_p1.8`, `v1_pow_p2.0`) at `z_cut = 1.0`, scale the
covariance by `s`, redo the Cholesky, run the actual-data fit, and run a
100-seed null power test. This is a single uniform rescaling, not a
stat/sys decomposition.

Result:

| `s` | spec | actual `Delta BIC` | null median | null p10 | gap to null p10 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.70 | `v0_log` | -18.45 | +6.98 | +4.50 | -22.95 |
| 0.70 | `v1_pow_p1.8` | -17.60 | +6.98 | +4.70 | -22.30 |
| 0.70 | `v1_pow_p2.0` | -17.41 | +7.03 | +4.79 | -22.21 |
| 1.00 | `v0_log` | -10.69 | +6.96 | +4.50 | -15.18 |
| 1.00 | `v1_pow_p1.8` | -10.09 | +6.99 | +4.70 | -14.79 |
| 1.00 | `v1_pow_p2.0` |  -9.96 | +6.99 | +4.78 | -14.74 |
| 1.30 | `v0_log` |  -6.51 | +6.97 | +4.51 | -11.01 |
| 1.30 | `v1_pow_p1.8` |  -6.05 | +6.99 | +4.71 | -10.76 |
| 1.30 | `v1_pow_p2.0` |  -5.95 | +6.98 | +4.77 | -10.72 |
| 1.50 | `v0_log` |  -4.65 | +6.98 | +4.50 |  -9.15 |
| 1.50 | `v1_pow_p1.8` |  -4.25 | +6.98 | +4.70 |  -8.95 |
| 1.50 | `v1_pow_p2.0` |  -4.17 | +6.99 | +4.77 |  -8.94 |

Interpretation:

1. The null `Delta BIC` distribution is flat across `s in [0.7, 1.5]` to
   within ~0.05 BIC of its `s = 1` value, as Wilks predicts. The MC and
   the analytical expectation agree: null median ~ `+6.97`, p10 ~ `+4.5
   to +4.8` regardless of covariance scaling.
2. The actual-data `Delta BIC` scales close to the analytical
   `Delta chi2_observed / s + log(n)`. For `v0_log`: `-18.11 / s + 7.42`.
   This gives `-18.45` at `s = 0.7`, `-10.69` at `s = 1.0`, `-4.65` at
   `s = 1.5`, all matching the MC to within rounding.
3. The actual-data gap to the null p10 stays below `-8.9` BIC across the
   whole sweep `s in [0.7, 1.5]`. The diagnostic crosses the conventional
   "no meaningful support" line `Delta BIC = -2` only at `s ~ 1.85`, i.e.
   when the assumed covariance underestimates true noise variance by
   ~85%. A 30% under-reporting (`s = 1.3`) leaves `Delta BIC ~ -6`
   ("weak/moderate support" band).
4. v1 specs track v0 within ~0.7 BIC across the entire sweep. The shape
   robustness observed at `s = 1` survives uniform covariance rescaling.

Allowed claim:

> Under uniform covariance rescaling `s in [0.7, 1.5]`, the v0 and v1
> Pantheon+ same-sample `Delta BIC` results at `z_cut = 1.0` remain
> incompatible with the null distribution of the diagnostic. The
> "no meaningful support" line is crossed only at `s ~ 1.85`, i.e. when
> the assumed covariance underestimates true noise variance by ~85%.

Forbidden claim:

> This sweep removes the covariance caveat. A uniform `s` rescaling is a
> first-order sensitivity check, not a model of structured systematics
> (off-diagonal mis-specification, calibration drift correlated across
> redshift bins, photometric zero-point errors with z-dependence, host-
> galaxy mass-step systematics, etc.). Those structured failure modes can
> bias the result in ways no uniform rescaling can capture.

Discipline notes:

1. The sweep treats covariance scale as a single free parameter. A
   physically informed sensitivity check would decompose stat vs. sys and
   scale them separately, then propagate the uncertainty in the stat/sys
   decomposition itself.
2. A 30% under-reporting (`s = 1.3`) would correspond to a substantial
   error in Pantheon+'s systematics budget. There is no claim here that
   such an error exists; the sweep just shows that even if it did, the
   v0/v1 diagnostic would still strongly prefer a non-zero deformation.

Next technical improvement:

A stat/sys decomposition sweep using the separate Pantheon+
`STAT_only` and `SYS_only` covariance blocks (not currently downloaded
into `data/raw/pantheon_plus/`), allowing differential rescaling of the
two. This is a contract-amendment level of care; it should be
predeclared as v1.1 or v2 if undertaken.

## 2026-04-26: v1 Proof-Derived Deformation, Pre-Registered

Added:

```text
empirical/aoc_proof_derived_contract_v1.md
empirical/pantheon_plus/analyze_v1_proof_derived.py
data/derived/pantheon_plus/pantheon_v1_actual_fit.csv
data/derived/pantheon_plus/pantheon_v1_power.csv
data/derived/pantheon_plus/pantheon_v1_summary.json
reports/pantheon_plus/pantheon_v1_proof_derived.png
```

Motivation:

The v0 contract's strongest open caveat is specification flexibility:
`mu_AOC(z) = mu_LCDM + lambda * log(1 + z / 0.8)` was chosen after data
contact, so the look-elsewhere effect across deformation families is
unbounded. The v1 contract pins that down by deriving the deformation shape
from `docs/apparatus_bound_k_program.md` §5: the relative reconstruction
error grows as `sigma_P(y)/y = (sigma_0) * y^{p-1}`, so the proof-derived
distance-modulus deformation is

```text
delta_mu_AOC(z; lambda_K, p) = lambda_K * (1 + z)^{p - 1}.
```

The exponent `p` is committed to the apparatus-bound toy value `p_primary =
1.8` and a robustness alternate `p_robust = 2.0`. Both `p` values are
written into the contract before any v1 fit was run. The contract also
fixes the cutoffs (`z_cut_primary = 1.0`, `z_cut_secondary = 0.75`) and the
power-test injection grid.

Method:

The v1 deformation is plugged into the same machinery as the v0 power test:
covariance Cholesky once per `(spec, z_cut)` block, single solve per seed
for the noise vector, vectorized `chi2(lambda_K)` over the same grid
`[-0.30, 0.30]` step `0.01`. The v0 phenomenological log-threshold is
re-evaluated on the same `lambda_K` injection grid for direct
shape-comparison.

Actual-data fits at `z_cut = 1.0` (`n = 1676`):

| spec | best `lambda_K` | mag at `z = 1` | `Delta chi2` | `Delta BIC` |
| --- | ---: | ---: | ---: | ---: |
| `v0_log` (phenomenological) | -0.120 | -0.097 mag | -18.11 | -10.69 |
| `v1_pow_p1.8` (proof-derived) | -0.150 | -0.261 mag | -17.52 | -10.09 |
| `v1_pow_p2.0` (proof-derived robust) | -0.110 | -0.220 mag | -17.39 | -9.96 |

Actual-data fits at `z_cut = 0.75` (`n = 1653`):

| spec | best `lambda_K` | mag at `z = 1` | `Delta chi2` | `Delta BIC` |
| --- | ---: | ---: | ---: | ---: |
| `v0_log` | -0.130 | -0.105 mag | -17.51 | -10.10 |
| `v1_pow_p1.8` | -0.150 | -0.261 mag | -17.02 | -9.61 |
| `v1_pow_p2.0` | -0.120 | -0.240 mag | -16.88 | -9.47 |

Power summary at `z_cut = 1.0`, on a common magnitude-at-`z = 1` axis:

```text
v0_log:        50% detection at mag@z1 ~ -0.085 mag, 95% at ~ -0.115 mag
v1_pow_p1.8:   50% detection at mag@z1 ~ -0.18  mag, 95% at ~ -0.25  mag
v1_pow_p2.0:   50% detection at mag@z1 ~ -0.16  mag, 95% at ~ -0.21  mag
```

(`P(Delta BIC < -2)` evaluated against `lambda_K_inj` injected on top of
Pantheon+ covariance noise, 200 seeds.)

Null distribution under all three specs is centered at `Delta BIC ~ +7.0`
with p10 ~ `+4.6` and `P(Delta BIC < -2 | null) = 0` over 200 seeds, as in
the v0 power test entry above.

Interpretation:

1. `Delta BIC` is shape-robust within the apparatus-bound family. The three
   specs differ by less than `1` BIC unit on the actual data at
   `z_cut = 1.0` (range `-9.96` to `-10.69`). The exploratory v0 signal is
   not specific to the log-threshold form; the proof-derived power-law
   forms reach essentially the same evidence level.
2. The `v0_log` shape gives the highest detection power per unit
   magnitude-at-`z = 1`. This is because its derivative with respect to `z`
   is largest where Pantheon+ data is densest (`z ~ 0.1` to `0.5`); the
   proof-derived `(1 + z)^{p-1}` shapes have most of their curvature at
   higher `z`, where data is sparser. So the Pantheon+ data preference for
   `v0_log` over `v1_pow` is a sample-distribution effect, not a
   physical preference.
3. The three specs are correlated by construction: all three are smooth
   monotone deformations vanishing at `z = 0` after offset marginalization.
   Reaching similar `Delta BIC` is therefore not three independent
   confirmations of the same underlying signal; it is one detection
   reported under three correlated parameterizations. The relevant claim is
   only that the result does not collapse when the deformation is replaced
   by a proof-derived shape.
4. Both `v1_pow` `p` values fall on the same side of the null distribution
   as `v0_log` (`Delta BIC ~ -10`), well below the null floor at `+7`. The
   pre-registered v1 contract therefore confirms a non-null signal under
   the proof-derived deformation, conditional on the Pantheon+ covariance.

Allowed claim:

> Under the pre-registered v1 contract, a proof-derived AOC deformation of
> shape `(1 + z)^{p - 1}` with `p in {1.8, 2.0}` reaches `Delta BIC` between
> `-10.0` and `-10.1` on Pantheon+ at `z_cut = 1.0`, within `0.7` BIC of
> the v0 phenomenological result. The v0 same-sample preference is
> shape-robust within the apparatus-bound deformation family.

Forbidden claim:

> v1 confirms AOC, refutes `LambdaCDM`, or escapes the SRMF cautionary tale
> on flat-residue data. The pre-registered v1 result reduces but does not
> eliminate post-hoc effects, since `p` was chosen from the toy and the
> Pantheon+ data has been seen by the analyst.

Discipline notes:

1. The v0 power-test entry above contains a correction: the actual-data
   `Delta BIC` is `-10.69`, not `-16.11` (which is `Delta AIC`). The v1
   numbers in this entry use `Delta BIC` consistently.
2. v1 does not deprecate v0; both contracts coexist. Any future v2
   amendment must not silently drop v0 or change `p` in v1 without an
   explicit dated amendment.
3. The covariance-sensitivity sweep promised at the end of the v0 power-
   test entry is the next planned pass. v1 does not address it.

Next technical improvement:

Run the covariance-sensitivity sweep on both v0 and v1: scale the assumed
covariance by factors in `[0.7, 1.5]` and re-run the actual-data fit and
power test, to check how robust the `Delta BIC ~ -10` result is to
mis-specification of the Pantheon+ noise model.

## 2026-04-26: v0 Threshold-Deformation Power Test under Known lambda_inj

Added:

```text
empirical/pantheon_plus/power_test_v0.py
data/derived/pantheon_plus/pantheon_power_test_recovery.csv
data/derived/pantheon_plus/pantheon_power_test_power.csv
data/derived/pantheon_plus/pantheon_power_test_summary.json
reports/pantheon_plus/pantheon_power_test.png
```

Motivation:

The v0 same-sample exploratory result at `z_cut = 1.0` is
`best lambda = -0.12`, `Delta BIC = -16.11`. The split-robustness median is
`Delta BIC ~ -3.5`. Both numbers were uninterpretable on their own: we did
not know how the v0 diagnostic responds to noise, what the null distribution
of `Delta BIC` looks like under the Pantheon+ covariance, what `lambda` we
could detect, or how biased the recovered `lambda` is. This pass answers
those questions by injecting a known `lambda_inj` into a synthetic distance-
modulus vector built from the actual Pantheon+ redshift distribution and the
actual Pantheon+ covariance, then running the same v0 fit machinery.

Method:

1. Subset rows by `z <= z_cut` for `z_cut in [0.75, 1.0, 1.5]`.
2. Cholesky-factor `Cov[subset, subset] + 1e-9 I` once per `z_cut`.
3. For each seed, draw `iid ~ N(0, I_n)`, form `noise = L @ iid`, and the
   synthetic residual `r = lambda_inj * deformation + noise` where
   `deformation(z) = log(1 + z / z_star)`, `z_star = 0.8`.
4. Run the v0 fit: scan `lambda` over `[-0.30, 0.30]` in steps of `0.01` with
   constant magnitude offset marginalized via the precomputed Cholesky, find
   best `lambda_fit`, compute `Delta chi2` against the no-deformation case at
   `lambda = 0`, and `Delta BIC = Delta chi2 + log(n)`.
5. Aggregate over `n_seeds = 200` per `(z_cut, lambda_inj)` pair.

Recovery:

| `z_cut` | `lambda_inj` | median `lambda_fit` | p10-p90 `lambda_fit` | bias |
| ---: | ---: | ---: | ---: | ---: |
| 1.0 | 0.00 | 0.00 | -0.04 to +0.04 | 0.00 |
| 1.0 | -0.05 | -0.05 | -0.09 to -0.01 | 0.00 |
| 1.0 | -0.10 | -0.10 | -0.14 to -0.06 | 0.00 |
| 1.0 | -0.13 | -0.13 | -0.17 to -0.09 | 0.00 |
| 1.0 | -0.15 | -0.15 | -0.19 to -0.11 | 0.00 |
| 1.0 | -0.20 | -0.20 | -0.24 to -0.16 | 0.00 |
| 1.0 | -0.25 | -0.25 | -0.29 to -0.21 | 0.00 |

Recovery is unbiased at all tested `lambda_inj`. The p10-p90 spread of
roughly `+/- 0.04` corresponds to a Gaussian-equivalent recovery sigma of
`sigma_lambda ~ 0.03` at `z_cut = 1.0`.

Power and null:

| `z_cut` | `lambda_inj` | median `Delta BIC` | p10 `Delta BIC` | `P(Delta BIC < -2)` | `P(Delta BIC < -10)` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1.0 | 0.00 | +7.04 | +4.64 | 0.00 | 0.00 |
| 1.0 | -0.05 | +4.45 | -1.66 | 0.09 | 0.02 |
| 1.0 | -0.10 | -4.49 | -15.04 | 0.67 | 0.21 |
| 1.0 | -0.13 | -12.70 | -25.93 | 0.93 | 0.64 |
| 1.0 | -0.15 | -19.38 | -34.38 | 0.99 | 0.86 |
| 1.0 | -0.20 | -40.22 | -59.68 | 1.00 | 1.00 |
| 1.0 | -0.25 | -67.02 | -90.93 | 1.00 | 1.00 |

The other `z_cut` values track the same shape with slight shifts (see
`pantheon_power_test_power.csv`).

Interpretation:

1. The null distribution of the v0 diagnostic at `lambda_inj = 0` is centered
   at `Delta BIC ~ +7` with p10 `~ +4.6`. Over 200 seeds at `z_cut = 1.0`, no
   null draw produced `Delta BIC < -2`. This is a property of using BIC with
   `n ~ 1700`: the `+log(n) ~ +7.42` parameter penalty dominates the
   ~1-unit `chi2` improvement from a one-parameter best fit on noise.
2. The same-sample observed result `Delta BIC = -10.69` at `z_cut = 1.0`
   (`Delta chi2 = -18.11`, `Delta AIC = -16.11`) is ~15 BIC units below the
   null p10. Over 200 null seeds at `z_cut = 1.0`, no draw came within 15
   BIC units of the observed value, and the analytic chi-squared tail
   probability `P(chi2_1 > 18.11)` is ~`2e-5`. It is consistent in
   distribution with an injected `lambda_inj = -0.13` (median `Delta BIC` at
   that injection is `-12.70` with p10 `-25.93`, p90 `-3.10`, comfortably
   bracketing the observed `-10.69`).

   Note: an earlier draft of this entry conflated `Delta AIC = -16.11` with
   `Delta BIC`. The correct value is `Delta BIC = -10.69`. The qualitative
   conclusion (incompatible with null, consistent with `lambda_inj ~ -0.13`)
   stands; the magnitude of the gap to the null is smaller than the earlier
   draft implied. This is exactly the kind of bookkeeping mistake the v0
   discipline is supposed to catch on the way out.
3. The split-robustness median holdout `Delta BIC ~ -3.5` is also far below
   the null centroid (`+7`). It is roughly compatible with an effective
   injected `lambda` between `-0.05` and `-0.10`, where the median `Delta
   BIC` is `+4.45` and `-4.49` respectively in the full-sample power table;
   in halved holdout splits the shift is weaker.
4. Detection power at `Delta BIC < -2` reaches 50% near `lambda_inj ~ -0.09`
   to `-0.10` and saturates above 95% for `|lambda_inj| > 0.13` at
   `z_cut = 1.0`.

Allowed claim:

> Conditional on the Pantheon+ covariance being correct, the v0 threshold-
> deformation diagnostic recovers injected `lambda` unbiased with
> `sigma_lambda ~ 0.03` at `z_cut = 1.0`, has a null distribution centered
> at `Delta BIC ~ +7` with no draws below `-2` in 200 seeds, and reaches
> ~95% detection power at `Delta BIC < -2` for `|lambda_inj| >= 0.15`.
> The observed Pantheon+ same-sample `Delta BIC = -10.7` is incompatible
> with the diagnostic's null distribution under that covariance
> (analytic tail `P ~ 2e-5`), and is distributionally consistent with an
> injected `lambda_inj = -0.13`.

Forbidden claim:

> This validates AOC, refutes `LambdaCDM`, or proves that the observed
> Pantheon+ exploratory signal is real cosmology rather than systematics,
> calibration drift, sample selection, or specification flexibility from
> choosing the deformation form after data contact.

Discipline notes:

1. The covariance matrix is taken as given; this is a power test
   conditional on the Pantheon+ stated noise model. If the covariance
   underestimates real systematics, the null distribution shifts and the
   gap between the observed result and the null narrows.
2. The deformation form `log(1 + z / 0.8)` was chosen after Pantheon+
   exploration. This MC tests detection power for that form *as if* it had
   been pre-registered. The look-elsewhere effect across alternative
   deformation families is not bounded by this run.
3. None of this addresses the SRMF cautionary tale on flat-residue data:
   apparatus-bound `K` is not validated by any operation on Pantheon+ alone,
   regardless of how clean the diagnostic looks. This run only sharpens the
   internal status of the v0 contract.

Next technical improvement:

Repeat the power-test pipeline on a deformation derived from the AOC proof
spine rather than from data exploration, so that the look-elsewhere caveat
in note 2 above can be tightened. Alternatively, repeat the run on the
Pantheon+ holdout splits to confirm the split-robustness `Delta BIC` is
compatible with an effective injected `lambda` in the expected range.

## 2026-04-26: Two-Pipeline Apparatus-Bound K Simulation

Added:

```text
simulations/apparatus_bound_k/apparatus_k_two_pipeline.py
simulations/apparatus_bound_k/apparatus_k_two_pipeline_seeds.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_ratio.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_atlas.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_summary.json
simulations/apparatus_bound_k/apparatus_k_two_pipeline.png
```

Motivation:

The Pantheon+ branch reaches the limit of what flat residue data can say
about a pipeline-dependent quantity. `K_P` is, by construction, a property of
the reconstruction pipeline (`I, M, R, C` in
`docs/apparatus_bound_k_program.md`), not of the dataset alone. A test of the
formalism therefore has to be one in which the pipeline is fully specified by
the analyst: generate observations under a known noise law, run an explicit
reconstruction, measure `K` from the reconstruction, and check the §6 ratio
prediction against the closed form. That makes the agent ascribing label
authenticity explicit, which is the only setting in which the formalism is
honestly testable.

Method:

1. Forward model. FRW chart `a(t) = A t^alpha` with `A = 1`, `alpha = 0.5`,
   so `y(t) = 1/a(t) = t^{-1/2}`.
2. Two pipelines.

   ```text
   baseline: sigma_0 = 0.010, p = 1.8
   improved: sigma_0 = 0.003, p = 1.8
   ```

   Each pipeline samples `n_obs = 4000` log-uniform times in
   `[t_min, t_max] = [1e-4, 1e2]`, computes `y_true(t)`, and adds independent
   noise with `sigma_P(y) = sigma_0 * y^p`.
3. Empirical reconstruction. Bin residuals in `y` (30 log-spaced bins) and
   estimate `sigma_hat(y)` per bin. Find `K_emp` by log-log interpolation of
   the crossing `sigma_hat(y) = eta * y` with `eta = 0.10`.
4. Atlas coherence (§7). For each pipeline, run two independent reconstruction
   charts of `y(t)` from the same observations: a Gaussian kernel smoother in
   `log t` and a binned-median estimator in `log t`. Compute
   `Gamma(y) = |y_hat_1 - y_hat_2| / sqrt(se_1^2 + se_2^2)` on a shared
   evaluation grid and intersect the reliability and atlas conditions.
5. Monte Carlo. 60 seeds per pipeline.

Result:

| pipeline | `K_closed` | `K_emp` median | `K_emp` p10-p90 | `K_atlas` median |
| --- | ---: | ---: | ---: | ---: |
| baseline | 17.78 | 17.94 | 16.82-19.07 | 17.56 |
| improved | 80.09 | 80.72 | 72.94-89.72 | 78.80 |

Two-pipeline ratio (§6 prediction):

```text
theory K_improved / K_baseline = (sigma_0_baseline / sigma_0_improved)^(1/(p-1))
                               = (0.010 / 0.003)^(1/0.8)
                               = 4.504
median empirical K_improved / K_baseline = 4.499
p10 = 3.944, p90 = 5.051
n_seeds = 60
```

Interpretation:

The §6 two-pipeline ratio prediction is reproduced internally to within 0.1%
at the median over 60 seeds, with a roughly 10-15% spread from finite-sample
noise. The atlas-coherence cutoff is mildly tighter than the reliability
floor in both pipelines, as expected: a kernel and a binned-median estimator
of `y(t)` start to disagree relative to their internal uncertainty before the
reliability threshold alone is saturated. This separates a reliability floor
from a chart-fracture floor without requiring real cosmological data.

Allowed claim:

> The two-pipeline apparatus-bound mechanism reproduces the predicted
> `K_2 / K_1` ratio under explicit forward-model noise, and the §7
> atlas-coherence cutoff distinguishes a reliability floor from chart fracture
> in this controlled setting.

Forbidden claim:

> This simulation validates AOC against any real cosmological dataset, or
> proves apparatus-bound `K` as a property of nature.

Discipline note:

The structural reason this run is informative and the further Pantheon+
sharpening would not be: here we are the agent that ascribes label
authenticity, so the pipeline is fully auditable and the §6 ratio is a real
internal check. Running the v0 threshold deformation on a second public
dataset (DESI BAO, Union3, DES-SN5YR) would test curve-fit portability, not
the apparatus-bound mechanism, because in that setting the reconstruction
pipeline that produced the labels is opaque to the analyst.

Next technical improvement:

Implement a real two-real-pipeline contact: distance-ladder vs
inverse-distance-ladder, or Pantheon+ vs Cepheid-anchored or BAO-anchored
distances on overlapping redshift, so that the §6 ratio prediction can be
evaluated between two pipelines whose internal noise/inference are at least
partially auditable. Until then, contact with single flat residue datasets
should not be advertised as apparatus-bound `K` validation.

## 2026-04-26: Pantheon+ Split-Robustness Check

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_split_robustness.csv
reports/pantheon_plus/pantheon_aoc_split_robustness.png
```

Method:

Repeat the AOC threshold-deformation train/holdout procedure across 16 salted
`CID` splits. For each split and cutoff, select `lambda` on train and evaluate
on holdout. Summarize the holdout distribution.

Robustness summary:

| `z_cut` | median train `lambda` | median holdout `Delta chi2` | median holdout `Delta BIC` | frac `Delta BIC < 0` | frac `Delta BIC < -2` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.20 | -0.275 | -6.27 | -0.10 | 0.50 | 0.25 |
| 0.35 | -0.135 | -3.16 | 3.33 | 0.00 | 0.00 |
| 0.50 | -0.120 | -3.18 | 3.45 | 0.25 | 0.00 |
| 0.75 | -0.130 | -9.42 | -2.71 | 0.69 | 0.50 |
| 1.00 | -0.130 | -10.20 | -3.46 | 0.75 | 0.63 |
| 1.50 | -0.100 | -6.99 | -0.27 | 0.63 | 0.19 |
| 2.50 | -0.095 | -7.35 | -0.61 | 0.56 | 0.19 |

Interpretation:

The split-robustness check preserves the same broad intermediate-redshift
pattern, with the strongest median heldout BIC behavior at `z_cut=1.00`.
However, the split distribution is broad: some salted splits do not support the
deformation after BIC penalty. The result is therefore a useful empirical handle,
not evidence strong enough to claim support for AOC.

Allowed claim:

> The exploratory AOC-style threshold deformation is not solely an artifact of
> one object-level split; its strongest split-robust behavior remains near
> `z_cut=0.75-1.00`.

Forbidden claim:

> Split robustness confirms the deformation or validates AOC.

Next technical improvement:

Derive a deformation from the AOC proof spine or freeze the phenomenological
form before testing a separate public dataset.

## 2026-04-27: DESI DR2 BAO Selected as Next External Gate

Added:

```text
empirical/desi_dr2_bao/README.md
empirical/desi_dr2_bao/desi_dr2_bao_contract_v0.md
```

Decision:

DESI DR2 BAO is the next primary empirical target after Pantheon+. Pantheon+
is useful but degenerate with calibration, `M_B`, `H0`, and dark-energy-like
distance effects. DESI DR2 BAO tests expansion history with a different ruler,
using observables such as:

```text
D_M(z) / r_d
D_H(z) / r_d
D_V(z) / r_d
```

External source check:

1. DESI DR2 BAO papers were released in March 2025.
2. DESI DR2 cosmology chains and data products were released in October 2025.
3. DESI DR2 Results II supplementary data exists as an official Zenodo product,
   but the archive is large, so the first pass should find the smallest
   official BAO measurement table and covariance.

Program rule:

Do not tune on JWST/JADES first. JWST high-redshift galaxy maturity is
astrophysically messy and should be used later as a holdout or conceptual
payoff. Planck/CMB remains a guardrail before raw-likelihood work.

Allowed claim:

> DESI DR2 BAO is the correct next external gate for testing whether the
> Pantheon+-favored deformation direction survives a non-supernova ruler.

Forbidden claim:

> DESI confirms AOC, explains evolving dark energy, or solves the Hubble
> tension.

Next technical improvement:

Locate the smallest official DESI DR2 BAO measurement/covariance table, record
provenance and hashes, normalize it under `data/derived/desi_dr2_bao/`, then
compare flat `LambdaCDM`, frozen AOC v0/v1 shapes, and eventually `w0waCDM`
with equivalent parameter accounting.

## 2026-04-27: DESI DR2 BAO First-Pass Gate Executed

Added raw provenance and compact official likelihood inputs:

```text
data/raw/desi_dr2_bao/PROVENANCE.md
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt
```

Added executable gate:

```text
empirical/desi_dr2_bao/analyze_desi_dr2_bao.py
```

Generated:

```text
data/derived/desi_dr2_bao/desi_dr2_bao_all_gccomb_measurements.csv
data/derived/desi_dr2_bao/desi_dr2_bao_aoc_fit_grid.csv
data/derived/desi_dr2_bao/desi_dr2_bao_summary.json
reports/desi_dr2_bao/desi_dr2_bao_report.md
```

Data source:

The official DESI DR2 cosmology products page links the public BAO likelihoods
at `https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2`. The
first pass used the compact `desi_gaussian_bao_ALL_GCcomb_mean.txt` and
`desi_gaussian_bao_ALL_GCcomb_cov.txt` files rather than the 1.3 GB Zenodo
supplement.

Method:

1. Fit flat `LambdaCDM` BAO predictions with fixed `Omega_m=0.3`, `H0=70`, and
   `r_d=147.09 Mpc`.
2. Fit a global `alpha` nuisance scale for every model so the test is about
   redshift-dependent shape, not absolute `H0 * r_d` normalization.
3. Carry frozen Pantheon+ v0/v1 deformation shapes into DESI under two mappings:
   `derivative_dm` and `isotropic_scale`.
4. Report three subsets: all 13 points, galaxy-only/no-Ly-alpha, and
   `z <= 1` Pantheon-overlap.

Result:

DESI DR2 BAO prefers near-zero deformation for the carried-forward Pantheon+
v0/v1 shapes. On the full 13-point vector, best-fit `lambda_K` is approximately
`+0.002` to `+0.007`; on the `z <= 1` overlap subset, best-fit `lambda_K` is
only approximately `-0.005` to `-0.025`, much smaller than the Pantheon+
reference amplitudes (`-0.11` to `-0.15`). The Pantheon-amplitude deformation is
therefore not portable to DESI under this first projection.

Interpretation:

This is restrictive theory feedback. It does not refute AOC as a bounded-
observer framework, but it does reject the simple move "Pantheon+ deformation
amplitude carries directly into BAO distance observables" under the current
projection.

Allowed claim:

> DESI DR2 BAO now provides an auditable external constraint: the current
> Pantheon-amplitude deformation does not survive as a BAO shape under the
> first projection.

Forbidden claim:

> DESI confirms AOC, explains dark energy evolution, or solves the Hubble
> tension.

## 2026-04-27: AOC Assumption Audit Added

Added:

```text
docs/aoc_assumption_audit.md
```

Reason:

The first DESI DR2 BAO gate made clear that the zero-order question "does the
Pantheon+ deformation port directly to BAO?" is too strong and probably too
simple. It assumes shared observable structure, shared amplitude, shared
observer frame, and a simple distance-geometry map across probes.

Canonical correction:

> AOC is testable only through boundary behavior, not through direct inspection
> of what its own model places beyond the observer horizon.

The audit frames AOC evidence as second-order boundary evidence:

```text
pipeline-dependent reconstruction floors
stable inter-probe mismatch patterns
atlas-coherent boundary behavior
horizon-adjacent compression
control-resistant residuals
```

It also records the "cosmological Gabriel's horn" as a hypothesis-generator
model class, not a claim. The model class is useful only after specifying a
larger process space, observer quotient, reconstruction order, and at least one
second-order observable consequence.

## 2026-04-27: Observable Map Program Added

Added:

```text
docs/aoc_observable_map_program.md
```

Reason:

The DESI first pass rejected the direct portability assumption:

```text
Pantheon+ distance deformation -> same BAO distance deformation
```

This does not reject AOC, but it does reject using one fitted deformation as a
universal cross-probe map without derivation.

Program rule:

> AOC does not get a universal deformation for free; each observable must earn
> its own map from the reconstruction horizon to measured quantities.

The document now defines probe-specific map questions for Pantheon+, DESI BAO,
Planck/CMB, JWST/JADES, Hubble-tension work, and Fermi/instrument-forward
calibration. It also adds a pre-fit checklist requiring an exact observable,
pipeline, AOC map, frozen parameters, nuisance structure, baseline, failure
mode, allowed claim, and forbidden claim before any new empirical fit.

Recommended next order:

```text
observable map -> baseline upgrade -> frozen rerun -> only then new data
```

## 2026-04-27: DESI Baseline Upgrade Executed

Updated:

```text
empirical/desi_dr2_bao/analyze_desi_dr2_bao.py
reports/desi_dr2_bao/desi_dr2_bao_report.md
data/derived/desi_dr2_bao/desi_dr2_bao_summary.json
data/derived/desi_dr2_bao/desi_dr2_bao_omega_lambda_profile.csv
```

Method change:

The DESI gate now fits a global BAO `alpha` nuisance and grids over
`Omega_m = 0.15 ... 0.45` for both the flat `LambdaCDM` baseline and the frozen
AOC maps. This tests whether the earlier near-zero result was an artifact of
fixing `Omega_m=0.3`.

Baseline results:

| Subset | Best `Omega_m` | Baseline chi2 |
| --- | ---: | ---: |
| all | 0.297 | 10.274 |
| galaxy_no_lya | 0.299 | 10.176 |
| pantheon_overlap_z_le_1 | 0.310 | 8.517 |

Result:

The baseline-upgraded DESI gate still does not support the Pantheon+
deformation direction.

1. The `isotropic_scale` sensitivity map prefers near-zero deformation across
   subsets.
2. The `derivative_dm` map can improve chi2 in the galaxy/no-Ly-alpha and
   `z <= 1` subsets, but only by flipping sign relative to the Pantheon+
   deformation and often pushing `Omega_m` toward the upper grid edge.
3. The derivative-map improvements do not reach BIC-level support
   (`Delta BIC` remains above `-2` in the reported subsets).
4. Pantheon-reference amplitudes are disfavored relative to the upgraded LCDM
   baseline.

Interpretation:

This strengthens the earlier conclusion: the simple observable map from
Pantheon+ distance deformation to DESI BAO is not portable. AOC now needs a
native BAO observable map, a null-BAO position, or a decision to treat the
Pantheon+ pattern as supernova/pipeline-specific.

Allowed claim:

> After `Omega_m` baseline freedom, DESI DR2 BAO still does not support the
> Pantheon+ deformation direction under the current observable maps.

Forbidden claim:

> The derivative-map chi2 improvement confirms AOC.
