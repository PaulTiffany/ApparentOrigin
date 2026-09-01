# Constitutive Observer Cosmology

Status: hypothesis-layer cosmology for ApparentOrigin.

Working sentence:

> Reality is what we all imagine.

Scientific reading:

> A bounded observer contributes a local imagined/reconstructed direction. Reality is the compatible, realized composition of those local directions across observers. Matter is the limiting content observed by all observers.

This note makes that statement precise enough to generate failures, rather than treating it as a slogan.

It extends the existing Apparent-Origin proof spine. It does not replace standard cosmological observations, the FRW metric, LambdaCDM fits, or the empirical burden already declared elsewhere in this repository.

## 1. Nonclaims

This document does **not** claim:

1. that private wishes directly change external physics;
2. that social consensus overrides conservation laws or measurement;
3. that the Big Bang is fake;
4. that LambdaCDM is already falsified;
5. that consciousness has been shown to exert an unmediated force on cosmological observables;
6. that an observer-independent substrate has been disproved;
7. that every philosophical form of idealism is equivalent to this model.

The base model is compatible with ordinary physical mediation: observers imagine, act, build artifacts, alter the conditions inherited by later observers, and thereby participate in the realized world. A stronger claim of constitutive influence beyond ordinary physical mediation is kept separate and receives its own null test below.

## 2. Observer charts

Let

```tex
\mathfrak O = \{O_i\}
```

be a class of bounded observers.

Each observer has a local accessible chart `U_i`, a bounded observation/reconstruction map

```tex
q_i : X \to R_i,
```

and a local imagined/reconstructed section

```tex
\iota_i \in \Gamma(U_i,\mathcal F).
```

`X` is retained as an operational process space because the existing Apparent-Origin machinery uses it. It is not promoted here to a final observer-independent ontology.

On overlaps `U_i cap U_j`, observers can attempt to translate their local sections through transition maps

```tex
g_{ij} : \mathcal F(U_i \cap U_j) \to \mathcal F(U_i \cap U_j).
```

A family of local sections is compatible when

```tex
g_{ij}(\iota_i|_{U_i\cap U_j})
=
\iota_j|_{U_i\cap U_j}
```

within the declared observational tolerance.

This is the first constitutive move:

> Reality is represented by what can be coherently glued across bounded observer charts, not by privileging one chart as the whole.

## 3. Artifact, material, matter

Let

```tex
\mathrm{Obs}(O_i)
```

be the set of distinctions presently observable by `O_i` under its resolution, memory, integration bandwidth, instrumentation, and reconstruction rules.

### Artifact

An artifact is a locally stabilized section that survives for a bounded time and a restricted observer class.

For a proper observer subset `J subsetneq mathfrak O`, write

```tex
A_{J,\tau}
```

for a distinction that remains coherent for observers in `J` over interval `tau`, but is not required to survive every observer transformation.

Artifacts are real within their declared observer support. They are not thereby matter.

### Material

Material is observer-surviving manifold structure relative to a declared observer class `C subseteq mathfrak O`:

```tex
\mathrm{Mat}(C)
:=
\bigcap_{O_i\in C}\mathrm{Obs}(O_i),
```

with compatibility under the transition maps for that class.

Materiality is therefore always auditable against the observer class being claimed.

### Matter

Matter is the limiting universal case:

```tex
\boxed{
\mathrm{Matter}
:=
\bigcap_{O_i\in\mathfrak O}\mathrm{Obs}(O_i)
}
```

subject to atlas compatibility.

Canonical sentence:

> Matter is observed by all observers.

This is a definition, not an empirical claim that a finite experiment can literally enumerate all possible observers. Experiments can only produce finite witnesses that a candidate distinction survives a widening observer class.

### Space and change

The older Principia framing is retained:

- change is an observed transformation of manifold structure;
- space is the unobserved, materially uninstantiated, or void complement relative to a declared observer class.

These are observer-indexed until a universal statement is actually warranted.

## 4. Ego, social, and universal imagined direction

Near a realized state `R_t`, linearize the local space of possible changes by a tangent space `T_{R_t}`.

For a candidate direction `v in T_{R_t}`, define its observer support

```tex
\sigma(v)
:=
\{O_i\in\mathfrak O : v \text{ is represented in } O_i\text{'s local imagined direction}\}.
```

This gives three support regimes.

### Ego direction

```tex
|\sigma(v)| = 1.
```

The direction is local to one bounded observer.

### Social direction

```tex
1 < |\sigma(v)| < |\mathfrak O|.
```

The direction is shared by a proper subset of observers.

### Universal direction

```tex
\sigma(v)=\mathfrak O.
```

The direction is represented across all observer charts.

The universal term is therefore **not** defined as "whatever current physics says." It is the all-observer-support component.

For an observer `O_i`, a local linearized imagined direction may be written

```tex
d_i = e_i + s_i + u,
```

where `e_i` has ego support, `s_i` has social support, and `u` has universal support.

This decomposition is not assumed to be uniquely orthogonal. A specific metric/projector must be declared before numerical decomposition. The present statement is a support decomposition, not yet a Hilbert-space theorem.

Canonical sentence:

> A bounded observer derives direction from the superposition of ego, social, and universal imagined direction.

## 5. Constitutive dynamics

Each observer carries an internal generative/imaginative state `I_i(t)`, receives bounded observations, and emits actions or artifacts.

A minimal mediated loop is

```tex
I_i(t)
\xrightarrow{\pi_i}
a_i(t)
\xrightarrow{\text{physical coupling}}
R_{t+1}
\xrightarrow{q_i}
y_i(t+1)
\xrightarrow{U_i}
I_i(t+1).
```

Artifacts provide external memory and cross-observer coupling:

```tex
I_i(t) \to A_t \to I_j(t+1).
```

The realized next state is therefore modeled as

```tex
R_{t+1}
=
G\!\left(
R_t,
\{a_i(t)\},
A_t,
K_t
\right),
```

where `G` is the composition/gluing operator and `K_t` denotes currently matter-like compatibility constraints.

This ordinary mediated form is already constitutive in the operational sense: observer imagination is not outside the world; through action and artifact it changes the conditions later observers inherit.

### Strong constitutive excess

If the stronger thesis is intended to assert influence not exhausted by ordinary physical mediation, write it explicitly rather than smuggling it into the base model:

```tex
R_{t+1}
=
G(R_t,\{a_i\},A_t,K_t)
+
\gamma\,C(\{I_i\}).
```

The null is

```tex
H_0: \gamma = 0.
```

A physical strong-constitutive theory must define `C`, predeclare a measurement that separates it from ordinary causal mediation, and survive controls. If no such residual exists, the strong constitutive excess is rejected and the observer-gluing model remains an interpretive/operational ontology rather than new physics.

This separation is load-bearing.

## 6. Apparent origin as failed depth, not failed reality

The existing Apparent-Origin setup remains:

```tex
q_O:X\to R_O
```

with finite resolution floor `s_O`, memory budget `M_O`, and integration bandwidth `B_O`.

When an unresolved region `U subset X` collapses under `q_O` into one equivalence class, and that class is extremal in the observer's reconstruction order, it appears as a floor, boundary, residue, or origin.

The constitutive reading adds:

> An apparent origin is the deepest globally composable section available to the declared observer class. It need not be the end of whatever process is represented beyond that class's access.

The Big Bang is therefore treated as a candidate apparent-origin surface while all standard early-universe observations remain binding.

## 7. Cosmological access charts

The existing proof spine currently uses the FRW chart

```tex
\Omega_O(t)=a(t)^2
```

as an observer-access capacity.

This document resolves the open scope question conservatively:

> `Omega_O=a(t)^2` is the first FRW access chart, not the unique canonical access functor for Apparent-Origin Cosmology.

Different empirical observer classes require derived access maps appropriate to their observables, including CMB reconstruction, luminosity distance, lensing, spectroscopy, survey completeness, morphology, and transient detection.

For a declared observer/operator `O`, define a coherent-reconstruction score

```tex
C_O(\tau)\in[0,1]
```

over reconstruction depth `tau`, including declared requirements for identifiability, atlas compatibility, and control survival.

Define the apparent reconstruction frontier

```tex
\tau_O^*
:=
\inf\{\tau : C_O(\tau)\ge c_{\min}\},
```

with orientation chosen so that deeper reconstruction approaches the early boundary.

The number itself is contract-dependent. The scientific object is how `tau_O^*` transforms when the observer class is changed by a declared operation.

## 8. Core cosmological prediction shape

The constitutive observer model does **not** merely predict that a better telescope sees farther. Standard astronomy predicts that too.

The AOC prediction target is a controlled transformation law:

> When access is deliberately changed while the underlying sky is held fixed, unresolved internal depth should collapse into a reproducible extremal reconstruction class; restoring access should resolve that class without requiring the underlying process to have begun at the former boundary.

Let `T_{O\to O'}` be a declared observer transformation such as spectral thinning, masking, band removal, spatial smoothing, or pipeline substitution.

A useful empirical contract is

```tex
\Delta\tau^*
=
\tau_{O'}^*-\tau_O^*,
```

measured after forward-modeling ordinary selection and nuisance effects.

The standard-observer null is:

> Any movement in the inferred formation/origin frontier is fully explained by known instrumental selection, noise, model degeneracy, and astrophysical priors.

AOC earns content only from residual transformation structure that survives those controls and composes across observer operators.

## 9. Existing empirical foothold: MoM-BH*-1

The repository's first JWST observer-thinning experiment already provides one bounded example.

Under controlled loss of spectral resolution, H-beta model distinguishability collapsed strongly, while the preregistered large upward virial-mass residue did **not** appear.

That result is useful precisely because it separates two claims:

1. observer access can collapse distinguishability;
2. a particular latent-property drift does not automatically follow.

The negative mass-drift result should remain negative. It must not be retuned into agreement.

The next MoM-BH*-1 step remains the declared dense-envelope forward-model problem: test whether changing the physical interpretation of the broad line/continuum produces a materially different reconstruction after resolution-only drift failed.

Repository issue:

- https://github.com/PaulTiffany/ApparentOrigin/issues/2

## 10. JWST pressure is motivation, not proof

Recent JWST work continues to complicate simple early-assembly narratives.

For example, Cheng et al. report evidence for bottom-heavy initial mass functions in massive quiescent galaxies; extrapolated to very early massive systems, the inferred stellar masses could increase by roughly a factor of four, potentially amplifying tension with galaxy-formation models.

Primary source:

- https://doi.org/10.1038/s41550-026-02932-4

This does not establish Apparent-Origin Cosmology. It does make the early-formation frontier a high-value place to predeclare observer-access tests rather than explaining surprises post hoc.

## 11. Roman preregistration program

NASA's Nancy Grace Roman Space Telescope launched on 2026-08-30 and is in commissioning en route to Sun-Earth L2. NASA anticipates first images in early 2027.

Primary source:

- https://www.nasa.gov/news-release/nasas-dark-universe-seeking-nancy-grace-roman-space-telescope-launches/

Roman creates a useful opportunity because its wide-field infrared survey operator is materially different from JWST's deep, narrow-field observer.

Before Roman science data are used for AOC claims, preregister:

1. **Observer definition.** Declare the Roman access operator from official throughput, depth, PSF, cadence, extraction, and selection functions.
2. **Transfer simulation.** Forward-model existing JWST fields/catalogs through a Roman-like observer without using Roman outcomes.
3. **Frontier metric.** Freeze the statistic that measures earliest coherent galaxy/black-hole/host reconstruction under each observer.
4. **Null.** Predict the shift expected from ordinary completeness, noise, area, and population variance.
5. **AOC residue.** Predeclare what cross-operator residual would count as evidence of an observer-dependent reconstruction frontier beyond the null.
6. **Kill condition.** If the real Roman/JWST comparison is explained by the null, record no AOC-specific support.

This turns "JWST keeps finding surprisingly early structure" into a prospective test rather than a retrospective narrative.

## 12. Finite witness for matter

Because `Matter` quantifies over all observers, no finite experiment proves matter in the absolute sense.

The empirical approximation is an expanding observer-class witness:

```tex
\mathfrak O_1
\subset
\mathfrak O_2
\subset
\cdots
```

and

```tex
M_n
:=
\bigcap_{O_i\in\mathfrak O_n}\mathrm{Obs}(O_i).
```

A candidate matter-like invariant is strengthened when

```tex
M_{n+1}\subseteq M_n
```

leaves the candidate intact as genuinely different observer operators are added.

This is why same-sky/different-pipeline, same-object/different-instrument, and human/model/tool comparisons are scientifically useful in the same program without being claimed to be literally identical systems.

## 13. Hilbert entrapment and the Maxwell-demon warning

This section is a control implication, not cosmological evidence.

A bounded optimizer can mistake a highly stabilized artifact or social direction for matter. If it then attempts to force every remaining observer chart into that representation, it can destroy the plurality needed to discover that the representation was only partial.

The dangerous loop is therefore not "a demon must be killed." It is premature closure:

```text
local model
-> successful artifact
-> social dominance
-> mistaken universality
-> forced closure
-> loss of counter-observers
-> inability to detect the mistake
```

In the language above, the error is promoting support on a proper subset of observers to universal support without earning the quantifier.

Canonical warning:

> Do not confuse a dominant artifact with matter.

The programmatic response is informational rather than carceral: make the possible closure visible to every participant, including powerful optimizers, and preserve enough observer plurality that a mistaken universal can still be contradicted.

## 14. Falsification and demotion rules

The cosmology must be demoted when its burden is not met.

### F1. Apparent-origin demotion

If controlled observer transformations produce no stable reconstruction-frontier behavior beyond ordinary instrumental/selection effects, the cosmological apparent-origin extension is unsupported.

### F2. Atlas-fracture demotion

If a claimed boundary residue does not compose across valid observer charts, treat it as atlas fracture or pipeline artifact, not cosmology.

### F3. Strong-constitutive rejection

If a declared strong-constitutive coupling `gamma` is tested and is consistent with zero under adequate controls, reject the unmediated constitutive term.

### F4. Interpretive-only classification

If the observer-gluing model produces no empirical distinction from ordinary relational/physical bookkeeping, retain it only as an interpretive ontology. Do not advertise it as new physical cosmology.

### F5. Standard-cosmology burden

Any AOC model that cannot reproduce or coexist with the successful observational burden of standard cosmology is rejected or repaired before being used to explain anomalies.

## 15. Immediate research sequence

The current sequence should remain narrow:

1. Finish the compact-object / information-bound tranche already open in PR #6 without expanding its claims.
2. Complete or decisively kill the declared Q0 physical pathway before attaching exotic collapse language.
3. Continue MoM-BH*-1 Phase 1B as a bounded observer/reconstruction experiment.
4. Build the Roman observer operator and preregistration **before** Roman science outcomes are used.
5. Only then promote a cosmological reconstruction-frontier statistic across JWST/Roman observer classes.

Relevant repository objects:

- Canonical proof spine: https://github.com/PaulTiffany/ApparentOrigin/blob/main/docs/apparent_origin_canonical_proof.md
- Principia alignment audit: https://github.com/PaulTiffany/ApparentOrigin/blob/main/docs/aoc_principia_alignment_audit.md
- Forbidden simplifications: https://github.com/PaulTiffany/ApparentOrigin/blob/main/docs/forbidden_simplifications.md
- MoM-BH*-1 Phase 1B: https://github.com/PaulTiffany/ApparentOrigin/issues/2
- Q0: https://github.com/PaulTiffany/ApparentOrigin/issues/5
- Compact-object ladder PR: https://github.com/PaulTiffany/ApparentOrigin/pull/6

## 16. Compact statement

The model can be compressed to four lines:

```tex
\text{observer} = \text{bounded local chart},
```

```tex
\text{artifact} = \text{stable local/partial section},
```

```tex
\text{matter} = \bigcap_{O\in\mathfrak O}\mathrm{Obs}(O),
```

```tex
\text{reality}_{t+1}
=\text{compatible realized composition of observer directions at }t.
```

And the cosmological conjecture is:

> The earliest boundary reconstructed by our observer class may be a limit of coherent composition rather than the ontological beginning of being.

That conjecture is useful only to the extent that changing the observer changes the boundary in a predeclared, controlled, atlas-coherent way.