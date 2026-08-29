# K-Parameter Theory

Status: working note.

Purpose:

The FRW observer-quotient chart uses a finite reconstruction budget `K`.
At present, `K` is a free parameter. That makes Apparent-Origin Cosmology
interpretive rather than predictive.

This document records why `K` is load-bearing and lays out the three live
framings:

1. apparatus-bound `K`,
2. RG-effective `K`,
3. fundamental `K`.

The immediate recommendation is to develop apparatus-bound `K` first. Treat
RG-effective `K` as the harder follow-on, and defer any fundamental-constant
claim.

Companion notes:

1. `docs/cacophony_to_k_bridge.md`
   - Transfers the Cacophony operationalization discipline into AOC without
     importing LLM-specific variables as cosmology.
2. `docs/apparatus_bound_k_program.md`
   - Gives the first concrete definition of apparatus-bound `K` from pipeline
     reliability and atlas coherence.

## 1. Why K Matters

In the first FRW observer-quotient chart:

```tex
\kappa_O^{access}(t)=\frac{1}{a(t)}
```

and a finite observer reconstructs only times satisfying:

```tex
\kappa_O^{access}(t)\le K.
```

The reconstruction floor is defined by:

```tex
\kappa_O^{access}(t_K)=K.
```

For a perfect-fluid FRW chart with:

```tex
a(t)=A t^{2/(3(1+w))},
```

this gives:

```tex
t_K=(AK)^{-3(1+w)/2}.
```

Thus `K` sets the apparent-origin surface.

If `K` is arbitrary, the surface is arbitrary. If `K` is calculable, the
surface becomes a physical or operational prediction.

## 2. Current Status

The current chart establishes:

1. how a finite `K` produces a quotient boundary,
2. how that boundary moves as `K` changes,
3. how `K -> infinity` recovers the strict FRW boundary.

It does not yet establish:

1. what sets `K`,
2. whether `K` is observer/instrument dependent,
3. whether `K` has a universal limiting value,
4. whether `K` changes observable cosmological inference.

That is the next major proof and modeling burden.

## 3. Framing A: Apparatus-Bound K

In this framing, `K` is determined by the actual reconstruction apparatus:

```tex
K = K(\mathcal I,\mathcal M,\mathcal P),
```

where:

```tex
\mathcal I \quad \text{instrument stack}
\mathcal M \quad \text{model class / inference pipeline}
\mathcal P \quad \text{priors, calibration, and data-processing choices}.
```

Candidate contributors:

1. photon count / signal-to-noise,
2. angular resolution,
3. spectral resolution,
4. redshift uncertainty,
5. foreground subtraction error,
6. lensing reconstruction uncertainty,
7. model degeneracy,
8. numerical precision and regularization,
9. prior strength,
10. survey depth and selection function.

Interpretation:

`K` is not a cosmic constant. It is the effective budget of a concrete observer
pipeline. Better instruments or better staging increase `K`, lowering `t_K`.

This framing is safest because it does not compete with `LambdaCDM` directly.
It says:

> Apparent-origin surfaces are reconstruction floors induced by finite
> apparatus and inference budgets.

First calculable target:

Given a simplified observation pipeline, define a maximum reliable inverse
scale-factor reconstruction:

```tex
K_{app} \sim \frac{1}{a_{min}^{reconstructible}}.
```

Then ask whether `a_{min}` is set by noise, resolution, survey limits, or model
priors.

Near-canonical consequence:

> In the apparatus-bound framing, the apparent-origin surface is the surface
> where the reconstruction pipeline runs out of dynamic range on the scale
> factor.

In the first FRW chart, `K` bounds `1/a(t)`. Thus:

```tex
K_{app} \sim \frac{1}{a_{min}^{reconstructible}}
```

directly identifies `t_K` with the time at which the apparatus/model pipeline
can no longer resolve the scale factor. This gives AOC a physics-shaped
prediction:

> Different observation pipelines should yield systematically different
> effective `t_K` values, with differences calculable from instrument,
> inference, and prior specifications.

This is not yet a claim that those differences are detectable. It is the
prediction shape that makes apparatus-bound `K` more than metaphor.

## 4. Framing B: RG-Effective K

In this framing, `K` emerges from coarse-graining.

Let `ell` be a reconstruction scale. Then:

```tex
K = K(\ell)
```

and changing scale changes the effective observer.

Coarse charts have lower `K`; refined charts have higher `K`. The apparent
origin surface is therefore scale-dependent:

```tex
t_{K(\ell)}.
```

This matches the broader observer-bounded program:

> observer thickness is a scale-dependent capacity to preserve distinctions.

Possible RG-style relation:

```tex
\ell_2 < \ell_1
\quad \Rightarrow \quad
K(\ell_2) \ge K(\ell_1)
```

with:

```tex
t_{K(\ell_2)} \le t_{K(\ell_1)}.
```

Current limitation:

The monotonicity relation above is not yet an RG argument. It says that finer
resolution should preserve more distinctions, but it does not give a running
equation such as:

```tex
\frac{dK}{d\log \ell} = \beta(K).
```

Until such a beta function or explicit coarse-graining model is derived,
RG-effective `K` should be treated as a follow-on program, not as co-equal with
apparatus-bound `K`.

Follow-on target:

Build a toy model in which smoothing scale `ell` induces a quotient floor.
Then test whether the floor runs monotonically under refinement.

## 5. Framing C: Fundamental K

In this framing, `K` is set by a physical bound:

```tex
K = K_*
```

Candidate sources might include:

1. Planck-scale cutoff,
2. entropy/holographic bounds,
3. quantum measurement limits,
4. causal horizon information bounds,
5. finite computational capacity of an observer patch.

Private bookmark:

Of these, entropy/holographic bounds are the most natural bridge if the
program ever needs a fundamental `K`, because they already speak in the
language of finite information capacity for observer-accessible regions.
Planck cutoffs, quantum measurement limits, causal horizons, and computation
limits may matter, but holographic/covariant entropy bounds are the closest
mainstream quantitative machinery to the AOC question.

This is the boldest framing and should be deferred.

If AOC claims a fundamental `K_*`, it owes:

1. an order-of-magnitude value,
2. a derivation from known physics or a clearly stated new postulate,
3. an empirical consequence,
4. a comparison to existing singularity-resolution, bounce, cyclic, and
   holographic models.

Until then, `K_*` should remain an open possibility, not a public claim.

## 6. Recommended Near-Term Choice

Use:

```text
apparatus-bound K
```

as the working theory.

Treat:

```text
RG-effective K
```

as the follow-on once apparatus-bound `K` has a concrete observer-pipeline
model and once there is a candidate running equation.

Do not use:

```text
fundamental K
```

except as a deferred research path.

Reason:

Apparatus-bound `K` is where the first actual work happens: signal, noise,
resolution, priors, and distinguishability can be modeled directly.
RG-effective `K` fits the broader observer-bounded story, but it currently
lacks a rate law. Fundamental `K` is a deferred high-risk path.

## 7. How This Affects The FRW Chart

The FRW chart should be read as conditional:

```tex
\text{given } K, \text{ derive } t_K.
```

It is not yet:

```tex
\text{derive } K \text{ from cosmology}.
```

That means the chart currently proves a mechanism, not a new cosmological
prediction.

The next step is:

```tex
\text{derive or estimate } K \text{ for a specific reconstruction pipeline}.
```

## 8. First Modeling Task

Build a toy observer pipeline with:

1. a hidden depth variable `t`,
2. a signal `S(t)`,
3. noise `sigma`,
4. a distinguishability condition,
5. a derived maximum access cost `K`.

Example:

```tex
\text{distinguishable}(t_1,t_2)
\quad \Longleftrightarrow \quad
|S(t_1)-S(t_2)| > n\sigma.
```

Then define:

```tex
K_{eff}
=
\sup\{\kappa_O^{access}(t): t \text{ remains distinguishable}\}.
```

This turns `K` from a free parameter into an output of an observer model.

## 9. Long-Term Empirical Shape: Pipeline Disagreement

The apparatus-bound framing predicts that different reconstruction pipelines
can yield different effective origin floors:

```tex
K_1 \ne K_2
\quad \Rightarrow \quad
t_{K_1} \ne t_{K_2}.
```

This has the same broad shape as pipeline-dependent cosmological tensions, such
as early-universe CMB-anchored inference versus late-universe distance-ladder
inference.

Guardrail:

> AOC does not currently claim to explain the Hubble tension.

A mature `K` theory would need to predict the sign and order of magnitude of
pipeline disagreements before making contact with that problem. Until then,
the Hubble-tension connection is a long-term test shape, not a result.

## 10. Guardrail

Do not diagnose critics as "observer-thin" until the burden table, controls,
and `K` theory have been addressed.

Canonical discipline rule:

> Criticism routes first through burden, controls, and falsification. Only
> after that may observer-thickness be discussed.

Private discipline:

Even when the framework predicts refused recruitment or thin-observer behavior,
that prediction does not license bypassing the burden table. The scientific
response remains controls, falsification criteria, and specific behavioral
failure modes, not psychologizing the critic.
