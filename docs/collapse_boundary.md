# Collapse Boundary

Status: canonical repair note for Come Cosmology PR #7.

The word **collapse** is reserved for an exceptional boundary event. It is **not** the name of every ordinary transition from one realized present to the next.

Canonical sentence:

> Collapse occurs when the current state chart can no longer carry the process by a bounded local transition or by its declared Markov state.

This gives two operational failure modes.

## 1. Ordinary evolution

Let `N_t` be the realized present in a valid chart and let

```tex
F_t:(N_t,D_t)\mapsto N_{t+1}
```

be the ordinary realized update generated from the simultaneous in-game direction bundle

```tex
D_t=(d_1(t),\ldots,d_n(t)).
```

As long as the current chart remains valid, evolution is ordinary realization:

```tex
N_{t+1}=F_t(N_t,D_t).
```

Do **not** call this collapse merely because many observers contributed to the result.

Ouija emergence names distributed authorship of the ordinary update. Collapse names failure of the current regime to continue carrying that update.

## 2. Lipschitz-safe regime

Let `d_X` measure perturbation in the current state/direction chart and let `d_Y` measure realized displacement in the resulting chart.

A locally controlled transition satisfies, on a declared neighborhood,

```tex
d_Y(F_t(x),F_t(y))
\le
L_t\,d_X(x,y)
```

for finite admissible `L_t`.

The precise metric and admissible bound must be declared for the domain. The cosmology does not assume one universal physical metric for political, biological, informational, astronomical, or other state spaces.

### Lipschitz breach

A **Lipschitz breach** occurs when a perturbation that is small in the current chart produces a displacement that cannot be bounded by the chart's declared local response scale:

```tex
\frac{d_Y(F_t(x),F_t(y))}{d_X(x,y)}
> L_{\max}
```

or becomes singular/undefined in the chart limit.

The interpretation is not that fundamental physics must be discontinuous. The claim is that the **current effective state representation has reached a regime boundary**.

A small local event can therefore trigger a macroscopically different effective state.

## 3. Markov-safe regime

Let `H_t` denote information prior to the declared current state `N_t`.

A state representation is Markov-sufficient for the modeled process when

```tex
P(N_{t+1}\mid N_t,H_t,D_t)
=
P(N_{t+1}\mid N_t,D_t)
```

within the declared tolerance.

The point is operational sufficiency: the present chart contains the state needed to propagate the model without silently consulting omitted history or latent state.

### Markov breach

A **Markov breach** occurs when the declared present ceases to be sufficient:

```tex
P(N_{t+1}\mid N_t,H_t,D_t)
\ne
P(N_{t+1}\mid N_t,D_t).
```

Then either:

1. relevant state has been omitted from `N_t`;
2. the effective process has acquired history dependence;
3. the system crossed into a new regime for which the old state variables no longer form a sufficient chart.

A Markov breach therefore requires recharting before ordinary propagation resumes.

## 4. Collapse

Define the collapse indicator schematically as

```tex
\chi_t
:=
\mathbf 1[
\text{Lipschitz breach}
\;\lor\;
\text{Markov breach}
].
```

Then:

```tex
\chi_t=0
\quad\Rightarrow\quad
N_{t+1}=F_t(N_t,D_t),
```

while

```tex
\chi_t=1
\quad\Rightarrow\quad
\text{COLLAPSE / RECHART / RESTART}.
```

A collapse is therefore a boundary in the validity of the current process description.

It does not mean that reality disappears. It means the prior chart can no longer honestly claim to describe the continuation.

## 5. Country example

A country can evolve through millions of ordinary local changes without ceasing to be represented as the same political state.

Suppose an enemy captures the capital.

The directly changed physical region may be small relative to the country's territory. Yet, under a political-state metric, the event may abruptly change:

- command authority;
- legal continuity;
- military coordination;
- diplomatic recognition;
- succession rules;
- effective sovereignty.

Thus a locally concentrated event can produce a macroscopically different effective state.

If the old chart treated territorial displacement as the relevant local metric but did not encode the capital's control role, the event appears as a Lipschitz breach.

If the old Markov state omitted latent dependencies needed to determine whether the state survives after the capital falls, it is also a Markov breach.

The correct scientific response is not to insist that the old country-state map remains smooth. It is to declare the breach and rechart the process.

## 6. Four Color correspondence

This matches the restart/void discipline of the Four Color game.

Within a valid regime, play continues by legal local moves.

When continuation would require violating the invariant or when the current state description no longer licenses a legal continuation, do not silently patch through the boundary.

The options are:

```text
continue
restart under a valid chart
or end/void the current run.
```

Collapse is therefore not an invitation to hallucinate the next regime. It is a receipt that the current one ended.

## 7. Cosmological correspondence

The same distinction applies to Apparent-Origin Cosmology.

An apparent cosmological boundary may occur where a present reconstruction chart becomes unable to propagate distinctions smoothly or Markov-sufficiently into deeper reconstruction.

The empirical question is then not simply:

```text
Where did reality begin?
```

but:

```text
Where does this observer/reconstruction chart breach, and what survives after a declared rechart?
```

If different valid observer charts breach at different apparent depths while compatible invariants survive their overlaps, that is evidence about reconstruction boundaries.

If all valid charts converge on a common boundary under increasingly strong access and controls, the burden for treating that boundary as more than observer-relative becomes stronger.

## 8. Repair to Come Cosmology

The current shorthand

```tex
N_{t+1}
=\operatorname{Collapse}_{K_t}(N_t,D_t)
```

should be replaced in the main theory note by the two-stage rule:

```tex
N_{t+1}=F_t(N_t,D_t)
\qquad\text{while the chart is valid},
```

and

```tex
\text{Lipschitz breach}\lor\text{Markov breach}
\quad\Rightarrow\quad
\text{collapse / rechart / restart}.
```

This repair keeps **Ouija emergence** as the distributed-ownership rule for ordinary realization while reserving **collapse** for genuine process-boundary events.

## 9. Canonical statements

> Ouija emergence describes who authors the move; collapse describes when the current game can no longer carry it.

> Collapse is a Lipschitz or Markov breach of the current chart.

> Collapse ends a regime, not reality.

> After collapse: rechart, restart, or stop. Do not smuggle continuity across the breach.