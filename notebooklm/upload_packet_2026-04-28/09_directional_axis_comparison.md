# Planck Operator-Residue Directional Comparison

Status: directional analysis at ell=2 of the operator-residue handle.
Compares unmasked nside64 alms with the galcut20 (`|b|>20°`) variant.
Tests the *axial* feature of the gestural conjecture under a self-
similarity reading: physical and epistemic manifolds at large scale
should share preferred-axis structure if the conjecture's bounded-
observer framing holds.

Phase tag: near-cousin-phase. Does not commit the conjecture to Kerr
or any specific physical realization.

## Headline numbers

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| operator-axis median pairwise dispersion (deg) | 41.3 | **1.6** |
| pair-residue-axis median pairwise dispersion (deg) | 81.2 | 43.6 |
| operator-axis median anisotropy | 0.45 | 0.31 |
| pair-residue-axis median anisotropy | 0.39 | 0.40 |

Reference: for axes uniformly distributed on the sphere modulo sign,
expected median pairwise separation is ~57°.

## Operator quadrupole axes

Each operator's own ell=2 sky pattern.

**Unmasked:**

| operator | l (deg) | b (deg) |
| --- | ---: | ---: |
| Commander | 332.3 | 2.7 |
| NILC      | 334.9 | 2.5 |
| SEVEM     | 55.0  | 23.7 |
| SMICA     | 334.0 | 2.8 |

Pattern: Commander/NILC/SMICA converge near `(l≈334°, b≈3°)`; SEVEM
sits at `(l=55°, b=24°)` ~80° away. Same SEVEM-as-outlier pattern that
appeared in the operator-residue distance metric: SEVEM diverges from
the others in the galactic plane, where its template-fitting method
behaves differently.

**Galcut20:**

| operator | l (deg) | b (deg) |
| --- | ---: | ---: |
| Commander | 68.0 | 59.5 |
| NILC      | 69.2 | 57.1 |
| SEVEM     | 66.9 | 57.8 |
| SMICA     | 69.7 | 58.1 |

All four operators converge to `(l≈68°, b≈58°)` within 1.6° of each
other. SEVEM joins the cluster once the galactic plane is removed.

**This is the strongest finding.** On the clean sky, the four
component-separation pipelines independently reconstruct the same
quadrupole axis to within 1.6°. The physical manifold (the sky's
quadrupole orientation as it appears to each pipeline) is pipeline-
robust at this level, much tighter than the ~4% per-coefficient noise
floor would naively suggest for direction.

The clean-sky operator axis at `(68°, 58°)` is **not** aligned with
published low-ell anomaly directions:

| reference | offset from operator axis (deg) |
| --- | ---: |
| axis-of-evil (LM2005, 260°, 60°) | ~62 |
| quadrupole-octupole alignment (S2004, 250°, 65°) | ~57 |
| CMB cold spot (210°, -57°) | ~20 |
| CMB kinematic dipole (264°, 48°) | ~74 |

The operators agree on a quadrupole axis that is *not* the axis-of-evil
direction.

## Pair-residue quadrupole axes

The epistemic manifold: direction in which two operators systematically
differ at ell=2.

**Unmasked:**

| pair | l (deg) | b (deg) | offset from AoE-LM2005 |
| --- | ---: | ---: | ---: |
| Commander-NILC  | 83.7  | 8.1  | 68.2° |
| Commander-SEVEM | 2.2   | 1.2  | 85.0° |
| Commander-SMICA | 80.2  | 8.3  | 68.3° |
| NILC-SEVEM      | 179.9 | 0.4  | 84.7° |
| NILC-SMICA      | 221.3 | 78.8 | **22.3°** |
| SEVEM-SMICA     | 359.1 | 0.9  | 86.2° |

**Galcut20:**

| pair | l (deg) | b (deg) | offset from AoE-LM2005 |
| --- | ---: | ---: | ---: |
| Commander-NILC  | 246.7 | 56.5 | **7.8°** |
| Commander-SEVEM | 164.8 | 84.6 | 30.9° |
| Commander-SMICA | 99.2  | 31.2 | 87.4° |
| NILC-SEVEM      | 98.4  | 44.4 | 74.5° |
| NILC-SMICA      | 232.2 | 54.4 | **15.9°** |
| SEVEM-SMICA     | 106.6 | 53.9 | 64.1° |

Pattern in the masked variant: two of six pair residues sit within 16°
of the published axis-of-evil direction. Both pairs involve NILC
(Commander-NILC at 7.8°, NILC-SMICA at 15.9°). The other four pairs
are dispersed.

Suggestive, but not significant under a look-elsewhere correction:
probability that any 2 of 6 axes uniformly distributed mod-sign land
within 16° of a fixed reference is ~2%. With multiple reference
directions tried (4 here) and pipeline-pair structure (NILC anchoring
both close pairs), this drops below interesting. **The pattern is
worth flagging, not concluding.**

## Self-similarity readout

The conjecture's self-similarity claim, read locally at ell=2:
*physical preferred axis (operators' quadrupole) and epistemic
preferred axis (pair residues) should share structure*.

Galcut20 result:

- Physical axis: well-determined, four pipelines agree to 1.6° at
  `(68°, 58°)`.
- Epistemic axes: dispersed (median 43.6°), no coherent direction
  shared across all six pairs. The two NILC-involving pairs cluster
  near `(240°, 55°)` (axis-of-evil-adjacent); the other four are
  scattered.
- Operator-axis-vs-residual-axis offsets: typically large (40-90°
  range, see operator_vs_residue_deg in the JSON).

Reading: at ell=2 in this realization, the physical and epistemic
preferred axes do not coherently align. Self-similarity between the
two manifolds, in this specific test, is **not supported**.

Caveats that prevent calling this a refutation:

1. Cosmic variance at ell=2 is enormous (5 modes, one realization).
2. Residual power is ~0.08% of CMB signal variance — small enough
   that the residual axis may be dominated by sub-leading structure
   that does not track the physical axis even if a deeper axial
   feature exists.
3. The fallback extractor (astropy direct quadrature) is not the
   canonical `healpy.map2alm` pipeline. Quantitative axis values may
   shift slightly under canonical extraction.
4. ell=2 alone is one multipole. The full self-similarity check needs
   ell=3 (octupole, where the quadrupole-octupole alignment lives) and
   ideally cross-multipole structure.

## Allowed claims

1. On the galactic-plane-cut sky (`|b|>20°`, `f_sky=0.66`), the four
   Planck PR3 component-separation operators independently
   reconstruct the same ell=2 quadrupole axis to within 1.6° of each
   other at galactic `(68°, 58°)`.
2. The operator-axis convergence is much tighter than under the
   unmasked extraction (41° dispersion), driven by SEVEM joining the
   cluster once the galactic plane is removed.
3. The clean-sky operator axis is not within ~30° of the published
   axis-of-evil direction.
4. The pair-residue axes are dispersed (median 43.6° pairwise
   separation) and do not share a coherent preferred direction.
5. Two of six pair residues (both involving NILC) sit within 16° of
   the published axis-of-evil direction; this is suggestive but not
   significant under a look-elsewhere correction.
6. At ell=2, the test for self-similarity between physical (operator
   axis) and epistemic (pair-residue axis) manifolds returns no
   coherent alignment in this single-realization measurement.

## Forbidden claims

1. AOC is confirmed by the operator axis alignment at `(68°, 58°)`.
2. LambdaCDM is refuted.
3. The two-NILC-pair proximity to the axis of evil is statistical
   evidence for cosmological axiality.
4. Self-similarity between physical and epistemic manifolds is
   demonstrated or refuted by a single-realization ell=2 measurement.
5. The result confirms or rules out rotating-interior cosmology, the
   Kerr-cousin geometry, or any other specific bounded-observer
   physical realization.
6. The 1.6° operator convergence is independent confirmation of the
   sky's intrinsic quadrupole orientation; that orientation is a
   reconstruction product, not direct observation.

## Phase tag

Near-cousin-phase test of an axial feature of the gestural conjecture.
Result is data; interpretation requires sim-level controls (CMB-only
realizations through pipeline-equivalent reconstructions) and theory-
derived predictions of magnitude and direction. The strongest single
finding (clean-sky operator-axis convergence to 1.6°) is informative
about the operator-residue framework, not about AOC's truth.

## Next directional moves

1. **ell=3 (octupole) directional analysis.** The published
   quadrupole-octupole alignment lives in the joint structure of
   ell=2 and ell=3; a full self-similarity test needs both. The
   tensor decomposition for ell=3 is rank-3 and more involved; can be
   done via Wigner-D rotation maximization of the m=±3 mode.
2. **Simulation-level null on directional statistic.** Generate
   CMB-only ell=2 realizations from a fiducial Cl, propagate through
   pipeline-equivalent reconstructions with calibrated noise, compute
   operator-axis convergence and pair-residue-axis dispersion. Ask
   whether the observed 1.6° convergence is typical or atypical under
   the null.
3. **Theory-derived axis prediction.** Derive what the apparatus-bound
   K parameter under a near-cousin geometry predicts for the magnitude
   and direction of operator-axis offset from naive ΛCDM. If the
   prediction is concrete, this becomes a falsifiable test rather than
   a coincidence check.

## Octupole (ell=3) directional analysis and methodology correction

Subsequent analysis added the octupole (`ell=3`) m=ℓ-maximizing axis
search and re-did the quadrupole (`ell=2`) analysis with the same
m=ℓ-maximizing methodology, because the original ell=2 used the
tensor-largest-`|eigenvalue|` eigenvector which can flip ~90° depending
on whether the dominant eigenvalue is positive or negative. The
correction matters: in the unmasked case, three of four operators
had largest-|eigenvalue| negative, so the original axis pointed at
the *suppression* direction rather than the *enhancement* direction.
The corrected m=ℓ-max methodology is what the axis-of-evil /
quadrupole-octupole-alignment literature uses.

Scripts:

```text
empirical/planck_operator_residue/directional_residue_axis_octupole.py
empirical/planck_operator_residue/directional_residue_axis_quadrupole_mlmax.py
```

### Operator axes under m=ℓ-max methodology

**Unmasked nside64:**

| operator | ell=2 axis (l, b) | ell=3 axis (l, b) | Q-O angle |
| --- | ---: | ---: | ---: |
| Commander | (237.6, 47.5) | (242.7, 64.8) | 17.5° |
| NILC      | (242.7, 57.4) | (237.6, 62.3) | 5.6° |
| SEVEM     | (207.3, 64.8) | (247.8, 67.2) | 16.3° |
| SMICA     | (237.6, 54.9) | (237.6, 62.3) | 7.4° |

**Median Q-O alignment angle: 11.9°.**

Operator-axis dispersion at ell=2: 14.1°. At ell=3: 3.3°.

**Galcut20 nside64:**

| operator | ell=2 axis (l, b) | ell=3 axis (l, b) | Q-O angle |
| --- | ---: | ---: | ---: |
| Commander | (257.9, 30.2) | (283.2, 54.9) | 30.6° |
| NILC      | (262.9, 32.6) | (283.2, 57.4) | 28.3° |
| SEVEM     | (252.8, 32.6) | (293.3, 52.4) | 35.1° |
| SMICA     | (257.9, 32.6) | (278.1, 54.9) | 26.4° |

**Median Q-O alignment angle: 29.5°.**

Operator-axis dispersion at ell=2: 4.6°. At ell=3: 5.1°.

### Reproduction of published anomaly directions (Commander, unmasked)

| reference | offset from ell=2 axis | offset from ell=3 axis |
| --- | ---: | ---: |
| axis-of-evil (LM2005, 260°, 60°)    | 18.0° | 9.3° |
| quad-oct align (S2004, 250°, 65°)   | 18.7° | 3.1° |
| CMB cold spot (210°, -57°)          | 73.0° | 55.7° |
| CMB kinematic dipole (264°, 48°)    | 17.6° | 20.3° |

The ell=3 axis lands within 3° of the Schwarz et al. 2004
quadrupole-octupole alignment direction and within 9° of the Land &
Magueijo 2005 axis of evil direction. **The published anomaly is in
our data**, reproduced with consistent methodology, with the ell=2 and
ell=3 axes aligned at median 11.9° in the unmasked case — comfortably
within the published 5-15° alignment range.

### What masking does

Cutting the galactic plane at `|b|>20°` (`f_sky=0.66`) shifts both
axes and *increases* the Q-O alignment angle from ~12° to ~30°. In
other words: the published axis-of-evil / Q-O alignment is at least
partly driven by galactic-plane structure that the unmasked extraction
includes. When we exclude the plane, the clean-sky axes drift farther
apart.

This is consistent with the contested status of the axis-of-evil claim
in mainstream cosmology — multiple papers have argued that proper
masking and foreground treatment weakens the apparent alignment.

### Pair-residual axes at ell=3

| pair | ell=3 axis (l, b) (unmasked) | ell=3 axis (l, b) (galcut20) |
| --- | ---: | ---: |
| Commander-NILC  | (242.7, 27.7) | (197.2, 17.8) |
| Commander-SEVEM | (86.0,  5.4)  | (283.2, 0.5) |
| Commander-SMICA | (247.8, 20.3) | (35.4, 7.9) |
| NILC-SEVEM      | (80.9,  0.5)  | (298.3, 5.4) |
| NILC-SMICA      | (288.2, 45.0) | (207.3, 0.5) |
| SEVEM-SMICA     | (262.9,  0.5) | (262.9, 0.5) |

Pair-residual axis dispersion at ell=3: unmasked 33.2°, galcut20 55.6°.

The pair-residual axes do not coherently cluster at ell=3 in either
mask state. The self-similarity test (physical operator axis vs
epistemic pair-residual axis) does not show alignment at either ell=2
or ell=3 in this measurement.

### Updated allowed claims

1. With consistent m=ℓ-maximizing methodology, the four Planck PR3
   operators reproduce the published axis-of-evil and
   quadrupole-octupole alignment directions in the unmasked
   extraction. ell=3 axis lands within 3° of Schwarz 2004 reference
   and 9° of Land-Magueijo 2005 reference.
2. Median Q-O alignment angle is 11.9° unmasked, 29.5° galcut20. The
   alignment weakens substantially when the galactic plane is removed.
3. Operator-axis convergence is tight at ell=3 (3.3° unmasked, 5.1°
   masked), confirming the four pipelines agree on the cosmic octupole
   axis on the clean sky.
4. The pair-residual ell=3 axes do not coherently cluster, in either
   mask state, replicating the ell=2 self-similarity null result.

### Updated forbidden claims

1. AOC is confirmed by the program reproducing the published
   axis-of-evil / Q-O alignment. Reproducing a known phenomenon with
   the correct methodology is not evidence for AOC; it is methodological
   validation that the operator-residue framework is reading the data
   correctly.
2. The masking-weakens-alignment finding refutes the axis-of-evil claim.
   It is consistent with one common reading of the published literature
   (alignment is partly foreground-driven) but does not refute either
   the published claim or its alternatives.
3. The reproduction of published anomaly directions implies AOC's
   apparatus-bound K is responsible for them. The reproduction is at
   the operator level (four pipelines agree), not at a level that
   distinguishes AOC from any other observer-bounded reconstruction
   framework.

### Phase tag (octupole and methodology correction)

Near-cousin-phase test of axial features at ell=2 and ell=3 with
consistent m=ℓ-maximizing methodology. The published axis-of-evil /
QO-alignment phenomenon is reproduced in the unmasked extraction;
masking weakens it. Self-similarity at the operator level (physical
vs epistemic preferred axes) is not supported in either mask state at
ell=2 or ell=3 in this single-realization measurement.

## Provenance

```text
empirical/planck_operator_residue/directional_residue_axis.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64

empirical/planck_operator_residue/directional_residue_axis.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64_galcut20

empirical/planck_operator_residue/directional_residue_axis_octupole.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64

empirical/planck_operator_residue/directional_residue_axis_octupole.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64_galcut20

empirical/planck_operator_residue/directional_residue_axis_quadrupole_mlmax.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64

empirical/planck_operator_residue/directional_residue_axis_quadrupole_mlmax.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
  --outdir reports/planck_operator_residue/directional_axis_nside64_galcut20
```

Per-input details (full alignment tables, anisotropy values, eigenvalues):

- `reports/planck_operator_residue/directional_axis_nside64/directional_residue_axis_report.md`
- `reports/planck_operator_residue/directional_axis_nside64/directional_residue_axis_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_residue_axis_report.md`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_residue_axis_summary.json`
