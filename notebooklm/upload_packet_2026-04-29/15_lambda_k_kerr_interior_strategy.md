# λ_K Kerr-Interior Strategy (Seed)

**Phase: near-cousin / gesture, NOT derivation, NOT instantiation.**

Status: seed document. Engagement target for Paul between Episode 3 release
and Episode 4 work-start. The Kerr-interior name is an external nomination
(NotebookLM Strategic Program Proposal output, 2026-04-28); committing it as
the territory is exactly the failure mode `AGENTS.md` flags.

Purpose:

To name the strategic next near-cousin geometry for `λ_K` — the
apparent-origin / reconstruction-deformation parameter that would distinguish
AOC from naive standard-cosmology analysis — and to list the open derivation
milestones as questions, not claims. The bridge from instantiation back to
gesture is what `docs/principia_symbolica_conjecture_state.md` calls out as
*missing on the theory side* (`§ What is missing`); this doc opens that work
without prosecuting it.

What this doc is **NOT**:

1. A derivation of `λ_K`. No numbers appear.
2. A claim about `λ_K`'s value, sign, or order of magnitude.
3. An instantiation-grade commitment to Kerr-interior cosmology as the
   territory. It is a candidate near-cousin geometry, one of several listed
   in the conjecture-state document.
4. A replacement for the apparatus-bound K program. Apparatus-bound K_P is
   instantiation-grade for what it covers; the Kerr-interior question is
   whether a *theory-side* number can be derived to complement it.

## 1. Why Kerr-interior is the strategic near-cousin

The Kerr-interior geometry is named explicitly in
`docs/principia_symbolica_conjecture_state.md § Near-cousins` as a
mathematically tractable physics frame whose structure intersects the AOC
gesture: rotating BH interior, effective FRW projection visible to an interior
observer, axial structure, multiple horizons, sustainable null-geodesic
constraints. It is the simplest non-trivial geometry where an observer-bounded
reconstruction has both a *generative boundary* (ring singularity / inner
horizon region) and a *dissipative boundary* (event horizon) — which is the
two-horizon shape named in `docs/glossary.md § Dual-Horizon Cosmogenesis` and
the reconstruction/escape pair named in `§ Escape Horizon`. <!-- near-cousin
reminder: structural intersection, not identity -->

Confidence on Kerr-interior structural similarity to AOC's gesture:
**~60%** on first pass. The ingredient list (axial, two horizons, sustainable
orbits, interior FRW projection) matches more of the gesture's working
features than any other named near-cousin in the conjecture-state document.
The 40% reservation is because (a) the gesture's *bounded observer* is not
yet pinned to "interior observer of a rotating compact object," (b) Kerr is
vacuum and AOC's apparent-origin surface is reconstruction-frame, not
geometric, and (c) Pathria-Good and Haggard-Rovelli also carry partial
ingredients; promoting Kerr alone would silently re-collapse the gesture
onto one cousin. Strategic, not committed.

## 2. The λ_K target

`λ_K` names a number Episode 4 wants Episode 5+ to land: a closed-form or
numerical map from Kerr-interior observer-quotient parameters (Kerr spin
parameter `a`, mass `M`, observer trajectory class) to an observable
cosmological deformation amplitude that connects to the apparatus-bound K
program in `docs/apparatus_bound_k_program.md`. The shape is:

```text
λ_K = λ_K(a, M, observer_class; pipeline) → observable deformation amplitude
```

Operationally, the open question is whether `λ_K` can be defined so that it
plugs into one of three live empirical handles:

1. **Distance-modulus deformation.** The Pantheon+ K_P contract
   (`empirical/aoc_threshold_contract_v0.md`) already runs
   `δμ_AOC(z; λ_K, p) = λ_K · (1+z)^{p-1}` as an exploratory map; on
   `z ≤ 1` overlap the best-fit lives at `λ_K ≈ +0.002` to `+0.007` (science
   log entries 2026-XX). The number Episode 4 wants is one *predicted* from
   theory, not fit from data — a different epistemic object.
2. **BAO observable map.** The DESI DR2 gate rejected naive shared-distance
   portability of v0 (`docs/empirical_burden_table.md § Second-Order Evidence
   Rule`); a Kerr-interior derivation would have to predict an
   observable-specific BAO map, not import the SN map.
3. **CMB-side residual structure.** The Planck operator-residue Episode 2
   work (`empirical/planck_operator_residue/`, glossary
   `§ Pipeline Independence Postulate`) flagged parallel-fifths block-motion
   at ell=3 under masking transitions. Whether `λ_K` derived from interior
   dynamics predicts that signature — or is orthogonal to it — is itself an
   open question (see § 5).

The criterion for Episode 4 success is *not* that `λ_K` is large or
detectable. It is that `λ_K` is a derived number, with a stated derivation
chain, that distinguishes AOC from ΛCDM in at least one of these handles
even at order of magnitude.

## 3. Existing scaffolding

| doc | provides | phase |
|---|---|---|
| `docs/k_parameter_theory.md` | apparatus-bound / RG-effective / fundamental K framings; recommends apparatus-bound first | near-cousin (theory) |
| `docs/apparatus_bound_k_program.md` | concrete K_P from pipeline reliability and atlas coherence | instantiation (for K_P specifically) |
| `docs/cacophony_to_k_bridge.md` | calibrated-oracle methodology import; routing-not-staging discipline | near-cousin (methodology, not physics) |
| `docs/iteration_operator_bridge.md` | AGI-26 audible-operator notebook → K parameterization; explicit-operator lemma | near-cousin |
| `docs/frw_observer_quotient_chart.md` | first concrete FRW observer-quotient chart; `Ω_O = a(t)^2`; t_K = (AK)^(-1/α) | instantiation (chart only) |
| `docs/principia_symbolica_conjecture_state.md` | gesture-state of the conjecture; lists Kerr-interior as one named near-cousin | gesture |
| `docs/apparent_origin_canonical_proof.md` | proof spine; observer-quotient lemma, Rayleigh access dual, adapted-filtration cohomology | publication-grade for what it covers |
| `docs/empirical_burden_table.md` | what every empirical claim must pay; flags DESI BAO portability gap | standing checklist |
| `docs/forbidden_simplifications.md` | guardrail; what AOC explicitly does not claim | standing |

Note: none of these scaffolding pieces commits a number for `λ_K`. That is
the gap Episode 4 work would address. <!-- near-cousin reminder: gap, not
absence-of-content -->

## 4. Open derivation milestones (questions, not claims)

Each is a chip-able milestone, falsifiable-when-answered:

1. **Does the Kerr-interior observer-quotient produce an apparent-origin
   surface from a finite-K reconstruction, or does it require additional
   structure beyond the FRW chart logic?** Concretely: does the construction
   in `docs/frw_observer_quotient_chart.md` (where `Ω_O(t) = a(t)^2` yields
   `t_K = (AK)^(-1/α)`) lift to a Kerr-interior chart, or does the axial
   structure force a different access functor `Ω_O(a, M, r, θ, ...)` whose
   vanishing locus is not a simple time slice? If lift fails, the
   near-cousin contributes ingredients but not a direct derivation.

2. **What is the simplest closed-form map from (a, M, observer-class) to a
   single number `λ_K` that distinguishes AOC from ΛCDM in at least one
   handle?** First-pass acceptance: an order-of-magnitude bound, not a
   precision prediction. The map must say *which observable channel* it
   addresses; "general deformation" is a forbidden simplification.

3. **Does the Kerr-interior near-cousin geometry predict the
   parallel-fifths-at-ell=3 block-motion finding (Episode 2 voice-leading
   analysis, glossary `§ Pipeline Independence Postulate`), or is that
   finding orthogonal to interior dynamics?** Both answers are valuable.
   "Orthogonal" sharpens the empirical separation between Kerr-derived `λ_K`
   and the operator-residue handle; "predicts" is a bridge that would have
   to specify *how* interior axial structure leaks into low-ell CMB
   reconstruction-frame distortion. Either result reduces the search space.

4. **How does the Cacophony staging discipline
   (`docs/cacophony_to_k_bridge.md`: calibrated oracle, distinguishability
   threshold, atlas-coherence control, routing-not-always-staging) constrain
   which Kerr-interior parameters are observer-bindable into an
   apparatus-bound K_P?** The methodology import is a discipline, not a
   physics claim. The open question is whether the discipline cuts down the
   parameter space enough that a Kerr-interior-derived `λ_K` becomes
   uniquely calibrated by one live pipeline, or whether the binding
   under-determines the answer.

5. **What is the minimal first-pass derivation that lands a number — even
   an order-of-magnitude bound — for `λ_K` from apparatus-bound K of one
   live pipeline (Pantheon+ SN, DESI BAO, or Planck PR3)?** This is the
   "break the circle" milestone from `principia_symbolica_conjecture_state.md
   § What is missing`. The criterion is: a derivation chain that does not
   pass through fitting `λ_K` to data the deformation is then evaluated
   against (the SRMF cautionary tale lives in user auto-memory; a
   Kerr-interior-derived `λ_K` evaluated on the *same* Pantheon+ data the
   v0 contract was fit against would be a different version of that same
   error).

These five are the spine. The list may shorten, not lengthen, before
Episode 4 work-start. <!-- near-cousin reminder: each question is open;
none asserts that Kerr is the right cousin -->

## 5. What this doc is NOT (closing)

To preserve phase across future engagement:

1. This is **not a derivation**. No numbers for `λ_K` appear here. None
   should be added without an explicit phase transition documented at the
   top of this file.
2. This is **not an endorsement of Kerr-interior cosmology as the
   territory**. It is a near-cousin partial map, with confidence ~60% on
   structural similarity to the gesture. Pathria-Good, Haggard-Rovelli /
   Rovelli-Vidotto, Smolin CNS, and Poplawski Einstein-Cartan torsion are
   alternative cousins listed in the conjecture-state document and are not
   ruled out by selecting Kerr for Episode 4 attention.
3. The phase tag is **maintained throughout**. If a future revision starts
   to drift toward instantiation framing — committing a number, dropping
   the "near-cousin" qualifier on Kerr, or treating Kerr-interior dynamics
   as the source of `λ_K` rather than a candidate source — that revision
   must explicitly transition phase with a documented commitment in the
   header.
4. This is **not a procedure**. It is a seed for engagement, not a
   workflow. Per `AGENTS.md § Stage discipline`: harnesses enable
   continuity but should not grow past their use.

Drift-naming reminder for any agent extending this doc: if you reach for
"Kerr cosmology predicts" in place of "the Kerr-interior near-cousin would
need to be shown to predict," name the substitution out loud and revert.
The fluency cost is the right trade.
