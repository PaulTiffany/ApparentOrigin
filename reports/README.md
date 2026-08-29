# Reports

Generated reports and figures live here.

Current empirical reports:

1. `reports/pantheon_plus/pantheon_k_report.md`
   - First real-data apparatus-bound `K_P` calculation using Pantheon+
     distance-modulus uncertainty as a provisional reliability proxy.
2. `reports/desi_dr2_bao/desi_dr2_bao_report.md`
   - First DESI DR2 BAO external-gate report. Current read: DESI prefers
     near-zero deformation under the current projection, so Pantheon-amplitude
     portability is rejected in this first pass.
3. `reports/planck_operator_residue/`
   - Planck operator-residue reports. Includes a synthetic example run plus the
     first real fallback run:
     `reports/planck_operator_residue/planck_operator_residue_first_contact.md`.
   - Phase-randomized coefficient null (unmasked):
     `reports/planck_operator_residue/phase_null_nside64/phase_null_report.md`.
   - Mask-aware phase null (`|b|>20°` synthetic galactic cut, `f_sky=0.6615`)
     and side-by-side comparison with the unmasked run:
     `reports/planck_operator_residue/phase_null_nside64_galcut20/phase_null_report.md`,
     `reports/planck_operator_residue/phase_null_nside64_galcut20/mask_aware_comparison.md`.
   - Directional (axial) analysis at ell=2: quadrupole tensor decomposition,
     principal axes, self-similarity readout (physical vs epistemic
     preferred axes), alignment with published low-ell anomaly directions:
     `reports/planck_operator_residue/directional_axis_comparison.md`.
   - First coefficient-space directional null for the corrected ell=2/ell=3
     m=ell-maximizing statistic:
     `reports/planck_operator_residue/directional_axis_null_coeffspace/directional_axis_null_report.md`.
   - First masked-sky geometry null for the corrected ell=2/ell=3
     m=ell-maximizing statistic:
     `reports/planck_operator_residue/directional_axis_masked_sky_null/directional_axis_masked_sky_null_report.md`.
   - High-ell leakage extension of the masked-sky geometry null:
     `reports/planck_operator_residue/directional_axis_high_ell_leakage_null/directional_axis_high_ell_leakage_null_report.md`.
   - Opticks-style color/music composition layer over the corrected ell=2/ell=3
     directional axes:
     `reports/planck_operator_residue/opticks_axis_residue_map/opticks_axis_residue_map_report.md`.
   - Opticks v2 chart with saturation = score amplitude (per-multipole
     normalized) and value held in reserve:
     `reports/planck_operator_residue/opticks_axis_residue_map_v2/opticks_axis_residue_map_v2_report.md`.
   - Sonification of the four component-separation algorithms as voices across
     the unmasked → galcut20 transition (auditory companion to the Opticks
     visual chart; honest null on "auditory reveals patterns visual doesn't"
     for this dataset):
     `reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift_report.md`.
   - Counterpoint voice-leading analysis with classical forbidden-motion rules
     adapted to spherical-axis geometry (headline: at ell=3 all six voice pairs
     trigger parallel-fifths, suggesting the four pipelines move as a single
     block under masking):
     `reports/planck_operator_residue/counterpoint_voice_leading/counterpoint_voice_leading_report.md`.
   - Synthetic galactic-cut threshold sweep for the corrected ell=2/ell=3
     directional axes:
     `reports/planck_operator_residue/directional_axis_galcut_sweep/directional_axis_galcut_sweep_report.md`.
   - Isotropic low-ell null for the galcut threshold-sweep cliff statistic:
     `reports/planck_operator_residue/directional_axis_galcut_sweep_null/directional_axis_galcut_sweep_null_report.md`.
   - Fine synthetic-cut sweep evaluating P1 from the frozen threshold
     prediction contract:
     `reports/planck_operator_residue/directional_axis_galcut_fine_sweep/p1_prediction_evaluation.md`.
   - High-ell leakage threshold-sweep null evaluating P2 from the frozen
     prediction contract:
     `reports/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null/directional_axis_galcut_sweep_high_ell_null_report.md`.
   - Official Planck common-mask morphology sweep evaluating first-pass P3:
     `reports/planck_operator_residue/directional_axis_official_mask_morphology/directional_axis_official_mask_morphology_report.md`.
   - Sprint D voice-leading sim-null calibrating the Episode 2 parallel-fifths
     block-motion finding against ΛCDM cosmic variance with a noise-scale
     sensitivity sweep (headline: observed 6/6-pair pattern at ell=3 under
     galcut20 sits at the 98.6-100.0 percentile of the null across noise scales
     0.5x/1.0x/2.0x; mask geometry alone produces ~7× more lockstep events
     than the noise-only baseline at noise=0.5x):
     `reports/planck_operator_residue/voice_leading_sim_null/voice_leading_sim_null_report.md`.
   - Per-operator octave-pair duet sonification (Sprint C-prime; auditory
     companion to Sprint D, isolating per-pipeline cross-octave Q-O detuning
     that the Episode 2 8-voice voicing obscured):
     `reports/planck_operator_residue/sonification_octave_pair_duets/sonification_octave_pair_duets_report.md`.
   - λ_K Planck operator-prism contract gate (Episode 4 TTCS contract; live
     PASS via GitHub Actions Linux compute, 2026-04-30; verdict
     `contract_success_if_inputs_were_predeclared`,
     `C_axis(base) = 0.281`, `C_axis(dilate1) = 0.426`):
     `reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md`.
   - Sprint F1 D_iso first-principles calibration (n=4 axial-median
     reference is 60 deg; the gate's hardcoded 57 deg is honored because
     it was predeclared, but future contracts should cite this calibration):
     `reports/planck_operator_residue/d_iso_calibration/d_iso_calibration_report.md`.
   - Sprint F2 C_axis null baseline using Sprint D surrogate scaffolding;
     reveals that the C_axis > 0 condition is trivially satisfied under
     a shared-sky-plus-noise cartoon, with the live values sitting below
     the surrogate bulk; names the proper official-mask null as the
     frozen open question that closes Episode 4:
     `reports/planck_operator_residue/operator_prism_c_axis_null/operator_prism_c_axis_null_report.md`.

Current prediction contracts:

1. `docs/planck_directional_threshold_prediction_contract.md`
   - Frozen next-run predictions for fine-cut localization, high-ell leakage
     threshold nulls, and official-mask specificity after the Planck galcut
     recomposition cliff.
2. `docs/planck_p3_official_mask_contract.md`
   - Frozen official-mask product and first morphology family for P3.
3. `docs/lambda_k_planck_operator_prism_contract.md`
   - Episode 4 TTCS candidate map. Predeclared sign condition
     `C_axis(ell=3, official-mask-base) > 0` and survival under
     `dilate1`. Live PASS via GitHub Actions Linux compute, 2026-04-30.
     See the gate report and Sprint F1/F2 audits for the reading
     discipline.
