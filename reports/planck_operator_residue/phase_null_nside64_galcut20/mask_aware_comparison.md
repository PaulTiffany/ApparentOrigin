# Planck Operator-Residue Mask-Aware Comparison

Status: second null control on the operator-residue handle. Compares the
unmasked phase null with a galactic-plane-cut version. Coefficient-level
control, not a full CMB simulation or pseudo-Cl mode-decoupled analysis.

## Inputs

| variant | input CSV | f_sky | mask source |
| --- | --- | ---: | --- |
| unmasked | `planck_lowell_alm_fallback_nside64.csv` | 1.000 | none |
| galcut20 | `planck_lowell_alm_fallback_nside64_galcut20.csv` | 0.6615 | synthetic `|b|>20°` |

Both runs use:

```text
2 <= ell <= 30
1000 phase-randomized null seeds
seed = 20260428
nside_out = 64
extractor: extract_planck_lowell_fallback[_masked].py (astropy direct quadrature)
```

The galcut20 mask is a synthetic galactic-plane proxy, not the official
Planck PR3 common confidence mask. Its f_sky is in the same neighborhood as
the official common-Int mask (~0.78 retained) but cuts more aggressively at
the plane and ignores point-source masking.

## Headline

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| observed median pairwise distance | 0.337761 | 0.041244 |
| null median | 1.414070 | 1.414207 |
| null q05 | 1.386992 | 1.384254 |
| null q95 | 1.441485 | 1.444125 |
| fraction null <= observed | 0 / 1000 | 0 / 1000 |

Plain English: removing the galactic plane drives the observed cross-operator
distance *down* by an order of magnitude (0.338 -> 0.041), while the
phase-shuffled null distribution is essentially unchanged. The four operators
agree more tightly with each other outside the plane, not less.

## Pairwise medians

| pair | unmasked observed | galcut20 observed | unmasked null median | galcut20 null median |
| --- | ---: | ---: | ---: | ---: |
| `Commander-NILC`  | 0.273684 | 0.044765 | 1.412485 | 1.413990 |
| `Commander-SEVEM` | 0.460631 | 0.046654 | 1.413349 | 1.413252 |
| `Commander-SMICA` | 0.251256 | 0.046156 | 1.415351 | 1.416054 |
| `NILC-SEVEM`      | 0.498159 | 0.036003 | 1.414337 | 1.414956 |
| `NILC-SMICA`      | 0.092011 | 0.028941 | 1.412899 | 1.412956 |
| `SEVEM-SMICA`     | 0.482440 | 0.042264 | 1.412648 | 1.413503 |

Pattern: in the unmasked variant, every pair *involving SEVEM* sits near
0.46-0.50 while every pair *without SEVEM* sits near 0.09-0.27. Once the
galactic plane is cut, all six pairs collapse into the same ~0.03-0.05
band. This is consistent with the known behavior of SEVEM as a
template-fitting component-separation method that diverges from the others
mainly inside foreground-rich regions; outside the plane, it converges with
the rest.

## Cross-Band Split

Re-running the same null on `2 <= ell <= 10` and `11 <= ell <= 30`
separately localizes where the alignment lives.

| band | unmasked observed | galcut20 observed | unmasked frac<=obs | galcut20 frac<=obs |
| --- | ---: | ---: | ---: | ---: |
| `2 <= ell <= 10`  | 0.246507 | 0.039510 | 0/1000 | 0/1000 |
| `11 <= ell <= 30` | 0.377989 | 0.041605 | 0/1000 | 0/1000 |
| `2 <= ell <= 30`  | 0.337761 | 0.041244 | 0/1000 | 0/1000 |

Pattern:

- The **galcut20 distance is band-flat** (`0.040` low vs `0.042` high). Outside
  the plane, the operators agree equally well at the lowest multipoles and
  at the upper end of the analyzed band.
- The **unmasked distance has structure**: `0.247` at low ell vs `0.378` at
  high ell. The unmasked-residual gap concentrates at higher ell — consistent
  with point-source and small-scale galactic-foreground residuals dominating
  there.
- Cutting the plane removes the band structure. Whatever was producing the
  ell-dependent shape was geographic, not multipole-physical.

This is informative for the AOC operator-residue framing: a boundary- or
apparatus-bound signature one might naively expect at the *very* lowest
multipoles is not visible above the band-flat noise floor in this control.
The clean-sky residual looks like an IID per-coefficient noise term, not
like a low-ell-localized excess.

## Analytic Shared-Fraction Reading

For two operators with `a_i = S + N_i` where `S` is a shared cosmic
realization with per-coefficient variance `Cs` and `N_i` are independent
zero-mean noise terms with variance `Cn` (same per coefficient), the
expected coefficient distance is:

```text
distance^2 ~ 2 * Cn / (Cs + Cn) ~ 2 * (Cn / Cs)   when Cn << Cs
```

Equivalently, `Cn / Cs ~ distance^2 / 2` is the noise-to-signal variance
ratio under this null. Rough readings:

| variant | distance | implied Cn/Cs |
| --- | ---: | ---: |
| unmasked full        | 0.337761 | 5.7%  |
| unmasked low (2-10)  | 0.246507 | 3.0%  |
| unmasked high (11-30)| 0.377989 | 7.1%  |
| galcut20 full        | 0.041244 | 0.085% |
| galcut20 low (2-10)  | 0.039510 | 0.078% |
| galcut20 high (11-30)| 0.041605 | 0.087% |

In the unmasked case the implied "noise" is dominated by *foreground residue*,
not pipeline noise — and it is larger at high ell, as expected for small-scale
foregrounds. In the galcut20 case, the implied per-coefficient noise floor
sits at ~0.08% of CMB signal variance and is band-flat. That number is
consistent with published low-ell sensitivity for the four PR3
component-separation methods on the clean sky and is *not* a positive
detection of operator-bound apparatus signal.

This is an analytic baseline, not a Monte Carlo. The simulation null move
remains required to test whether the observed clean-sky distance is
inconsistent with a fully shared-CMB plus independent pipeline-noise null
at the per-pipeline noise spec.

## Interpretation

What the unmasked null established: cross-operator closeness depends on
*phase alignment*, not just per-coefficient amplitudes. The four maps share
aligned low-ell structure.

What the galcut20 null adds:

- The observed alignment is **not** a galactic-plane artifact. The galactic
  plane was *anti-aligning* the maps (especially SEVEM vs the rest). Cutting
  the plane sharpens the alignment by about an order of magnitude.
- The natural AOC-style reading: the operators agree on the cosmic sky and
  disagree on the foreground residue. This is what you would expect from
  reconstruction operators that share a target signal but apply different
  apparatus models in regions where the target is dominated by what each
  apparatus is built to suppress.
- The galcut20 result is therefore *consistent with*, but does not *prove*,
  the AOC operator-residue framing. The next clean step is a simulation-level
  null where we control the input sky.

## Allowed claims

1. Removing the galactic plane reduces the observed operator-residue distance
   by an order of magnitude while leaving the phase-randomized null
   distribution effectively unchanged.
2. The unmasked SEVEM-vs-others gap is dominated by galactic-plane
   disagreement and disappears outside the plane.
3. The four Planck PR3 component-separation operators converge to within
   ~5% of the phase-randomized null distance scale on the clean-sky band
   `2 <= ell <= 30`.

## Forbidden claims

1. This control proves AOC.
2. The operator-residue distance is a measure of cosmic torque or a false
   bottom.
3. The clean-sky alignment is independent of cosmic variance: a single
   realization of CMB-only sky run through four pipelines is expected to
   alias as "shared structure" and a coefficient-level phase null cannot
   separate that from operator-bound apparatus signal.
4. The official Planck common confidence mask would necessarily reproduce
   these numbers. The synthetic `|b|>20°` mask is a galactic proxy only.

## Next controls

1. Re-run with the official Planck PR3 common-Int confidence mask
   (`COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits`, ESA PLA route confirmed
   reachable). This adds point-source masking and the official galactic
   boundary.
2. Simulation-level null. Generate a CMB-only sky from a fiducial
   `LambdaCDM` `Cl`, propagate it through four operator-equivalent
   reconstruction pipelines, compute the operator-residue distance under
   the same band and same mask, and compare its distribution to the
   observed value. This is the loop-instrumentation move from the SRMF
   cautionary memory: only when we control the input sky can we tell whether
   the residual is operator-bound or cosmic-variance-bound.
3. Cross-band split. Re-run on `2 <= ell <= 10` and `11 <= ell <= 30`
   separately. The very low-ell band is where coefficient cosmic variance
   is largest; if the alignment is overwhelmingly low-ell driven, that
   constrains the interpretation.

## Provenance

```text
empirical/planck_operator_residue/extract_planck_lowell_fallback_masked.py
  --map-dir data/raw/planck_operator_residue/maps
  --output data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
  --manifest data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.manifest.json
  --nside-out 64 --lmax 30 --galactic-cut 20.0

empirical/planck_operator_residue/phase_null_operator_residue.py
  --input  data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
  --outdir reports/planck_operator_residue/phase_null_nside64_galcut20
  --ell-min 2 --ell-max 30 --seeds 1000 --seed 20260428
```
