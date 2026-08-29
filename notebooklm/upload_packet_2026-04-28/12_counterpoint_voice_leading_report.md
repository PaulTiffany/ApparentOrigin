# Counterpoint Voice-Leading Analysis

Status: composition/methodology import artifact, not new evidence.

Treats the four Planck PR3 component-separation algorithms (Commander,
NILC, SEVEM, SMICA) as four contrapuntal voices, the unmasked vs
galcut20 mask-state pair as a two-chord progression, and per-voice
axis motion as voice-leading on the celestial sphere. Classical-
counterpoint forbidden-motion rules (parallel fifths, voice crossing,
hidden unison) are adapted to spherical-axis geometry and applied as
diagnostics. The mappings are first-pass.

Phase tag: methodology import / near-cousin layer. The framework
license is the AOC primitive that geometricity originates from
observer measurement: counterpoint is centuries of crystallized
observer-discipline against shared-source artefacts masquerading as
independent agreement. The same structural worry applies to four
pipelines reading the same sky.

## Conversion Contract

| source quantity | music-theoretic feature | preserved | discarded |
| --- | --- | --- | --- |
| component-separation algorithm | voice (one of four) | identity, comparability across mask states | timbral / harmonic content |
| operator axis (l, b) at fixed ell, mask state | pitch position in a chord | direction on the sphere, voice-pair separations | absolute physical magnitude (a_lm power) |
| (unmasked, galcut20) pair at fixed ell | two-chord progression | mask-state-induced motion per voice | temporal duration / rhythm |
| arccos(|<u_unmasked, u_galcut>|) per voice | melodic interval (Δ) | spherical voice-leading distance | scalar sign / handedness |
| u_unmasked × u_galcut (sign-oriented) | direction of motion in the harmonic plane | rotation axis of the voice on the sphere | pre-image curvature off the great-circle path |

## Forbidden-Motion Rules (spherical adaptation)

- **Parallel-fifths analog.** Two voices V_a, V_b with similar Δ magnitudes (within 5°) AND rotation axes aligned within 15°, both moving > 3°. Reading: shared foreground signal pushing both voices the same way under masking, not independent recoveries. (~75-85% confident this is the right structural map for the parallel-fifths prohibition; the deepest classical-counterpoint worry was "two voices stop being independent voices".)
- **Voice crossing.** V_a's self-motion (unmasked -> galcut20) exceeds the unmasked separation between V_a and V_b, i.e., V_a's path passes through V_b's starting pitch. Reading: differential foreground sensitivity reordering the voices. (~70-80% confident on the structural map; classical voice-crossing concerns clarity of part-recovery, here it concerns pipeline-distinguishability under the mask transformation.)
- **Hidden unison.** Two voices arrive within 5° at galcut20 having started >15° apart in unmasked. Reading: mask-induced artificial coherence (an apparent agreement created by the cut, not by the underlying sky). (~80% confident; the mapping is fairly direct since the classical "hidden" qualifier is exactly about a coincident arrival from divergent prior positions.)

Threshold choices are first-pass and conservative. They are not
p-values; they are rule cutoffs. (~60% confident the specific numeric
values would survive a calibration sweep against simulation-level
voice-leading from CMB-only realizations; the rules themselves are
more confident than the numbers attached to them.)

## Voice-Leading Distance Matrix

Δ_V,ell = arccos(|<u_V_unmasked,ell, u_V_galcut20,ell>|), in degrees.

| voice | Δ at ell=2 (deg) | Δ at ell=3 (deg) |
| --- | ---: | ---: |
| Commander | 23.26 | 22.10 |
| NILC | 28.32 | 22.89 |
| SEVEM | 42.32 | 26.35 |
| SMICA | 26.40 | 21.92 |

Per-multipole summary: ell=2 median Δ = 27.36° (max 42.32°); ell=3 median Δ = 22.49° (max 26.35°).

## Forbidden-Motion Findings

| rule | ell | triggers |
| --- | --- | --- |
| parallel_fifths | ell=2 | Commander-SMICA (Δ=23.3/26.4°, rot-axis sep=9.8°); NILC-SMICA (Δ=28.3/26.4°, rot-axis sep=3.9°) |
| parallel_fifths | ell=3 | Commander-NILC (Δ=22.1/22.9°, rot-axis sep=11.4°); Commander-SEVEM (Δ=22.1/26.3°, rot-axis sep=2.8°); Commander-SMICA (Δ=22.1/21.9°, rot-axis sep=3.1°); NILC-SEVEM (Δ=22.9/26.3°, rot-axis sep=11.7°); NILC-SMICA (Δ=22.9/21.9°, rot-axis sep=9.5°); SEVEM-SMICA (Δ=26.3/21.9°, rot-axis sep=5.5°) |
| voice_crossing | ell=2 | Commander through NILC (motion=23.3°, start-sep=10.4°); NILC through Commander (motion=28.3°, start-sep=10.4°); SEVEM through Commander (motion=42.3°, start-sep=23.8°); Commander through SMICA (motion=23.3°, start-sep=7.4°); SMICA through Commander (motion=26.4°, start-sep=7.4°); NILC through SEVEM (motion=28.3°, start-sep=18.3°); SEVEM through NILC (motion=42.3°, start-sep=18.3°); NILC through SMICA (motion=28.3°, start-sep=3.7°); SMICA through NILC (motion=26.4°, start-sep=3.7°); SEVEM through SMICA (motion=42.3°, start-sep=17.9°); SMICA through SEVEM (motion=26.4°, start-sep=17.9°) |
| voice_crossing | ell=3 | Commander through NILC (motion=22.1°, start-sep=3.3°); NILC through Commander (motion=22.9°, start-sep=3.3°); Commander through SEVEM (motion=22.1°, start-sep=3.2°); SEVEM through Commander (motion=26.3°, start-sep=3.2°); Commander through SMICA (motion=22.1°, start-sep=3.3°); SMICA through Commander (motion=21.9°, start-sep=3.3°); NILC through SEVEM (motion=22.9°, start-sep=6.5°); SEVEM through NILC (motion=26.3°, start-sep=6.5°); NILC through SMICA (motion=22.9°, start-sep=0.0°); SMICA through NILC (motion=21.9°, start-sep=0.0°); SEVEM through SMICA (motion=26.3°, start-sep=6.5°); SMICA through SEVEM (motion=21.9°, start-sep=6.5°) |
| hidden_unison | ell=2 | Commander-SEVEM (23.8° → 5.0°); SEVEM-SMICA (17.9° → 4.3°) |
| hidden_unison | ell=3 | none |

Total counts: parallel_fifths=8, voice_crossing=23, hidden_unison=2.

## Readout

What the voice-leading says about the unmasked -> galcut20
transition in this single-realization measurement:

1. **All four voices move substantially.** Per-voice Δ ranges from
   23.3° to 42.3° at ell=2
   (median 27.4°) and from 21.9° to
   26.3° at ell=3 (median 22.5°). No voice is fixed
   under the cut; this is a chord progression, not a held chord.

2. **Parallel-fifths is the dominant flagged pattern at ell=3.**
   All six voice pairs trigger the parallel-fifths rule at ell=3
   (matched Δ within 5°, rotation axes aligned within 12°). The
   four voices move as one block. Read in counterpoint terms: the
   ell=3 chord progression has zero independent voice motion.
   This is consistent with a shared-foreground-driven shift acting
   on all four pipelines together at the octupole, not four
   independent recoveries that happen to converge. (~75% confident
   that the parallel-fifths rule is doing real work here, given
   the mapping is first-pass and the threshold is uncalibrated.)

3. **At ell=2 the chord is partly independent.** Only 2/6 pairs
   trigger parallel-fifths (Commander-SMICA and NILC-SMICA), and
   SEVEM is the outlier (Δ=42°, much larger than the other three
   ~24-28°). This matches the SEVEM-as-outlier pattern noted in
   the parent directional report. The ell=2 chord shows partial
   shared motion with one detectably independent voice.

4. **Voice-crossing is pervasive.** 23 crossings across both
   multipoles. At ell=3 in particular, every operator's self-
   motion (~22-26°) dwarfs the unmasked operator-pair separations
   (~0-7°), so every voice passes through every other. This says
   the 'voice ordering' visible on the unmasked sky is not
   preserved under the cut: the masking transformation is much
   larger than the pipeline-distinguishability scale at ell=3.

5. **Hidden-unison fires twice at ell=2 only.** Commander-SEVEM
   (23.8° -> 5.0°) and SEVEM-SMICA (17.9° -> 4.3°) are SEVEM-
   joining-the-cluster events: SEVEM diverges in the unmasked
   galactic plane and converges to the others under the cut. This
   is the same SEVEM-rejoining-the-cluster fact already named in
   the parent directional report, now phrased as a voice-leading
   forbidden motion. The agreement at galcut20 is mask-induced,
   not independently confirmed by SEVEM and the others.

The aggregate read: at ell=3 the four voices are not behaving as
four independent pipelines under the masking transformation; they
are moving as a single block with shared rotation-axis structure.
This is a music-theoretic restatement of the parent finding that
the galcut20 sky-cut substantially reorganizes the operator axes
and that the resulting clean-sky agreement is not pipeline-
independent verification. None of these rules is a substitute
for a calibrated null simulation; they are diagnostic readings
that point at where to put one.

## Allowed Claims

1. Treating the four Planck PR3 component-separation algorithms as
   four spherical voices, with the unmasked → galcut20 transition
   as a two-chord progression, yields a well-defined voice-leading
   distance matrix and a well-defined per-voice rotation-axis on
   the sphere.
2. The first-pass adaptations of three classical-counterpoint
   forbidden-motion rules (parallel fifths, voice crossing, hidden
   unison) to spherical voice-leading are computable and produce a
   reproducible set of pair-level diagnostics under the documented
   thresholds.
3. The diagnostics give a compact way to inspect mask-induced
   pipeline behavior, complementary to the numeric dispersion
   tables in the parent directional reports.
4. Rule-flagged motions point at structurally interesting voice
   pairs to follow up with a calibrated null simulation; rule-
   not-flagged motions do not falsify the interest of those pairs
   either.

## Forbidden Claims

1. AOC is **not** confirmed by counterpoint analysis. Reproducing
   classical voice-leading worries on the operator axes is a
   compositional reading of pre-existing data; it adds no new
   empirical evidence.
2. ΛCDM is **not** refuted by any voice-leading finding here. The
   rules diagnose pipeline behavior under masking, not the
   underlying cosmological model.
3. A parallel-fifths flag is **not** statistical evidence of
   shared foreground; it is a music-theoretic flag whose
   probability under the null has not been calibrated.
4. A no-trigger result on a rule is **not** a clean bill of health
   for pipeline independence; null-result discipline applies in
   both directions.
5. The threshold values are **not** principled physical scales;
   they are first-pass diagnostic cutoffs adapted from classical
   heuristics.
6. The voice / chord / counterpoint vocabulary is **not** a claim
   that the cosmology is musical or that the operators are
   literally sound. The framework license is the observer-
   measurement origin of geometricity, not a metaphysical music.

## Outputs

- `counterpoint_voice_leading_report.md`
- `counterpoint_voice_leading_summary.json`
- `voice_leading_score_ell2.png`
- `voice_leading_score_ell3.png`
