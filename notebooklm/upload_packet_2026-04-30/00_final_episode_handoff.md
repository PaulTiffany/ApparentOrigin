# Final Episode Handoff: TTCS Contract, Live PASS, And A Frozen Open Question

Status: source-grounded handoff for NotebookLM (or similar tool) to draft an
"Episode 4" following `upload_packet_2026-04-29/00_next_episode_handoff.md`
(frozen-prediction-contract pay-off + Sprint D voice-leading sim-null +
Sprint C-prime duets + λ_K Kerr-interior strategy seed).

This is the final episode for now. Episode 3 ended on a hand-off: the λ_K
Kerr-interior seed doc opened five chip-able milestones and explicitly
deferred Sprint E (prismatic decomposition rigor) to Episode 4. Episode 4
takes those open questions and lands a TTCS candidate map plus a live
empirical contract.

The Episode 4 arc is shaped differently from Episode 3. Episode 3 was the
*pay-off* of predictions written before the data was inspected. Episode 4
is the *theory-side discipline* of carrying a near-cousin geometry into a
predeclared empirical contract without confusing feasibility for
observation, plus a methodology note about how a CI-side LLM agent
brokered the live run on Linux compute that the local Windows machine
could not run. Episode 4 closes with one frozen open question that names
exactly what the next confirmatory artifact must be.

## Episode arc

1. **Where Episode 3 left off.** The λ_K Kerr-interior strategy seed
   (`05_lambda_k_kerr_interior_strategy.md`) was 60% confidence on
   structural similarity to AOC's gesture, with five chip-able open
   milestones and an explicit phase tag of "near-cousin / gesture, NOT
   derivation, NOT instantiation." Sprint E (prismatic decomposition
   rigor) was deferred to Episode 4 by user decision. Episode 4
   engages both lanes.

2. **Sprint E -- Prismatic Decomposition Rigor.** The robustness
   grammar that any operator-residue feature must survive before being
   carried into stronger empirical or theory-side claims
   (`08_prismatic_decomposition_rigor.md`). Three prisms: *multipole*
   (single-ell vs band vs leakage), *mask / sky-partition* (synthetic
   vs official Planck mask family), *operator* (Commander / NILC /
   SEVEM / SMICA, plus pair-residue, plus per-operator cross-octave).
   Feature-state vocabulary is *routing labels, not honorifics*:
   `survives a prism`, `collapses under a prism`, `recomposes`,
   `operator-bound`, `mask-bound`, `shared-target residue candidate`,
   `theory-contact candidate`. Episode 3 features re-labeled under
   the grammar:

   - P1/P2/P3 Q-O cliff -> *mask-sensitive Q-O recomposition feature*.
   - Sprint D parallel-fifths lockstep -> *ell=3 operator-lockstep
     feature under masked transition*.
   - Sprint C-prime duets -> *composition-layer inspection of
     per-operator Q-O detuning*.

   Sprint E is methodology-class. It does not promote any feature to
   AOC evidence; it specifies what would have to survive before that
   promotion would even be admissible.

3. **λ_K Observable-Feasibility First Pass.** The first theory-side
   step after the Kerr-interior seed
   (`09_lambda_k_observable_feasibility_first_pass.md`). The load-bearing
   correction is a type guard:

   ```text
   feasible (allowed by near-cousin geometry)
     -> observable (survives a specified apparatus/pipeline band)
       -> observed (estimated in a dataset)
   ```

   The forbidden shortcut is `feasible -> observed`. Within that
   discipline the Episode 4 derivation lands a Kerr horizon kernel:

   ```tex
   h_K(\chi) = \frac{1 - \sqrt{1 - \chi^2}}{1 + \sqrt{1 - \chi^2}}
   ```

   and an admissible scale `Lambda_K^adm(chi, K_P) = h_K(chi) / K_P`.
   This is observable-feasibility *structure*, not an observed
   amplitude. No number for λ_K is narrated.

4. **λ_K SRMF Invariant Card.** Six-invariant guardrail
   (`10_lambda_k_srmf_invariant_card.md`) that names the failure modes
   the bounded-observer primitive predicts will appear: black-box
   judgment, observed/observable type mismatch, cross-probe portability,
   unbounded-observer leak, story-first confirmation, endless method
   refinement, hidden channel fitting, zero-order violation. The card
   places the program at TTIE -> TTCS in the SRMF cycle: the typed
   surface is integrated; the next move is to propose a constrained
   candidate map.

5. **λ_K Planck Operator-Prism Contract -- the TTCS candidate.**
   `11_lambda_k_planck_operator_prism_contract.md`. Picks the operator
   prism, defines a judge-free scalar coordinate, freezes the
   prediction *before* the data run:

   ```tex
   C_axis(\ell, m) = \frac{D_{res}(\ell, m) - D_{op}(\ell, m)}{D_{iso}}
   ```

   where `D_op` is the median pairwise axial dispersion among the four
   operator axes and `D_res` is the median pairwise axial dispersion
   among the six pair-residue axes. The predeclared sign condition is

   ```text
   C_axis(ell=3, official-mask-base) > 0
   AND C_axis(ell=3, official-mask-dilate1) > 0.
   ```

   Sign-only. Deliberately weaker than predicting a direction or
   amplitude. The contract document was committed at 2026-04-29 23:14;
   the gate code at 23:28. Both predate the live run.

6. **Live result -- contract PASS.** GitHub Actions, 2026-04-30
   (`12_operator_prism_contract_gate_report.md` plus the science-log
   entry). Linux runner, `healpy.map2alm`, official Planck PR3 common
   mask:

   ```text
   C_axis(ell=3, official-mask-base)    = 0.281497
   C_axis(ell=3, official-mask-dilate1) = 0.425643
   live_verdict = contract_success_if_inputs_were_predeclared
   ```

   The conditional `if_inputs_were_predeclared` clause stays in the
   verdict string. The contract sign condition was satisfied for both
   mask states. This is the first time AOC has run a true
   frozen-prediction-then-checked sequence on a low-ell coordinate
   end-to-end in the right timestamp order.

7. **Sprint F1 -- D_iso Calibration.** First-principles audit
   (`13_d_iso_calibration_report.md`) of the gate's hardcoded
   normalization. For two uniform unit vectors on `S^2`, the axial
   angle `theta = arccos(|u . v|)` has CDF `1 - cos(theta)`, so the
   median is exactly `pi/3 = 60 deg`. Monte Carlo (n_realizations =
   100,000) places the n=4 reference at **60.03 deg**, not 57 deg.
   The hardcoded 57 deg sits within the bulk of the distribution
   (between p25=52.6 and p75=67.6) but is ~3 deg below the empirical
   median, well outside Monte Carlo noise. The live sign verdict is
   invariant to this correction; under D_iso=60 the magnitudes become
   0.267 and 0.404 (still positive). The hardcoded value is *not
   retroactively modified* in the gate code, because the contract was
   frozen at that value before the run -- moving the goalpost after
   seeing the data is the predeclaration failure mode. Future
   contracts should cite this calibration and use 60 deg.

8. **Sprint F2 -- C_axis Null Baseline.** Local-machine null
   (`14_operator_prism_c_axis_null_report.md`) using the Sprint D
   surrogate-pipeline scaffolding: isotropic LambdaCDM low-ell sky,
   four surrogate operators with independent operator noise,
   compute `C_axis` per realization. Two conditions: unmasked and
   synthetic galcut20.

   The methodologically substantive finding from this null is that
   *under the surrogate Pipeline-Independence-Postulate cartoon*,
   `C_axis` is broadly positive with median around 0.6-0.7, because
   pair-residues in a "shared sky plus small operator noise" model
   reduce to (noise_i - noise_j) and their axes are nearly uniform
   random (D_res near 60 deg), while operator axes track the shared
   sky (D_op small). So `C_axis > 0` is **trivially satisfied** by any
   shared-sky-plus-small-noise model -- it is not a Kerr-specific
   prediction.

   The live observed values (0.281, 0.426) sit *below* the surrogate
   null bulk. That is informative in the opposite direction: the real
   Planck pair-residues are *more aligned* than the surrogate cartoon
   predicts. The four real Planck pipelines' pair-residues do not
   look like uniform-random axes; they have shared structure not
   captured by the surrogate.

   This is a baseline, not the proper test. The proper null requires
   isotropic LambdaCDM through the *official* Planck common mask with
   the same `healpy.map2alm` extractor used in the live run. Sprint F2
   documents this as the **frozen open question** that closes Episode 4.

9. **Sprint F3 -- CI LLM Compute Leverage.**
   `15_ci_llm_compute_leverage.md`. Names the methodology pattern by
   which the live operator-prism contract ran on GitHub-hosted Linux
   compute despite the local Windows environment having no working
   `healpy`. A CI-side LLM agent (GPT working through OpenAI Codex)
   staged a private GitHub repository plus workflow YAML. The local
   repo remained the canonical scientific state; the workflow
   artifact pulled back into the local repo. Predeclaration discipline
   ran forward: the contract was frozen in the local repo before the
   workflow ran. Large data inputs (7.45 GB of Planck PR3 FITS) were
   treated as fetched data, not Git-tracked source. The pattern is a
   tool choice, not a delegation of authorship.

10. **The frozen open question.** Episode 4 closes by naming exactly
    what the next confirmatory artifact must be. The proper null for
    the operator-prism contract requires another GitHub Actions run,
    this time with isotropic LambdaCDM low-ell skies pushed through
    the same official Planck common mask used in the live run, with
    the same `healpy.map2alm` extractor. Until that run lands, the
    Episode 4 result reads as: *first frozen-then-checked operator-prism
    contract, sign condition satisfied, baseline null shows the contract
    is methodologically substantive, proper null deferred*.

## Phase tags

| artifact | phase |
| --- | --- |
| Sprint E prismatic decomposition rigor | methodology / epistemological |
| λ_K observable-feasibility first pass | near-cousin / feasibility derivation |
| λ_K SRMF invariant card | near-cousin / theory discipline |
| λ_K Planck operator-prism contract | TTCS candidate map |
| operator-prism gate live report | TTCS contract live result, conditional verdict |
| Sprint F1 D_iso calibration | methodology / first-principles audit |
| Sprint F2 C_axis null baseline | instantiation-class baseline |
| Sprint F3 CI LLM compute leverage | methodology / harness pattern |

No artifact in this packet is publication-class. The closest is the
operator-prism gate live report, which carries `if_inputs_were_predeclared`
in its verdict string by design.

## What this episode does and does not establish

**Establishes:**

1. AOC has run a frozen-prediction-then-checked operator-prism contract
   end-to-end. The sign condition is satisfied.
2. Sprint E gives a robustness grammar that any future operator-residue
   feature must survive.
3. λ_K has a closed-form observable-feasibility kernel (Kerr horizon
   ratio) under explicit type discipline.
4. The CI-LLM-as-compute-broker pattern is a reusable methodology when
   the local environment cannot run a required library.

**Does not establish:**

1. AOC has been confirmed.
2. ΛCDM has been refuted.
3. Pipeline Independence Postulate has been refuted.
4. Kerr-interior is the territory.
5. λ_K has a derived numerical value.
6. The live operator-prism PASS is rare under the proper null
   (proper null deferred -- frozen open question).

## Reading order

1. `01_README.md`, `02_forbidden_simplifications.md`, `03_AGENTS.md`,
   `04_glossary.md` -- standing repository discipline.
2. `05_lambda_k_kerr_interior_strategy.md` -- Episode 3 -> 4
   hand-off seed.
3. `06_voice_leading_sim_null_report.md`,
   `07_p1_prediction_evaluation.md` -- Episode 3 anchor cluster.
4. `08_prismatic_decomposition_rigor.md` -- Sprint E grammar.
5. `09_lambda_k_observable_feasibility_first_pass.md`,
   `10_lambda_k_srmf_invariant_card.md`,
   `11_lambda_k_planck_operator_prism_contract.md` -- the λ_K theory
   stack.
6. `12_operator_prism_contract_gate_report.md` -- live PASS.
7. `13_d_iso_calibration_report.md`,
   `14_operator_prism_c_axis_null_report.md` -- Sprint F1 + F2 audit
   and baseline null.
8. `15_ci_llm_compute_leverage.md` -- methodology note on the CI run.
9. `16_science_log.md` -- full log through release date.

The Episode 3 anchor cluster (items 2-3 above) is intentionally thin.
Listeners who came in via Episode 3 already have the Sprint D / λ_K
seed context; this packet does not re-derive Episode 3.

## Hand-off after Episode 4

This is the final episode for now. The repository's open work after the
packet ships:

1. The frozen open question in Sprint F2 -- run the proper official-mask
   `C_axis` null on GitHub Actions and produce a percentile readout for
   the live values.
2. Per the operator-prism contract section 7, future contracts should
   cite the Sprint F1 calibration and use D_iso = 60 deg.
3. The four remaining Episode 3 chip-able λ_K milestones (the seed
   doc's questions) are still open. Episode 4 only closed the first
   ("does the FRW chart lift?") with the answer "not directly; a
   horizon-normal interior chart exists."

Slogan to preserve verbatim:

> Boundary of reconstruction, not beginning of being.
