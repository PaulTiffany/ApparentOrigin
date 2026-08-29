# Figure 3 Companion: Perfect-Proof Aim With Minimal Edits

This document is not a rewrite of `fig3_companion_scaling_cohomology.tex`.
It is a proof repair plan in the style of a contract redline: identify the
missing obligations, then add the smallest clauses/lemmas needed to make the
document defensible.

The central idea is sound:

> Work on the punctured finite-access family `Omega_O > 0`, then pass to the
> associated graded as `Omega_O -> 0`. The strict `T=0` or `Omega_O=0` point is
> not an ordinary operational stage. It is the boundary whose leading observable
> content is captured by the associated graded.

The current proof mostly needs sharper bookkeeping.

## Plain-English Unification

There are three layers that must not be collapsed:

1. **Access capacity**: `Omega_O(lambda)` is what the observer can resolve.
   When this goes to zero, access cost diverges.

2. **Operational finite-time charts**: actual LLM prompts, human reasoning
   episodes, and finite cosmological observations live at `Omega_O > 0`.
   They are not the strict boundary.

3. **Boundary invariant**: the universal claim lives at the associated-graded
   boundary as `Omega_O -> 0`, not as equality of finite systems.

In contract terms: the paper does not need a new deal. It needs definitions
that say exactly which party is obligated to do what.

## The Main Problem To Fix

The current observer-bounded cohomology definition says:

```tex
Because $D^2 = [\kappaO,\cdot]$ ... acts by lowering filtration order ...
it descends to zero on $\mathrm{gr}^{\bullet}$.
```

That sentence is doing too much work. To make it rigorous, add the missing
filtration-compatibility condition:

```tex
D(F^k C) \subseteq F^k C
```

and

```tex
[\kappaO, F^k C] \subseteq F^{k+1} C.
```

Then the proof is immediate:

```tex
\overline D^2[\omega]
= [D^2\omega]
= [[\kappaO,\omega]]
= 0
\quad \text{in } F^k C/F^{k+1}C.
```

This is the one lemma the proof most needs.

## Important Notation Split

A reviewer can get confused because `kappa` language is doing two jobs.

Use distinct names mentally, and if revision is allowed, on paper:

1. `\kappaO^{\mathrm{access}}`: scalar access cost, equal to
   `Omega_O^{-1/2}`. This can diverge.
2. `\kappaO`: bundle curvature in the curved bicomplex, where
   `D^2 = [\kappaO,\cdot]`.

The associated-graded cohomology needs the **bundle curvature action** to be
one filtration order deeper than the leading finite-access differential. The
scalar access cost may diverge; that is not the same object as the curvature
term that must vanish on `gr`.

Minimal edit if there is no room for notation changes:

```tex
Here $\kappaO$ denotes the bundle curvature in the curved bicomplex, not the
scalar access cost $\kappaO^{\mathrm{access}}=\OmegaO^{-1/2}$.
```

## Minimal Required Patch Set

### Patch 1: Add A Punctured-Boundary Convention

Best location: before Section 2 or before the filtration section.

```tex
\paragraph{Punctured finite-access convention.}
All asymptotic constructions below are made on the punctured observer domain
\[
I^\circ := \{\lambda \in I : \Omega_{\mathcal O}(\lambda)>0\}
\]
and then passed to the associated graded as $\lambda\to\lambda^*$.
The boundary $\Omega_{\mathcal O}=0$ is not an ordinary observer state;
it is the singular strict-access limit. Operational staging lives in
finite-access charts, while observer-bounded cohomology records the
leading boundary object seen by the observer.
```

Why this matters:

- It protects the `T=0` argument.
- It explains why staging is not a contradiction of universality.
- It prevents a reviewer from treating `Omega_O=0` as an actual step in the
  algorithm.

### Patch 2: Correct The Rayleigh Dual Wording

Current proof has the right target but a risky sentence about minimizing the
inverse expression. Replace the proof paragraph with:

```tex
The infimum exists because $B_\lambda$ is continuous and the unit sphere in
$W$ is compact. Functoriality follows from the definition of morphisms.
For a nonnegative quadratic form,
\[
\sup_{\|w\|=1}\langle w,B_\lambda w\rangle^{-1/2}
=
\left(\inf_{\|w\|=1}\langle w,B_\lambda w\rangle\right)^{-1/2},
\]
with the equality understood in the extended nonnegative reals. Thus the
access cost diverges exactly when the restricted Rayleigh infimum
$\Omega_{\mathcal O}(\lambda)$ vanishes.
```

Why this matters:

- It removes an easy optimization-wording objection.
- It keeps the theorem unchanged.

### Patch 3: Add Smoothness/Germ Scope To `Omega_O`

Current definition maps to `C^\infty(I; R_{\ge 0})`, but the smallest
Rayleigh quotient need not be smooth at eigenvalue crossings.

Minimal insertion after Definition 2:

```tex
In the arguments below we use only the asymptotic germ of
$\Omega_{\mathcal O}$ near the critical parameter $\lambda^*$.
Equivalently, one may replace $C^\infty(I;\mathbb R_{\ge 0})$ by the
space of nonnegative continuous, piecewise-smooth, or asymptotic-germ
functions. When smoothness is stated, it is assumed on the punctured
neighborhood in which the lowest observer-accessible eigenvalue has the
specified vanishing order.
```

Why this matters:

- It prevents a technical smoothness objection.
- It does not change the scaling theorem.

### Patch 4: Add The Adapted Filtration Assumption

Best location: after Definition 4, the `Omega_O`-filtration.

```tex
\begin{definition}[Adapted observer filtration]
\label{def:adapted-filtration}
The observer-induced curved bicomplex is \emph{adapted} to the
$\Omega_{\mathcal O}$-filtration if, for every $k$,
\[
D(F^k C^{\bullet\bullet}) \subseteq F^k C^{\bullet\bullet}
\]
and the bundle curvature action is one observer order deeper:
\[
[\kappa_{\mathcal O},F^k C^{\bullet\bullet}]
\subseteq F^{k+1} C^{\bullet\bullet}.
\]
This says that curvature is invisible to the leading observer-accessible
symbol, while remaining visible in the next filtration layer.
\end{definition}
```

Why this matters:

- It supplies the exact condition currently hidden in the phrase
  "curvature has definite order."
- It is the smallest honest assumption needed for `\bar D^2 = 0`.

### Patch 5: Add The Square-Zero Lemma

Best location: immediately before observer-bounded cohomology.

```tex
\begin{lemma}[Associated-graded differential]
\label{lem:graded-differential}
If the observer-induced curved bicomplex is adapted to the
$\Omega_{\mathcal O}$-filtration, then $D$ induces a square-zero
differential
\[
\overline D:\mathrm{gr}^k C^{\bullet\bullet}\to
\mathrm{gr}^k C^{\bullet\bullet}.
\]
\end{lemma}

\begin{proof}
Since $D(F^k)\subseteq F^k$, the formula
$\overline D[\omega]=[D\omega]$ is well-defined on
$\mathrm{gr}^k C=F^kC/F^{k+1}C$; if representatives differ by an element
of $F^{k+1}$, their $D$-images also differ by an element of $F^{k+1}$.
For any $[\omega]\in\mathrm{gr}^k C$,
\[
\overline D^2[\omega]
= [D^2\omega]
= [[\kappa_{\mathcal O},\omega]].
\]
By adaptedness, $[\kappa_{\mathcal O},\omega]\in F^{k+1}C$, so its class
in $F^kC/F^{k+1}C$ is zero. Hence $\overline D^2=0$.
\end{proof}
```

Why this matters:

- It makes Definition 5 valid.
- It is the cleanest rebuttal to the cohomology objection.

### Patch 6: Replace The Risky Sentence In Definition 5

Replace:

```tex
Because $D^2 = [\kappaO, \cdot]$ (Lemma~\ref{lem:curvature})
acts by lowering filtration order (curvature has a definite
$\OmegaO$-order), it descends to zero on $\mathrm{gr}^\bullet$,
and $\overline{D}^2 = 0$. The graded cohomology is therefore
well-defined.
```

with:

```tex
By Lemma~\ref{lem:graded-differential}, adaptedness of the
$\Omega_{\mathcal O}$-filtration implies that $\overline D^2=0$.
The graded cohomology is therefore well-defined.
```

Why this matters:

- It removes unsupported proof language from a definition.
- It points to the actual lemma.

### Patch 7: Specify Total Degree

Minimal insertion in Definition 5:

```tex
Here $n$ denotes total degree in the totalized bicomplex.
```

Why this matters:

- It prevents a bigraded bookkeeping objection.

### Patch 8: Quarantine The Strict `r_min=0` Theorem

This is the only part I would not defend as currently written. The line

```tex
\|\omega(\cdot,\lambda)\|_{\hO}=O(\OmegaO(\lambda)^k)
\quad \text{for every } k\in\mathbb Z
```

is false for nonzero lambda-independent cochains when `k > 0`.

Minimal replacement for that part:

```tex
When $\rmin=0$, the observer-induced curvature vanishes, so the curvature
term lies in every filtration level. Nonzero $\lambda$-independent cochains
have filtration order $0$; hence the filtration carries no nontrivial
observer-curvature obstruction in the strict limit. The associated-graded
observer-bounded construction therefore reduces to the ordinary strict
complex only after the curvature obstruction has vanished.
```

If the theorem statement currently requires `F^k C = C` for all `k`, change
the statement. That equality is not worth defending.

Minimal theorem-scope sentence:

```tex
The equivalence below is a model theorem for observer-induced, adapted,
analytic families; it is not a claim about arbitrary filtered curved
bicomplexes.
```

Why this matters:

- It avoids a real mathematical falsehood.
- It preserves the conceptual use: strict solvability is the zero-observer-bound
  limit, while finite observers use the associated-graded theory.

## Perfect Proof Spine

This is the proof you want the paper to have after minimal edits.

### Step A: Define observer access

`Omega_O(lambda)` is the least observer-accessible Rayleigh capacity on the
punctured domain. Its inverse square root is the access cost. If
`Omega_O -> 0`, access cost diverges.

Needed assumptions:

- Work in extended nonnegative reals.
- Work on `Omega_O > 0` before taking the boundary limit.
- Smoothness is only needed as an asymptotic germ near `lambda*`.

### Step B: Prove universal exponent

If

```tex
\Omega_O(lambda) = c |lambda-lambda*|^p + o(|lambda-lambda*|^p),
```

then

```tex
\Omega_O(lambda)^{-1/2}
= c^{-1/2}|lambda-lambda*|^{-p/2}(1+o(1)).
```

This part is fine once punctured positivity is stated.

### Step C: Define the curved bicomplex

`D^2 = [kappa_O,.]` is the curvature identity. This is fine as a curved
complex statement.

Needed clarification:

- `kappa_O` here is bundle curvature, not scalar access cost.

### Step D: Add adapted filtration

The finite observer sees leading symbols. The curvature obstruction is
subleading relative to that leading symbol:

```tex
[\kappa_O,F^kC] subset F^{k+1}C.
```

This is the mathematical expression of:

> the obstruction exists, but only one observer-order deeper than the leading
> finite-access differential.

### Step E: Take associated graded

Since `D` preserves filtration and curvature is subleading:

```tex
\bar D^2 = 0.
```

Therefore observer-bounded cohomology is ordinary cohomology of the leading
observer-accessible symbol complex.

### Step F: Interpret `T=0`

The universal construction is not claiming:

> finite LLM prompt = finite human cognition = finite FRW cosmology.

It is claiming:

> each has an observer-access boundary; after passing to the associated graded,
> the leading obstruction/scaling content is classified by the vanishing order
> of `Omega_O`.

This is the rebuttal-safe unification.

## Rebuttal-Safe One Paragraph

Use this if space is tight:

> The cohomology construction is made on the punctured finite-access family
> `Omega_O > 0` and then passed to the associated graded as `Omega_O -> 0`.
> The strict boundary is not an operational stage. The missing lemma is the
> standard filtered-curved-complex compatibility condition: `D(F^kC) subset
> F^kC` and `[kappa_O,F^kC] subset F^{k+1}C`, where `kappa_O` is the bundle
> curvature, not the scalar access cost. Then `D` induces `bar D` on
> `gr^kC`, and `bar D^2[omega]=[[kappa_O,omega]]=0` in `F^kC/F^{k+1}C`.
> Thus observer-bounded cohomology is well-defined as the leading
> observer-accessible boundary cohomology.

## Minimal Edit Ranking

If you can only do three edits:

1. Add Patch 4 and Patch 5: adapted filtration plus square-zero lemma.
2. Replace the risky Definition 5 proof sentence with a lemma citation.
3. Replace the false `omega = O(Omega^k)` line in the strict theorem.

If you can do five edits:

4. Add the punctured finite-access convention.
5. Split bundle curvature from scalar access cost.

If you can do polish:

6. Fix Rayleigh wording.
7. Add smoothness/asymptotic-germ scope.
8. Specify total degree.

## What Not To Defend

Do not defend these as written:

1. A nonzero lambda-independent cochain is `O(Omega^k)` for all positive `k`.
2. Vanishing of a de Rham curvature class automatically gives a global
   nonabelian flattening shift without extra hypotheses.
3. The access functor is globally smooth through all eigenvalue crossings.
4. A divergent scalar access cost is the same object as the curvature bracket
   that must vanish on the associated graded.

Each can be repaired with scope language or hypotheses. None is needed for the
main AGI-paper claim if the cohomology construction is presented as the
associated-graded boundary object.

## Final Position

The best version of the proof is not a full rewrite. It is a controlled
amendment:

- Work on `Omega_O > 0`.
- Treat `Omega_O=0` as the boundary, not a stage.
- Add adapted filtration.
- Prove `bar D^2=0` on `gr`.
- Stop overclaiming the strict `r_min=0` equivalence.

That gets the companion to a defensible mathematical core while preserving the
paper's intended unification.

