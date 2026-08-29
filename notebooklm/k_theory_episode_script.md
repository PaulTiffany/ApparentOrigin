# K-Theory Episode Script

Status: internal technical briefing draft.

## Title

What Sets K?

## Opening

**Host A:** In Apparent-Origin Cosmology, the `K` parameter is the next
load-bearing problem. The first FRW chart shows how a finite reconstruction
budget creates an apparent-origin surface, but that only becomes physics if `K`
is derived or estimated from an observer pipeline.

**Host B:** The short version is: if `K` is arbitrary, the boundary is
arbitrary. If `K` is calculable, the apparent-origin surface becomes an
operational prediction.

## Segment 1: Why Cacophony Matters

**Host A:** The useful transfer from Cacophony is methodological. Cacophony
does not give AOC a cosmological constant. It gives a discipline: take a
classical bound and make it operational through a calibrated interface.

**Host B:** In Cacophony, the interface is a generative oracle with calibrated
query cost, bounded displacement, violation detection, feasibility surrogates,
and routing policies.

**Host A:** For AOC, the analogous object is a reconstruction oracle: an
instrument stack, model class, reduction pipeline, calibration procedure, and
control layer that together determine how deep a boundary can be reconstructed
reliably.

**Host B:** That distinction matters. LLM constraint cliffs do not prove
cosmological claims. They teach us how to make bounded-observer claims
operational.

## Segment 2: Defining Apparatus-Bound K

**Host A:** The first FRW chart uses inverse scale factor as the access-cost
variable:

```tex
y(t)=1/a(t)=1+z.
```

**Host B:** A concrete pipeline estimates this quantity with uncertainty:

```tex
\sigma_P(y).
```

**Host A:** Then a first apparatus-bound definition is:

```tex
K_{P,\eta}
=
\sup
\left\{
y :
\sigma_P(y)/y \le \eta
\right\}.
```

**Host B:** In plain language, `K` is the deepest inverse-scale-factor value
the pipeline can reconstruct within accepted relative error.

## Segment 3: Mapping K to t_K

**Host A:** If the FRW scale factor is:

```tex
a(t)=A t^\alpha,
```

then:

```tex
y(t)=A^{-1}t^{-\alpha}.
```

**Host B:** Set `y(t_K)=K_P`, and the pipeline-specific apparent-origin time is:

```tex
t_K(P)=(A K_P)^{-1/\alpha}.
```

**Host A:** This gives the core apparatus-bound statement:

> The apparent-origin surface is the time at which a concrete reconstruction
> pipeline runs out of reliable dynamic range on inverse scale factor.

## Segment 4: The Toy Model

**Host B:** The first toy uncertainty law is:

```tex
\sigma_P(y)=\sigma_0 y^p,\qquad p>1.
```

**Host A:** Then:

```tex
K_{P,\eta}
=
\left(\eta/\sigma_0\right)^{1/(p-1)}.
```

**Host B:** So lowering `sigma_0`, meaning improving reconstruction quality,
increases `K` and pushes `t_K` earlier.

**Host A:** That is not empirical evidence for AOC. It is the first executable
apparatus-bound `K` mechanism.

## Segment 5: Atlas Coherence

**Host B:** Reliability is not enough. A smooth extrapolation can be precise and
wrong.

**Host A:** So the stronger definition adds an atlas-coherence control. If
multiple charts estimate the same boundary quantity, their transition maps must
compose within tolerance. Otherwise, what looks like a horizon may be atlas
fracture.

**Host B:** This is the same discipline as Cacophony's screening-statistic
rule. A risk indicator triggers checks. It does not render a verdict.

## Segment 6: Routing, Not Always-Staging

**Host A:** Another Cacophony lesson is that staging is not automatically good.
The value is selective staging.

**Host B:** For AOC, that means more instruments, priors, model passes, or
calibration layers are not free. They may increase `K`, but they also pay cost
and can introduce new degeneracy.

**Host A:** So the right policy is not "always add more machinery." It is:
simple reconstruction in low-risk regimes, staged reconstruction in moderate
risk regimes, and reject or defer in high-risk regimes.

## Close: Next Tasks

**Host B:** The next implementation task is the apparatus-bound `K` toy model:
compute `K_P`, compute `t_K(P)`, compare two pipelines, and add an
atlas-fracture cutoff.

**Host A:** After that, the harder task is to replace the toy uncertainty law
with a real or realistic observation pipeline.

**Host B:** The guardrail remains: apparatus-bound `K` is a route toward
physics, not a shortcut around the empirical burden.

