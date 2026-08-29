# Apparent-Origin Cosmology: Canonical Proof Spine

Status: working canonical document for this repo. This is not the submitted
Figure 3 companion. It is the current best version of the proof spine, with the
missing lemmas made explicit and with open control-analysis questions preserved
for later resolution.

Working thesis:

> The Big Bang boundary may be an apparent-origin surface: the deepest coherent
> reconstruction available to bounded observers, not necessarily the ontological
> beginning of the universe.

Canonical slogan:

> Boundary of reconstruction, not beginning of being.

Public metaphor:

> False bottom.

Formal posture:

> Apparent-Origin Cosmology does not deny cosmic expansion, CMB observations,
> early-universe thermodynamics, or the empirical success of standard
> `LambdaCDM`. It questions whether the earliest reconstructible boundary should
> be interpreted as an ontological beginning or as an observer-bounded
> reconstruction horizon.

## What This Document Does

This document consolidates four materials:

1. The current Figure 3 proof spine from
   `fig3_companion_scaling_cohomology.tex`.
2. The `T=0` / `Omega_O=0` universality clarification.
3. The adapted-filtration repair for observer-bounded cohomology.
4. The missing Test-Time / Amortization Boundary Lemma that connects Figure 2,
   Figure 3, LLM/human staging, and apparent-origin cosmology.

The goal is a canonical object that future images, simulations, website copy,
and rebuttal materials can inherit without re-inferring the idea from scratch.

## Nonclaims

This document does not claim:

1. The Big Bang is fake.
2. There was no hot dense early phase.
3. Cosmic expansion is only an illusion.
4. `LambdaCDM` has no empirical support.
5. The Figure 3 companion already proved every statement below in its submitted
   form.
6. Finite LLM prompts, human cognition, superconducting systems, and FRW
   cosmology are literally the same system.

It claims a narrower thing:

> Bounded observers can turn unresolved depth into apparent boundaries. When
> such a boundary is extremal in the reconstruction order, it can appear as an
> origin.

## Layer 0: The Observer-Bounded Setup

Let `X` be an underlying process space. Let `R_O` be an observer's
reconstruction space. Let

```tex
q_O : X \to R_O
```

be an observer-bounded reconstruction map. The observer has:

```tex
s_O > 0        \quad \text{resolution floor}
M_O < \infty   \quad \text{memory budget}
B_O < \infty   \quad \text{integration bandwidth}.
```

Define observer indistinguishability:

```tex
x \sim_O y
```

when the observer cannot maintain the distinction between `x` and `y` under
the budgets `(s_O, M_O, B_O)`.

Equivalently, all variations below the observer threshold are represented in
`R_O` as equivalence-class structure, not as further resolved internal depth.

This is the primitive move. Everything else is a structured version of it.

## Lemma 1: Observer-Quotient / Apparent-Origin Lemma

Statement:

Let `X` be an underlying process space and let

```tex
q_O : X \to R_O
```

be an observer-bounded reconstruction map. Suppose `U subset X` contains
variations that are not distinguishable by `O`, so that `q_O(U)` is represented
as a single equivalence class or a lower-dimensional image in `R_O`.

If `q_O(U)` is extremal with respect to the observer's reconstruction order,
then `q_O(U)` appears in `R_O` as a boundary, floor, cliff, residue, or apparent
origin, even when `U` is not an ontological boundary or origin in `X`.

Plain-language version:

> An apparent origin is a quotient artifact of bounded reconstruction.

Proof sketch:

1. By definition, `q_O` identifies all distinctions that fall below the
   observer's resolution, memory, or integration bandwidth.
2. Therefore unresolved internal variation in `U` is not represented as
   resolved depth in `R_O`; it is represented as an equivalence class.
3. If the reconstruction order has no represented predecessor below that class,
   then the class is extremal in `R_O`.
4. Extremal classes in a reconstruction order are interpreted operationally as
   floors, boundaries, or origins.
5. This conclusion is about the reconstruction `R_O`, not about the ontology of
   `X`.

Cosmological reading:

> The Big Bang boundary can be modeled as an apparent-origin surface: a deepest
> coherent reconstruction available to bounded observers.

## Lemma 2: Test-Time / Amortization Boundary Lemma

Purpose:

This lemma formalizes the line from the main paper:

```text
LLMs expose it per prompt, humans amortize sub-threshold.
```

Statement:

A bounded observer can encounter the same obstruction in two modes:

1. **Exposed mode**: the obstruction appears inside a single test-time act as a
   visible cliff, residue, boundary, or apparent origin.
2. **Amortized mode**: prior integration distributes the same obstruction
   across memory, embodiment, culture, instruments, staged computation, or
   external scaffolds, so the point-of-use behavior appears smooth.

Formal sketch:

Let `q_O : X -> R_O` be a bounded reconstruction map. Let `A` be an
amortization operator that augments the observer state:

```tex
O' = A(O)
```

by adding memory, staged certificates, tools, prior integration, or external
state. Then `O` and `O'` are different effective observers. A structure that
falls below the threshold of `O` may become resolved, partially resolved, or
smoothly approximated by `O'`.

Thus:

```tex
q_O(U)      \quad \text{may appear as an exposed boundary,}
```

while

```tex
q_{A(O)}(U) \quad \text{may appear as a smooth finite chart.}
```

Key sentence:

> Single-pass inference exposes the observer boundary; staged inference
> amortizes it within test-time compute and therefore changes the effective
> observer.

Human/LLM distinction:

Humans often arrive with an amortized observation floor produced by embodied
memory, culture, education, perceptual smoothing, and prior integration.
One-shot LLM inference often arrives with only the explicit prompt and context
state. Staged LLM pipelines add an artificial amortization layer through
scratchpads, certificates, retrieval, tools, and external ledgers.

This is an observer-thickness claim, not a metaphysical species claim.

Cosmological reading:

> Apparent origin equals exposed reconstruction boundary.

## Observer Thickness, Amortization Cost, and Atlas Fracture

Observer thickness is the effective capacity of an observer to preserve, stage,
and integrate distinctions before emitting a reconstruction.

Thin observers expose boundaries sharply: unresolved depth appears as a cliff,
residue, floor, or apparent origin.

Thick observers amortize boundaries across memory, embodiment, culture,
instruments, tools, retrieval, scratchpads, certificates, or staged
computation. The same obstruction can therefore appear smooth at point of use.

Canonical sentence:

> Observer thickness determines whether a boundary appears as a cliff or as
> smooth judgment.

No-free-lunch clause:

> Amortization does not eliminate the obstruction; it pays the cost elsewhere.

Staging moves cost from the exposed act of reconstruction into prior
integration, external memory, instrumentation, culture, or staged computation.
The obstruction is not destroyed. It is relocated into a different part of the
observer system.

Agency reading:

Agency is not unbounded freedom. An agent is not free because it has no
constraints. It is free to the extent that it can inspect, revise, stage, and
author the bounds under which it reconstructs.

Canonical sentence:

> Freedom is not escape from bounds; freedom is authorship of bounds.

Atlas fracture:

Atlas fracture occurs when an observer's coordinate charts no longer compose
coherently under drift. The observer may still emit local reconstructions, but
the transition maps between them fail. At that point, the system does not only
make a local error; it loses operational closure as a bounded observer.

For Apparent-Origin Cosmology, this is a control distinction:

> Apparent-origin claims are legitimate only when the reconstruction atlas
> remains coherent up to the boundary.

If the atlas fractures, the apparent boundary may be an artifact of failed
charting rather than a legitimate observer quotient. AOC therefore needs to
distinguish a coherent reconstruction horizon from mere atlas fracture.

## Layer 1: Observer-Bounded Access Functor

This is copied from the Figure 3 proof spine, with the missing scope clauses
made explicit.

An observer-bounded system is a tuple

```tex
\mathcal S = (V, \langle,\rangle, I, B, W),
```

where:

```tex
V              \quad \text{finite-dimensional real vector space,}
\langle,\rangle \quad \text{inner product,}
I              \quad \text{control-parameter interval,}
B_\lambda      \quad \text{symmetric positive semidefinite bilinear form,}
W \subset V    \quad \text{observer-accessible subspace.}
```

Define the observer-bounded access functor:

```tex
\Omega_O(\mathcal S)(\lambda)
 :=
\inf_{\substack{w \in W \\ \|w\|=1}}
\langle w,B_\lambda w\rangle.
```

Punctured finite-access convention:

All inverse-cost and boundary constructions are made first on

```tex
I^\circ := \{\lambda \in I : \Omega_O(\lambda)>0\}
```

and then passed to the boundary as `lambda -> lambda*`.

The boundary `Omega_O = 0` is not an ordinary observer state. It is the
singular strict-access limit. Operational staging lives in finite-access
charts. The associated graded records the leading boundary object.

Smoothness/germ convention:

The proof uses only the asymptotic germ of `Omega_O` near the critical
parameter. The target can be read as continuous, piecewise smooth, or
asymptotic-germ functions. If smoothness is needed, assume it on the punctured
neighborhood where the lowest observer-accessible eigenvalue has the stated
vanishing order.

## Lemma 3: Rayleigh Access Dual

Statement:

For a nonnegative quadratic form on `W`,

```tex
\kappa_O^{access}(\lambda)
 :=
\sup_{\|w\|=1}\langle w,B_\lambda w\rangle^{-1/2}
 =
\Omega_O(\lambda)^{-1/2},
```

with equality understood in the extended nonnegative reals.

Proof:

```tex
\sup_{\|w\|=1}\langle w,B_\lambda w\rangle^{-1/2}
=
\left(
\inf_{\|w\|=1}\langle w,B_\lambda w\rangle
\right)^{-1/2}.
```

Thus access cost diverges exactly when the restricted Rayleigh infimum
`Omega_O(lambda)` vanishes.

Important notation split:

```tex
\kappa_O^{access}
```

is scalar access cost. It is not the same object as the bundle curvature

```tex
\kappa_O
```

appearing in the curved bicomplex identity

```tex
D^2 = [\kappa_O,\cdot].
```

This distinction is load-bearing.

## Theorem 1: Universal Critical-Exponent Theorem

Statement:

Let `S` be an observer-bounded system. Suppose there exists
`lambda*` with

```tex
\Omega_O(\mathcal S)(\lambda)
=
c|\lambda-\lambda^*|^p
+ o(|\lambda-\lambda^*|^p),
\qquad c>0,\; p>0,
```

as `lambda -> lambda*` through the punctured finite-access domain. Then

```tex
\kappa_O^{access}(\lambda)
=
c^{-1/2}|\lambda-\lambda^*|^{-p/2}
+ o(|\lambda-\lambda^*|^{-p/2}).
```

Proof:

On the punctured domain, `Omega_O(lambda)>0`, so inverse square root is
well-defined. Write

```tex
\Omega_O(\lambda)
=
c|\lambda-\lambda^*|^p(1+o(1)).
```

Then

```tex
\Omega_O(\lambda)^{-1/2}
=
c^{-1/2}|\lambda-\lambda^*|^{-p/2}(1+o(1))^{-1/2}
=
c^{-1/2}|\lambda-\lambda^*|^{-p/2}(1+o(1)).
```

Therefore the access-cost exponent is `-p/2`.

Interpretation:

The exponent is universal only relative to the vanishing order of the access
functor. It does not assert equality of the finite systems that instantiate the
functor.

## Instance A: Cacophony Boundary

For the Cacophony family with `k` channels and pairwise coupling `rho`, the
observer-accessible capacity is modeled as

```tex
\Omega_O(\mathrm{Cacph}(k))(\rho)
=
1-\rho(k-1).
```

This vanishes linearly at

```tex
\rho^* = 1/(k-1).
```

Therefore `p=1`, and Theorem 1 gives access-cost exponent

```tex
-p/2 = -1/2.
```

This is the finite-budget feasibility boundary: as the Gram direction
approaches degeneracy, access cost diverges like the inverse square root of
the residual capacity.

## Instance B: FRW Cosmological Boundary

For a perfect-fluid FRW cosmology with constant equation-of-state parameter
`w > -1`, the scale factor satisfies

```tex
a(t) \propto t^{2/(3(1+w))}
```

near `t=0`. If the observer-access capacity is chosen as squared spatial scale,

```tex
\Omega_O(\mathrm{FRW}(w))(t) := a(t)^2,
```

then

```tex
\Omega_O(\mathrm{FRW}(w))(t)
\propto
t^{4/(3(1+w))}.
```

Thus the vanishing order is

```tex
p = 4/(3(1+w)).
```

The access-cost exponent is therefore

```tex
-p/2 = -2/(3(1+w)).
```

Examples:

```tex
w=0       \quad \text{matter era: exponent } -2/3,
w=1/3     \quad \text{radiation era: exponent } -1/2.
```

Interpretation:

This is a cosmological instance of the access-boundary theorem. It does not by
itself replace standard cosmology. It says that if `Omega_O=a(t)^2` is the
first FRW observer-access chart, then the apparent origin surface has a
controlled boundary exponent.

Question for Paul:

Is `Omega_O=a(t)^2` the canonical access choice for Apparent-Origin Cosmology,
or should it be explicitly called the first FRW chart, with other access
functors allowed for CMB, luminosity-distance, and lensing analyses?

## Layer 2: Curved Bicomplex

Let `U = {U_alpha}` be a good cover of the geometric realization `|K_t|`, and
let `(E,h_O,nabla_O)` be the observer-relative symbolic bundle over `|K_t|`.

Define the bigraded space:

```tex
C^{p,q}
:=
\check C^p(\mathcal U;\Omega^q(\cdot,\mathrm{End}(E))).
```

Let:

```tex
d_1 = \delta
```

be the Cech coboundary, and let:

```tex
d_2 = D_O
```

be the covariant exterior derivative induced by `nabla_O`. The total
differential is:

```tex
D := d_1 + (-1)^p d_2.
```

The curvature identity is:

```tex
D^2 = [\kappa_O,\cdot],
```

where `kappa_O` is the bundle curvature.

Scope:

This is a curved complex, not an ordinary cochain complex. Strict cohomology of
`(C,D)` is not defined unless the curvature vanishes. Observer-bounded
cohomology is therefore constructed on the associated graded, after the
filtration compatibility below is imposed.

## Layer 3: Omega_O Filtration

On the punctured finite-access family, define:

```tex
F^k C^{p,q}
:=
\{
\omega \in C^{p,q}
:
\|\omega(\cdot,\lambda)\|_{h_O}
= O(\Omega_O(\lambda)^k)
\text{ as } \lambda\to\lambda^*
\}.
```

Elements of `F^k` have filtration order at least `k`. Larger `k` means more
vanishing at the observer boundary.

The associated graded is:

```tex
\mathrm{gr}^k C := F^k C/F^{k+1}C.
```

Bookkeeping note:

Negative filtration orders may occur for divergent quantities. Positive orders
vanish faster at the boundary. Order `0` is bounded nonvanishing leading
content.

## Definition: Adapted Observer Filtration

The observer-induced curved bicomplex is adapted to the `Omega_O` filtration if
for every `k`,

```tex
D(F^k C^{\bullet\bullet})
\subseteq
F^k C^{\bullet\bullet}
```

and the bundle-curvature action is one observer order deeper:

```tex
[\kappa_O,F^k C^{\bullet\bullet}]
\subseteq
F^{k+1} C^{\bullet\bullet}.
```

Plain-language meaning:

> Curvature exists, but it is invisible to the leading observer-accessible
> symbol. It becomes visible in the next filtration layer.

This is the formal clause missing from the submitted Figure 3 proof.

Question for Paul:

Should adaptedness be treated as an assumption defining the canonical
observer-induced class, or as a theorem derived from the construction of
`A_O(s_O)` in the Figure 2 companion? The current safe version treats it as a
definition/assumption. A stronger version would need a proof from the kernel
construction.

## Lemma 4: Associated-Graded Differential

Statement:

If the observer-induced curved bicomplex is adapted to the `Omega_O`
filtration, then `D` induces a square-zero differential

```tex
\overline D:
\mathrm{gr}^k C^{\bullet\bullet}
\to
\mathrm{gr}^k C^{\bullet\bullet}.
```

Proof:

Since

```tex
D(F^k) \subseteq F^k,
```

the formula

```tex
\overline D[\omega] := [D\omega]
```

is well-defined on

```tex
\mathrm{gr}^k C = F^k C/F^{k+1}C.
```

If representatives differ by an element of `F^{k+1}`, their `D`-images differ
by an element of `F^{k+1}`.

For any class `[omega] in gr^k C`,

```tex
\overline D^2[\omega]
=
[D^2\omega]
=
[[\kappa_O,\omega]].
```

By adaptedness,

```tex
[\kappa_O,\omega] \in F^{k+1}C.
```

Therefore its class in `F^kC/F^{k+1}C` is zero. Hence:

```tex
\overline D^2=0.
```

This proves that observer-bounded cohomology is well-defined on the associated
graded.

## Definition: Observer-Bounded Cohomology

The observer-bounded cohomology of the adapted `Omega_O`-filtered curved
bicomplex is:

```tex
H_O^{k,n}
:=
H^n(\mathrm{gr}^k C^{\bullet\bullet},\overline D),
```

where `n` denotes total degree in the totalized bicomplex.

Interpretation:

Strict cohomology would require resolving curvature below the observer floor.
Observer-bounded cohomology records the leading obstruction content available
to the observer at the `Omega_O -> 0` boundary.

## Layer 4: Boundary Universality

The phrase "universal" means:

> universal at the observer-access boundary type, not equality of finite
> systems away from that boundary.

The relevant regimes are:

```tex
\Omega_O > 0      \quad \text{finite operational charts}
\Omega_O \to 0+   \quad \text{asymptotic boundary regime}
\Omega_O = 0      \quad \text{singular strict-access boundary}
```

Staging does not compute at the singular boundary. Staging moves the system
into finite-access charts, where subproblems have nonzero capacity. The
associated graded records the leading object that survives as those charts
approach the boundary.

Reviewer-safe sentence:

> Universality is claimed for the `Omega_O -> 0` boundary type, not for
> identical finite-observer dynamics. Single-pass LLM inference exposes this
> boundary per prompt; humans and staged systems may amortize the same
> obstruction across prior integration, making the boundary less visible at the
> point of use.

## Layer 5: Apparent-Origin Cosmology

Apparent-Origin Cosmology imports the same boundary logic into cosmology.

The Big Bang boundary is treated as a candidate reconstruction horizon:

```tex
\text{apparent origin}
=
\text{extremal observer quotient}
=
\text{deepest coherent reconstruction surface}.
```

This does not decide whether there is or is not an ontological beginning below
that surface. It says the empirical boundary in our reconstruction should not
automatically be promoted to metaphysical ground.

Formal bridge:

1. `Omega_O(t)` measures cosmological observer-access capacity.
2. `Omega_O(t)->0` produces diverging reconstruction cost.
3. The boundary class at `Omega_O=0` is not an ordinary observable event.
4. If the boundary is extremal in the reconstruction order, it appears as an
   origin.
5. Therefore "beginning" is a claim requiring additional ontology, not merely
   the presence of an observational floor.

Canonical phrase:

> The Big Bang as surface, not source.

## Empirical Burden Table

This is the minimum control ledger for Apparent-Origin Cosmology. It prevents
the model from becoming only metaphor.

| Observation | Standard account | AOC burden |
|---|---|---|
| Redshift-distance relation | Expanding spacetime | Reproduce or reinterpret redshift as a function of reconstruction geometry without losing observed regularities. |
| Supernova dimming and time dilation | Expansion history plus dark energy | Specify whether observer-threshold projection predicts the observed light-curve dilation relation. |
| CMB mean temperature and blackbody spectrum | Relic radiation from hot dense early phase | Preserve, reinterpret, or replace the thermal account without handwaving. |
| CMB anisotropy spectrum | Acoustic physics plus initial perturbations | Explain which features remain standard and which are threshold/reconstruction effects. |
| Light-element abundances | Big bang nucleosynthesis | State whether BBN is preserved as finite-chart physics or replaced by a new mechanism. |
| BAO scale | Early-universe acoustic standard ruler | Show whether BAO remains a real acoustic relic or is modified by reconstruction geometry. |
| Large-scale structure | Growth from initial perturbations under gravity | Reproduce growth statistics or identify testable deviations. |
| Lensing statistics | GR plus mass distribution | Specify whether threshold geometry changes horizon-scale lensing predictions. |
| High-redshift galaxy ages | Galaxy formation under expansion history | Identify whether AOC predicts a different age-redshift envelope. |

Question for Paul:

Does AOC preserve the standard hot dense finite-chart account above the
reconstruction horizon, with only the ontological status of the earliest
boundary demoted? Or does it aim to replace part of the early thermal history?
The first path is much safer and should be the default unless you explicitly
want the stronger claim.

## Control-Analysis Plan

The first operational target is not "explain everything." It is:

> identify one place where Apparent-Origin Cosmology and `LambdaCDM` disagree.

Candidate control analyses:

1. **Luminosity-distance residuals**:
   Compare standard `D_L(z)` to a threshold-projection correction.

2. **Cosmic time-dilation relation**:
   Test whether an apparent-origin projection preserves exactly the standard
   `(1+z)` dilation or predicts a controlled deviation.

3. **High-redshift age envelope**:
   Check whether the reconstruction horizon shifts inferred ages for very
   high-redshift galaxies.

4. **CMB low-ell anomalies**:
   Treat only the largest angular scales as candidate reconstruction-boundary
   artifacts, leaving the main acoustic structure intact.

5. **Horizon-scale lensing/caustic signature**:
   Ask whether a false-bottom surface creates a specific weak-lensing or
   magnification residual at very high redshift.

Negative controls:

1. No threshold: `q_O` is identity on the relevant depth variable.
2. Random threshold: boundary exists but is not extremal/coherent.
3. Smooth monotone reparameterization only: no quotient collapse.
4. Standard FRW chart: `Omega_O=a(t)^2` with no additional apparent-origin
   correction.

Acceptance standard:

> AOC becomes physically live only when it gives a quantitative deviation or
> invariant that survives these controls.

## Toy Model Skeleton

Goal:

Show a continuous underlying process whose bounded observer quotient creates an
apparent floor.

Underlying depth coordinate:

```tex
u \in (-\infty,\infty)
```

Observer threshold:

```tex
q_\epsilon(u)
=
\max(u,\epsilon)
```

or a smooth saturating map:

```tex
q_{\epsilon,\delta}(u)
=
\epsilon
+
\delta \log\left(1+\exp\left(\frac{u-\epsilon}{\delta}\right)\right),
\qquad \delta>0.
```

For `u << epsilon`, `q_{epsilon,delta}(u) approx epsilon`, so sub-threshold
depth is compressed into a false bottom. For `u >> epsilon`,
`q_{epsilon,delta}(u) approx u`, so above-threshold structure is preserved. The
parameter `delta` controls the smoothness of the transition.

A process with no ontological beginning in `u` can acquire an apparent origin
in `q_{epsilon,delta}(u)`.

This toy model is not cosmology. It proves the observer-quotient mechanism in
the simplest possible setting.

## Relation To Figure 2

Figure 2 establishes that bounded differentiation and bounded integration are
not exact inverses. The observer-relative FFTC leaves a residue:

```tex
D_O I_O(f) = f + \rho_O.
```

That residue is the local cost of bounded reconstruction. Staging is one way to
amortize or externalize this residue; it does not erase the underlying observer
bound.

The Test-Time / Amortization Boundary Lemma turns this into a cross-domain
principle:

> the same residue can appear as an exposed boundary in thin observers and as
> a smoothed sub-threshold cost in thick observers.

## Relation To Figure 3

Figure 3 establishes the boundary scaling:

```tex
\Omega_O \to 0
\quad \Rightarrow \quad
\kappa_O^{access} \sim \Omega_O^{-1/2}.
```

The adapted-filtration lemma establishes the cohomological carrier:

```tex
[\kappa_O,F^kC] \subseteq F^{k+1}C
\quad \Rightarrow \quad
\overline D^2=0 \text{ on } \mathrm{gr}^kC.
```

Together:

1. Figure 2 gives bounded reconstruction residue.
2. Figure 3 gives universal access-boundary scaling.
3. Adapted filtration gives observer-bounded cohomology.
4. Apparent-Origin Cosmology interprets cosmological origin surfaces as
   candidate reconstruction horizons.

## Repair To The Submitted Strict `r_min=0` Passage

Do not defend this sentence as written:

```tex
\|\omega(\cdot,\lambda)\|_{h_O}
=
O(\Omega_O(\lambda)^k)
\quad \text{for every } k.
```

For nonzero lambda-independent cochains, this is false for positive `k`.

Canonical replacement:

```tex
When s_O=0, the observer-induced curvature vanishes, so the curvature term
lies in every filtration level. Nonzero lambda-independent cochains have
filtration order 0; hence the filtration carries no nontrivial
observer-curvature obstruction in the strict limit. The associated-graded
observer-bounded construction reduces to the ordinary strict complex only after
the curvature obstruction has vanished.
```

Scope sentence:

```tex
The strict equivalence is a model statement for observer-induced, adapted
families; it is not a theorem about arbitrary filtered curved bicomplexes.
```

## Open Questions For Paul

These are the points where I should not silently choose the theory for you.

1. Should adapted filtration be a defining axiom of observer-induced bundles,
   or should we try to prove it from the Figure 2 smoothing-kernel
   construction?

2. Is `Omega_O=a(t)^2` the canonical FRW access capacity, or just the first
   chart?

3. Should AOC preserve standard hot dense early-universe thermodynamics above
   the reconstruction horizon, or is it meant to replace part of that story?

4. Which first quantitative disagreement with `LambdaCDM` do you want to
   target: luminosity distance, time dilation, CMB low-ell anomalies,
   high-redshift age envelope, or horizon-scale lensing?

5. Should "False Bottom" remain only a public metaphor while
   "Apparent-Origin Cosmology" is the formal project name?

6. Does the observer quotient need a measure/probability structure now, or can
   the first canonical proof stay topological/order-theoretic?

7. Should the human/LLM amortization claim remain a bridge lemma, or become a
   central theorem of the cosmology stack?

## Canonical Short Form

Use this paragraph as the source for other assets:

> Apparent-Origin Cosmology treats the Big Bang boundary as a candidate
> reconstruction horizon: the deepest coherent surface available to bounded
> observers, not automatically the ontological beginning of reality. The
> formal mechanism is the observer quotient: unresolved depth collapses into an
> extremal equivalence class, which appears as a floor, boundary, or origin.
> Figure 3 supplies the access-boundary scaling through `Omega_O -> 0`; the
> adapted-filtration lemma supplies the associated-graded cohomology; the
> amortization lemma explains why thin observers expose the boundary while
> staged or embodied observers may smooth it below threshold. The model must
> still pay the empirical bill: redshift, CMB, BBN, BAO, lensing, supernova
> time dilation, large-scale structure, and high-redshift ages.
