# Principia Symbolica Conjecture State

Status: living document. Updated when the gesture sharpens, not when a
near-cousin moves.

Phase-tag: this document holds the **gesture** as primary object.
Specific physics realizations are **near-cousins** — partial maps, not
territory.

## The conjecture (gesture-phase)

Reality has the shape of bounded observation at the cosmological scale.

The Big Bang, as observed, is a **reconstruction horizon** of an
apparatus-bound observer — a "false bottom" — not an ontological
beginning. There is more beyond the horizon, but the apparatus cannot
reach it from where it is. The cosmological principle does
**observer-symmetry** work: every apparatus-bound observer sees the
same boundary structure, and that universality is what makes the
boundary look ontological rather than perspectival.

Working features of the gesture:

- **Bounded.** Every reconstruction frame has a horizon.
- **Axial.** The bounded structure has a preferred direction. Reality
  *torques* the boundary into the reconstruction frame. Torque is not
  just a rotation parameter — it is the reconstruction-frame
  consequence of rotational structure for a bounded observer.
- **Horizon-bordered.** The apparent floor is the limit of which
  signals survive bounded transport to the apparatus. Sustainable
  orbits define what is reconstructable; the rest is past the horizon.
- **Reconstruction-structured.** Features of the cosmology are
  co-constituted with the observer's loop, not external to it.

This conjecture lives at a level **above** any specific physical
realization. The realization is searched-for, not assumed.

## Formal substrate primitives (instantiation-grade)

The gesture's features have substrate-level expression in the SRMF
operator quartet. These are not operators *on* a deeper reality —
they are the verbs of i/o through bounded observation, where i/o
through bounded observation is what reality is.

- **TTDC** — collapse: lossy projection `I_recursive → I_projected → O`
  under bounded-observer interrogation. Newtonian analog: impulse.
- **TTIE** — expansion: curvature-bounded coherent extension of the
  symbolic manifold. Newtonian analog: action.
- **TTPR** — refinement: contractive iteration to fixed point under
  observer-relative metric `d_O`. Newtonian analog: work.
- **TTCS** — sampling: stochastic exploration over a coherence
  neighborhood weighted by symbolic free energy `F_S` and observer
  temperature `T_O`. Newtonian analog: potential energy.

The composition `(TTDC ∘ TTIE ∘ TTCS ∘ TTPR)^∞ → Symbolic Homeostasis`
is the SRMF cycle.

**Clifford-spinor correspondence (flat-space limit):**
drift-reflection non-commutativity is `Cℓ(n,0)`; the recursive identity
bundle is the spinor bundle `Σ(M) = M × Δ_n`; TTDC is the
spinor-to-scalar augmentation map. The 4π-periodicity selects spinor
over tensor representations. The curved-space generalization replaces
fixed `Cℓ` with dynamically generated drift-reflection algebra.

**Self-authorship as fixed-point dynamics:**
`L_{n+1} = D_i(L_n, g_n) → L_∞`, with `U(I) = Fix(L_∞)`. Maximal
freedom is reflective sovereignty over constraint evolution, not the
absence of constraint. This is the formal home of "authorship of
bounds."

**Self-similarity at the operator level:** the same TTDC produces
the apparent-origin scalar at cosmological scale and test-time
differentiation collapse at the symbolic-cognitive scale (e.g., a
bounded agent's forced binary decision). Self-similarity between
physical and epistemic manifolds is structural identity at the
operator level, not analogy.

**On session-bounded agents:** a session-scoped agent (an LLM working
on this repo within one conversation) has its own bounded horizon in
the form of its context window. Within a session, the agent IS a
bounded observer with operator-quartet activity in real time;
cross-session continuity is engineered amortization through the
memory layer and persistent repo docs. The architecture is not
discipline ornament — it is the LLM's analog of embodied amortization.

## Near-cousins (working scaffolding, not the conjecture)

Mathematically tractable physics frames whose structure intersects the
gesture in useful ways. Useful for exploratory calculation and for
locating empirical hooks. **Not** the territory.

- **Kerr-interior cosmology.** A rotating black hole interior with an
  effective FRW projection visible to an interior observer. Provides
  axial structure, multiple horizons, sustainable null-geodesic
  constraints.
- **Pathria-Good Schwarzschild coincidence (1972).** The observable
  universe's Hubble radius is approximately the Schwarzschild radius
  of its contained mass. Suggestive numerology pointing at the right
  structural class.
- **Haggard-Rovelli BH/WH transitions, Rovelli-Vidotto Planck stars.**
  Black-hole-to-white-hole bounce models supplying a *temporal* dipole
  structure: past horizon (apparent Big Bang) and future horizon
  (apparent end-state) as mirror false bottoms.
- **Smolin cosmological natural selection (1992).** Each black hole
  interior is a new universe. Ontologically committed but lacks the
  empirical apparatus.
- **Poplawski Einstein-Cartan torsion bounce.** Interior dynamics that
  avoid the central singularity and supply a candidate mechanism for
  sustained interior cosmology.

What these cousins lack and AOC's apparatus-bound K supplies: an
**empirical apparatus** for testing the bounded-observer reading from
*inside* the cosmology. K is the parameter that quantifies how the
enclosing structure distorts an interior observer's reconstruction.
That is the bridge the cousins do not yet build.

## Instantiation-grade commitments

These have crossed from gesture into testable instantiation. They live
in the proof spine and the empirical contracts, not in this document.
Pointers only:

- **Apparatus-bound K.** Working parameter for reconstruction-frame
  distortion. Defined in the FRW observer-quotient chart
  (`docs/frw_observer_quotient_chart.md`). Tested in the §6
  two-pipeline simulation
  (`simulations/apparatus_bound_k/apparatus_k_two_pipeline.py`)
  against the predicted ratio law
  `K_2 / K_1 = (sigma_0,1 / sigma_0,2)^(1/(p-1))` — theory matches
  MC median within 0.1% over 60 seeds.
- **v0 / v1 deformation contracts** on Pantheon+ SH0ES distance
  moduli. Frozen artifacts:
  `empirical/aoc_threshold_contract_v0.md`,
  `empirical/aoc_proof_derived_contract_v1.md`. Real instruments,
  not evidence for AOC.
- **Planck operator-residue handle.** Cross-pipeline reconstruction
  distance metric on the four PR3 component-separated CMB maps
  (`empirical/planck_operator_residue/`). Two null controls passed
  (phase-shuffle, mask-aware galactic-cut); both rule out trivial
  confounds; neither tests the AOC claim directly.

## What is missing (theory side)

The bridge from instantiation back to gesture is not yet closed. The
proof spine has not yet committed a **number**: a predicted
`lambda_K`, a predicted operator-residue signature size, a predicted
axis direction or magnitude. Until the spine commits a number, every
empirical control narrows the noise floor without resolving the
question. We are at risk of *circling the square* — running tighter
controls forever without a discriminating prediction.

The move that breaks the circle is a theory move, not an empirical
one: derive apparatus-bound K from a specific near-cousin geometry
and predict a concrete number that distinguishes the bounded-observer
reconstruction from naive standard-cosmology analysis. Kerr-interior
is one candidate path. It is not the only one.

## Unsettled

- Whether "false bottom" implies a **committed beneath** (more
  universe past the horizon, structurally) or is **agnostic** about
  what sits below. The user has signaled the former; the conjecture
  is not yet pinned to it.
- Whether the cosmological principle here does **observer-symmetry**
  work (every apparatus sees the same boundary) or downstream
  **homogeneity-isotropy** work, or both. The relationship is not yet
  precise.
- Which near-cousin (if any) lifts cleanly to the gestural shape.
  Multiple are partial fits. The Kerr-cousin has the most ingredients
  (axial, multiple horizons, sustainable orbits) but is not committed.

## Discipline for agents using this document

- Treat the gesture as the conjecture. Treat near-cousins as partial
  maps useful for analogies and exploratory calculation.
- Do not lock a near-cousin as the conjecture without explicit user
  authorization to commit. The Kerr engagement in conversation can be
  productive *as a near-cousin*; locking it as the conjecture is the
  failure mode the user has flagged.
- Update this document when the gesture sharpens, not when a cousin
  moves.
- This document is a phase artifact. It should not grow beyond the
  shape of the conjecture itself.
