# FRW Observer-Quotient Chart

Status: first concrete chart for Apparent-Origin Cosmology.

Purpose:

This document instantiates the Observer-Quotient / Apparent-Origin Lemma in a
specific FRW chart. The goal is to make the false-bottom mechanism do actual
work rather than remain only a slogan.

This is not yet a replacement for `LambdaCDM`. It is a controlled chart showing
how a bounded observer can derive an apparent-origin surface from finite access
capacity.

## 0. Current Caveats

This chart is a mechanism proof, not yet a predictive cosmology. Three points
remain load-bearing:

1. **Access-cost provenance.** The relation
   `kappa_O^{access}=Omega_O^{-1/2}` is imported from the Figure 3
   observer-access functor. This chart uses it as the first FRW access
   formalism; a native cosmology derivation remains open.

2. **Reconstruction order.** The order in Section 6 is currently induced by
   the chosen time chart and quotient. A stronger version should derive the
   order from distinguishability, causal reconstructibility, information cost,
   or an explicit observer pipeline.

3. **The K-parameter.** `K` is currently a finite reconstruction budget. Until
   `K` is derived or estimated from apparatus, coarse-graining, or a physical
   bound, the chart is interpretive rather than predictive. See
   `docs/k_parameter_theory.md`.

## 1. Claim

In a perfect-fluid FRW chart, if observer-access capacity is represented by

```tex
\Omega_O(t) = a(t)^2,
```

then any finite observer with maximum access budget `K < infinity` has a
minimum reconstructible time `t_K > 0`. Histories with

```tex
0 < t < t_K
```

are quotiented into a boundary class by the observer reconstruction map. That
class is minimal in the observer reconstruction order, so it appears as an
apparent-origin surface for that observer.

As `K -> infinity`, the apparent-origin surface moves toward the FRW singular
boundary:

```tex
t_K -> 0.
```

Core sentence:

> The Big Bang boundary is modeled here as the infinite-budget limit of finite
> observer reconstruction floors.

## 2. FRW Background

Use a spatially homogeneous and isotropic FRW chart:

```tex
ds^2 = -dt^2 + a(t)^2 d\Sigma_k^2,
```

where `a(t)` is the scale factor and `dSigma_k^2` is the spatial metric of
constant curvature `k`.

For a perfect fluid with constant equation-of-state parameter `w > -1`,

```tex
a(t) = A t^\alpha,
\qquad
\alpha = \frac{2}{3(1+w)},
\qquad
A>0,
```

near `t=0`.

The first FRW observer-access chart chooses:

```tex
\Omega_O(t) := a(t)^2 = A^2 t^{2\alpha}.
```

This is not declared to be the only possible cosmological access functor. It is
the first chart because it directly measures squared spatial scale available to
the observer.

## 3. Access Cost

Define scalar access cost:

```tex
\kappa_O^{access}(t)
:=
\Omega_O(t)^{-1/2}
=
\frac{1}{a(t)}
=
A^{-1}t^{-\alpha}.
```

This access-cost law is inherited from the general observer-access functor:

```tex
\kappa_O^{access}=\Omega_O^{-1/2}.
```

In this chart, the first FRW access capacity is `Omega_O=a(t)^2`, so the law
becomes `kappa_O^{access}=1/a(t)`. A later version should either derive this
access law directly from a cosmological reconstruction task or keep it
explicitly scoped as the Figure 3 access-functor import.

Thus:

```tex
\kappa_O^{access}(t)
=
A^{-1}t^{-2/(3(1+w))}.
```

As `t -> 0+`, access cost diverges.

For common cases:

```tex
w=0       \quad \Rightarrow \quad \kappa_O^{access}(t)\sim t^{-2/3}
```

```tex
w=1/3     \quad \Rightarrow \quad \kappa_O^{access}(t)\sim t^{-1/2}.
```

## 4. Observer Budget

Let the observer have finite reconstruction budget:

```tex
K < \infty.
```

In this document, `K` is conditional input, not yet derived output. The chart
proves:

```tex
K \mapsto t_K.
```

It does not yet prove:

```tex
\text{cosmology} \mapsto K.
```

The live theories of `K` are apparatus-bound, RG-effective, and fundamental.
The current working path is apparatus-bound plus RG-effective.

The observer can resolve times `t` only when:

```tex
\kappa_O^{access}(t) \le K.
```

The reconstruction floor `t_K` is defined by:

```tex
\kappa_O^{access}(t_K)=K.
```

Solving:

```tex
A^{-1}t_K^{-\alpha}=K,
```

so:

```tex
t_K = (AK)^{-1/\alpha}.
```

Since

```tex
\alpha=\frac{2}{3(1+w)},
```

we get:

```tex
t_K = (AK)^{-3(1+w)/2}.
```

Interpretation:

> Every finite observer has a nonzero reconstruction floor.

As budget increases:

```tex
K_2 > K_1
\quad \Rightarrow \quad
t_{K_2} < t_{K_1}.
```

As `K -> infinity`:

```tex
t_K -> 0.
```

## 5. Reconstruction Space

Let the underlying FRW history domain be:

```tex
X := (0,\infty)
```

with coordinate `t`.

For a finite observer with budget `K`, define the reconstruction space:

```tex
R_{O,K} := \{B_K\} \cup [t_K,\infty),
```

where `B_K` is a boundary class representing all sub-budget histories:

```tex
B_K \equiv (0,t_K).
```

Define the observer quotient map:

```tex
q_{O,K}: X \to R_{O,K}
```

by:

```tex
q_{O,K}(t)
=
B_K,
\qquad 0<t<t_K,
```

and

```tex
q_{O,K}(t)
=
t,
\qquad t\ge t_K.
```

This is the hard-threshold quotient.

## 6. Reconstruction Order

Define the observer reconstruction order `<=_O` on `R_{O,K}` by:

```tex
B_K \le_O t
\quad \text{for all } t\ge t_K,
```

and for resolved times:

```tex
t_1 \le_O t_2
\quad \text{iff} \quad
t_1 \le t_2.
```

Then `B_K` is the unique minimal element of `R_{O,K}`.

Thus the quotient image of unresolved early histories is extremal in the
observer reconstruction order.

By the Observer-Quotient Lemma, `B_K` appears as a boundary, floor, or apparent
origin in `R_{O,K}`.

Order caveat:

This order is presently stipulated by the chart. A stronger version should
derive it from a concrete reconstructibility relation, for example:

```tex
x \le_O y
\quad \Longleftrightarrow \quad
\text{the observer can reconstruct } x \text{ no later/deeper than } y.
```

or from an information-cost monotone. Until then, the proposition establishes
the quotient mechanism in the chosen chart, not an observer-independent cosmic
ordering theorem.

## 7. Apparent-Origin Proposition

Proposition:

For the first FRW observer-access chart

```tex
\Omega_O(t)=a(t)^2,
```

every finite observer budget `K` induces an apparent-origin boundary class

```tex
B_K = q_{O,K}((0,t_K)).
```

This boundary is observer-relative. It is not identical to an ontological
beginning in the underlying domain `X`.

Proof:

1. `kappa_O^{access}(t)=1/a(t)` diverges as `t->0+`.
2. For finite budget `K`, there exists a unique `t_K>0` satisfying
   `kappa_O^{access}(t_K)=K`.
3. For `0<t<t_K`, reconstruction cost exceeds budget, so those histories are
   not individually resolved.
4. The quotient map `q_{O,K}` identifies `(0,t_K)` as one class `B_K`.
5. `B_K` is minimal in `R_{O,K}` under `<=_O`.
6. Therefore `B_K` is an apparent-origin surface for the finite observer.

This proves the false-bottom mechanism in the first FRW chart.

## 8. Smooth Quotient Variant

The hard quotient is mathematically clean but physically abrupt. A smooth
observer map can use a shifted softplus floor:

```tex
q_{K,\delta}(t)
=
t_K
+
\delta \log\left(1+\exp\left(\frac{t-t_K}{\delta}\right)\right),
\qquad \delta>0.
```

For:

```tex
t \ll t_K,
```

we have:

```tex
q_{K,\delta}(t)\approx t_K.
```

For:

```tex
t \gg t_K,
```

we have:

```tex
q_{K,\delta}(t)\approx t.
```

The parameter `delta` controls transition smoothness. The hard quotient is
recovered as:

```tex
\delta \to 0+.
```

Interpretation:

The false bottom does not require a literal discontinuity. It requires a
bounded observer map whose derivative collapses below the reconstruction floor.

## 9. Observer Thickness

An observer-thickening operation increases the effective reconstruction budget:

```tex
A(O_K)=O_{K'},
\qquad
K'>K.
```

Then:

```tex
t_{K'} < t_K.
```

The apparent-origin surface moves deeper:

```tex
B_K \rightsquigarrow B_{K'}.
```

Staging, instruments, memory, external ledgers, and accumulated theory all act
as observer-thickening operations when they increase effective reconstruction
budget or preserve distinctions that the thinner observer would collapse.

No-free-lunch clause:

> Amortization does not eliminate the obstruction; it pays the cost elsewhere.

In this chart, increased observer thickness lowers `t_K` by paying more
reconstruction cost.

## 10. Controls

The chart should be stress-tested against controls.

### Control 1: Infinite Budget

Let:

```tex
K=\infty.
```

Then:

```tex
t_K=0.
```

No finite false bottom remains. The observer can in principle approach the FRW
singular boundary.

### Control 2: No Divergent Access Cost

If `a(t)` does not vanish and `Omega_O(t)` remains bounded below by a positive
constant, then `kappa_O^{access}` does not diverge. A finite budget need not
induce an apparent-origin floor.

### Control 3: Random Threshold

If a threshold is imposed without being induced by access cost, the resulting
floor is a modeling artifact, not an observer-quotient boundary.

### Control 4: Smooth Reparameterization Only

If a coordinate change merely reparameterizes `t` without quotienting
sub-budget histories, it does not create an apparent-origin class. The false
bottom requires loss of resolved distinctions, not only a change of variables.

### Control 5: Atlas Fracture

If transition maps between reconstruction charts fail before `t_K`, then the
apparent boundary may be an artifact of failed charting rather than a coherent
observer quotient.

Apparent-origin claims are legitimate only when the reconstruction atlas remains
coherent up to the boundary.

## 11. What This Chart Establishes

This chart establishes:

1. A concrete `X`.
2. A concrete `Omega_O`.
3. A concrete access cost.
4. A concrete finite budget `K`.
5. A concrete observer quotient map `q_{O,K}`.
6. A concrete reconstruction space `R_{O,K}`.
7. A concrete reconstruction order `<=_O`.
8. A derived apparent-origin class `B_K`.

This makes Lemma 1 do work in a specific FRW setting.

## 12. What This Chart Does Not Establish

This chart does not yet establish:

1. A replacement for `LambdaCDM`.
2. A new fit to observational data.
3. A reinterpretation of CMB anisotropies.
4. A reinterpretation of BBN.
5. A prediction for luminosity-distance residuals.
6. A prediction for supernova time dilation.
7. A complete account of BAO or large-scale structure.

It is the first derivation of the apparent-origin mechanism, not the full
physics program.

## 13. Next Quantitative Step

The next step is to ask whether the finite-budget quotient changes any
observable inference.

Before fitting observables, the immediate modeling step is to make `K`
non-free. Pick a specific observer pipeline and derive:

```tex
K_{eff}
=
\sup\{\kappa_O^{access}(t): t \text{ remains distinguishable under the pipeline}\}.
```

Candidate first target:

```tex
D_L(z)
```

the luminosity-distance relation.

Question:

Does replacing the strict lower boundary `t=0` with a finite reconstruction
floor `B_K` produce any controlled residual in inferred luminosity distance,
cosmic age, or high-redshift observables?

If yes, AOC gets a first possible empirical handle.

If no, the chart is still useful as an interpretive reconstruction-horizon
model, but not yet a competing physics model.

## 14. Canonical Short Form

> In the first FRW observer-access chart, `Omega_O(t)=a(t)^2`, access cost is
> `1/a(t)` and diverges as `t->0+`. A finite observer budget `K` therefore
> defines a minimum reconstructible time `t_K`. Histories with `0<t<t_K` are
> quotiented into a boundary class `B_K`, which is minimal in the observer's
> reconstruction order and therefore appears as an apparent origin. As observer
> thickness increases, `K` rises and `t_K` moves toward zero. Thus the Big Bang
> boundary can be modeled as the infinite-budget limit of finite false bottoms:
> a reconstruction horizon, not automatically the beginning of being.
