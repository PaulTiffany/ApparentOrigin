# Repo Operating Loop

Status: working protocol for this repository.

Purpose:

This repo should function as an operational home base for Apparent-Origin
Cosmology, not as a loose collection of prompts. The loop is:

```text
Principia alignment -> proof spine -> controlled chart -> toy model ->
empirical burden -> media asset
```

No media asset should outrun the proof spine. No proof claim should skip the
empirical burden table.

## 1. Proof Loop

Goal:

Tighten the formal claims without over-closing the theory.

Inputs:

1. `docs/apparent_origin_canonical_proof.md`
2. `docs/frw_observer_quotient_chart.md`
3. `docs/k_parameter_theory.md`
4. `docs/aoc_principia_alignment_audit.md`

Current load-bearing questions:

1. Does the claim respect the observer-horizon / escape-horizon framing?
2. Can `kappa_O^{access}=Omega_O^{-1/2}` be derived natively in the FRW chart?
3. Can the reconstruction order be derived from a pipeline rather than
   stipulated?
4. Can apparatus-bound `K` be estimated from instrument and inference
   specifications?
5. Can a first `D_L(z)` comparison be written without claiming too much?
6. Can an operator-residue test be specified on the same target reconstructed
   by multiple pipelines?

Exit condition:

A proof change is accepted only when it clarifies definitions, strengthens a
derivation, or marks an open assumption more honestly.

## 2. Simulation Loop

Goal:

Make every abstract mechanism touch a small executable object.

Current toy:

`simulations/false_bottom_projection/`

Next simulations:

1. FRW `t_K` calculator for perfect-fluid equations of state.
2. Apparatus-bound `K` sensitivity sweep.
3. Smooth quotient comparison across several thresholds.
4. First luminosity-distance sandbox.

Exit condition:

A simulation is useful only if it states what it does not prove.

## 3. Empirical Loop

Goal:

Convert AOC from interpretation toward physics by forcing contact with
cosmological observables.

Main checklist:

`docs/empirical_burden_table.md`

Near-term target:

Operator-residue analysis:

```text
same target -> multiple reconstruction operators -> stable or unstable residue
```

First candidate:

```text
Planck CMB component-separated maps:
Commander, NILC, SEVEM, SMICA
```

Secondary target:

Apparatus-bound pipeline disagreement:

```tex
K_1 \ne K_2
\quad \Rightarrow \quad
t_{K_1} \ne t_{K_2}.
```

Guardrail:

Do not claim AOC explains the Hubble tension until the sign and order of
magnitude are predicted before comparison.

## 4. Media Loop

Goal:

Create images, stories, and video prompts that recruit attention while
preserving the mathematical constraints.

Inputs:

1. `media/image_atlas.md`
2. `media/graphic_novel_bible.md`
3. `media/prompt_pack.md`
4. `docs/forbidden_simplifications.md`

Exit condition:

Every media artifact must be captioned as compression, not evidence.

## 5. Site Loop

Goal:

Maintain a public-facing research homepage that routes readers to the strongest
current objects first.

Current site:

`site/index.html`

Exit condition:

The site should make it hard for a reader to confuse AOC with "the Big Bang is
fake." The first click should route to the proof spine or guardrails.

## 6. Agent Loop

Goal:

Use agents as tooling extensions while preserving authorship of bounds.

Protocol:

1. Give the agent the canonical thesis.
2. Give the agent the forbidden simplifications.
3. Ask for a concrete artifact, not vibes.
4. Route every strong claim through the burden table.
5. Preserve open questions instead of hiding them.
6. Record useful outputs as repo files.

Failure mode:

The agent produces fluent explanation that weakens constraints. Treat this as
atlas fracture: local text remains smooth, but transition maps no longer
compose.

Canonical sentence:

> The agent becomes useful when it helps author the bounds instead of merely
> speaking inside them.
