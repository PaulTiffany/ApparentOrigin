# Prismatic Decomposition Rigor

Status: Sprint E seed artifact.

Phase: methodological / epistemological, not new evidence.

Purpose:

Sprint E defines a robustness grammar for operator-residue features after the
Episode 3 Planck work. It does not add a new measurement and does not promote
any Planck feature to AOC evidence. It names how a feature should be decomposed
before it is allowed to travel into stronger empirical or theory-side claims.

Core question:

```text
When a structure appears, which decomposition prisms does it survive,
and which prism creates, destroys, or recomposes it?
```

This document is the instrumentation-side complement to
`docs/lambda_k_kerr_interior_strategy.md`. The Kerr-interior lane asks whether
a theory-side `lambda_K` can be derived. Sprint E asks what decomposition
contract a future `lambda_K` prediction would have to survive.

## 1. Why Sprint E follows Sprint D

Sprint D calibrated the Episode 2 parallel-fifths finding against a documented
surrogate null:

```text
real Planck operator axes -> frozen counterpoint detector -> LambdaCDM
surrogate-pipeline null
```

That was the right next step after Sprint A. It measured whether the
ell=3 all-six-pair lockstep pattern was ordinary under the chosen null model.

Sprint E asks a different question. It does not ask whether the pattern is rare
inside one detector coordinate. It asks whether the pattern has been
decomposed through enough independent observational prisms that future work can
say what kind of object it is:

1. multipole-local feature,
2. mask-induced recomposition,
3. operator-bound residue,
4. shared-target residue candidate,
5. or a mixture that should not yet be promoted.

Drift note: "shared-target residue candidate" is used here instead of
"sky-candidate" to avoid quietly promoting a reconstruction-stable residue into
sky ontology.

## 2. The Three Prisms

### Multipole Prism

Question:

```text
Does the feature live at one multipole, across a low-ell band,
or through high-ell leakage?
```

The multipole prism separates:

1. ell=2 behavior,
2. ell=3 behavior,
3. quadrupole-octupole relation,
4. low-band behavior,
5. high-ell leakage behavior.

Episode 3 current read:

1. The headline parallel-fifths lockstep is ell=3-local under the Sprint D
   detector.
2. The ell=2 observed pair count sits in the null bulk under Sprint D.
3. The quadrupole-octupole cliff is real in the tested directional-axis
   coordinate, but it is a relation between multipoles, not a single-multipole
   claim.
4. The high-ell leakage null broadened the cliff distribution but did not cross
   the predeclared explanation boundary in the tested control.

Allowed promotion:

```text
The current strongest feature is not "low ell in general"; it is a specific
ell=3 operator-motion pattern plus a related Q-O recomposition cliff.
```

Forbidden promotion:

```text
Low-ell anomaly validates AOC.
```

### Mask / Sky-Partition Prism

Question:

```text
Does the feature depend on one hand-made cut, or does it persist across
mask-family variation?
```

The mask prism separates:

1. unmasked extraction,
2. synthetic galcut family,
3. fine synthetic cut localization,
4. high-ell leakage under the same synthetic cut family,
5. official Planck common-mask morphology.

Episode 3 current read:

1. P1 localized the coarse Q-O cliff into the predeclared 22 to 25 degree
   synthetic-cut window, with the largest fine-grid jump at 23 to 24 degrees.
2. P2 found that simple high-ell leakage did not fully explain the cliff under
   the tested high-ell null.
3. P3 found that a cliff-like recomposition survives the first official-mask
   morphology family, though not at the same sky fraction or as a universal
   latitude threshold.
4. Sprint D showed that mask geometry contributes meaningfully to surrogate
   lockstep, especially at noise scale 0.5x, but is insufficient in that model
   to reproduce the observed all-six-pair ell=3 pattern.

Allowed promotion:

```text
The mask is not a nuisance to subtract after the fact. It is an operator
transition whose geometry can create, destroy, or recompose low-ell structure.
```

Forbidden promotion:

```text
Mask sensitivity makes the result meaningless.
```

### Operator Prism

Question:

```text
Does agreement mean independent recovery, shared reconstruction-floor behavior,
or one-operator pathology?
```

The operator prism separates:

1. Commander,
2. NILC,
3. SEVEM,
4. SMICA,
5. pairwise operator motion,
6. per-operator cross-octave behavior.

Episode 3 current read:

1. Sprint A found all six operator pairs triggering the parallel-fifths analog
   at ell=3 under the unmasked to galcut20 transition.
2. Sprint D calibrated that all-six-pair detector output against surrogate
   pipelines, not the actual internal algorithmic logic of the four Planck
   component-separation methods.
3. Sprint C-prime showed that all four operators loosen their per-operator
   quadrupole-octupole alignment under galcut20, with different magnitudes.
4. SEVEM remains important as a possible outlier/rejoining case, especially in
   ell=2 behavior.

Allowed promotion:

```text
The operator prism interrogates the Pipeline Independence Postulate by testing
whether agreement survives operator decomposition.
```

Forbidden promotion:

```text
The Pipeline Independence Postulate has been refuted.
```

## 3. Feature-State Vocabulary

Use these labels when carrying an Episode 3 feature forward:

| label | meaning | example use |
| --- | --- | --- |
| `survives a prism` | remains qualitatively present after the relevant decomposition | cliff-like recomposition under first official-mask morphology |
| `collapses under a prism` | disappears when the relevant decomposition is applied | a feature present only in one operator |
| `recomposes` | changes sector or relation coherently across a boundary | ell=2 G-to-F sector movement across the fine-cut transition |
| `operator-bound` | lives in reconstruction-operator behavior, not yet sky ontology | pairwise lockstep under a detector coordinate |
| `mask-bound` | depends on mask geometry or sky partition | galcut-driven axis motion |
| `shared-target residue candidate` | survives enough operator and mask variation to deserve ordinary CMB controls | not yet established by Sprint E alone |
| `theory-contact candidate` | clean enough for a future `lambda_K` prediction to specify | requires a derived prediction, not a fitted reading |

These are not honorifics. They are routing labels.

## 4. Applying the Grammar to Episode 3

### P1/P2/P3 Q-O Cliff

Current state:

```text
multipole prism: Q-O relation, not low-ell-general
mask prism: localized under fine synthetic cuts; cliff-like under official mask
operator prism: at least three of four operators participate in ell=2 sector
recomposition across the localized transition
```

Best label:

```text
mask-sensitive Q-O recomposition feature
```

Allowed next step:

Use this as a target for extractor robustness and official-mask-family
extensions.

Forbidden next step:

Treat the cliff as a universal 25 degree boundary or as evidence for a cosmic
phase transition.

### Sprint D Parallel-Fifths Lockstep

Current state:

```text
multipole prism: strongest at ell=3; ell=2 in null bulk
mask prism: galcut20 contributes to surrogate lockstep but does not reproduce
the observed all-six-pair pattern in the tested sensitivity sweep
operator prism: all six real Planck operator pairs trigger the detector, but
the null uses surrogate pipelines
```

Best label:

```text
ell=3 operator-lockstep feature under masked transition
```

Allowed next step:

Replace surrogate operator-noise with a more realistic component-separation or
foreground-residual control before making claims about actual Planck algorithm
independence.

Forbidden next step:

State that LambdaCDM is ruled out or that the four real Planck pipelines are
not independent in their full algorithmic construction.

### Sprint C-prime Duets

Current state:

```text
multipole prism: per-operator Q-O alignment angle
mask prism: unmasked to galcut20 transition
operator prism: four separated two-voice readouts
```

Best label:

```text
composition-layer inspection of per-operator Q-O detuning
```

Allowed next step:

Use the duet form as a listening guide and a communication artifact for the
already-computed axis values.

Forbidden next step:

Treat the WAV files as independent evidence.

## 5. Handshake with the `lambda_K` Lane

Sprint E does not derive `lambda_K`.

Its role is to define the decomposition contract a future `lambda_K`
prediction would have to survive. A theory-side prediction should specify, in
advance:

1. which prism it addresses,
2. which observable coordinate it predicts,
3. whether it predicts survival, collapse, or recomposition,
4. which null or control could disconfirm it,
5. which phase the claim occupies.

The minimal handshake sentence is:

```text
`lambda_K` predicts only after it says which prism it expects the residue to
survive.
```

That keeps the theory lane and the instrumentation lane coupled without
letting either one borrow authority from the other.

## Allowed Claims

1. Sprint E defines a disciplined robustness grammar for Episode 3
   operator-residue features.
2. The three prisms are multipole, mask/sky-partition, and operator
   decomposition.
3. The grammar clarifies whether a feature is multipole-local,
   mask-sensitive, operator-bound, or ready for stronger controls.
4. Sprint E prepares later `lambda_K` predictions for cleaner empirical
   contact.

## Forbidden Claims

1. Triple-prism survival confirms AOC.
2. Triple-prism survival refutes LambdaCDM.
3. Operator agreement proves sky ontology.
4. Mask sensitivity makes a result meaningless.
5. Sprint E derives `lambda_K`.
6. A feature may be promoted from operator-bound to shared-target residue
   candidate without ordinary CMB controls.
