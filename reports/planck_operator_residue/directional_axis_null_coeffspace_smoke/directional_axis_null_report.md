# Directional Axis Coefficient-Space Null

Status: first simulation-level control for the corrected ell=2/ell=3
m=ell-maximizing directional statistic.

## Question

Under an isotropic common low-ell sky plus independent operator noise
calibrated from the observed coefficient distances, how often do the
observed Q-O alignment, operator-axis clustering, and mask-state shift
occur?

## Calibration

| condition | ell=2 C_noise/C_sky | ell=3 C_noise/C_sky |
| --- | ---: | ---: |
| unmasked | 0.0736954 | 0.0122903 |
| galcut20 | 0.00267331 | 0.0134281 |

## Tail Fractions

| condition | metric | observed | null median | 5-95% null | tail |
| --- | --- | ---: | ---: | ---: | ---: |
| unmasked | `qo_median_deg` | 11.9 | 60.75 | 25.96-81.82 | 0 |
| unmasked | `ell2_operator_dispersion_deg` | 14.13 | 24.12 | 12.97-64.95 | 0.2 |
| unmasked | `ell3_operator_dispersion_deg` | 3.343 | 8.888 | 3.565-21.43 | 0 |
| unmasked | `ell2_pair_residue_dispersion_deg` | 80.9 | 58.49 | 36.59-70.64 | 0 |
| unmasked | `ell3_pair_residue_dispersion_deg` | 33.17 | 53.83 | 33.11-67.1 | 0.95 |
| galcut20 | `qo_median_deg` | 29.5 | 61.73 | 17.31-81.4 | 0.15 |
| galcut20 | `ell2_operator_dispersion_deg` | 4.615 | 3.716 | 1.671-9.271 | 0.6 |
| galcut20 | `ell3_operator_dispersion_deg` | 5.112 | 10.36 | 3.427-27.13 | 0.2 |
| galcut20 | `ell2_pair_residue_dispersion_deg` | 58.44 | 58.17 | 40.46-67.99 | 0.5 |
| galcut20 | `ell3_pair_residue_dispersion_deg` | 55.62 | 55.68 | 27.61-65.63 | 0.5 |

Mask-state Q-O delta:

```text
observed galcut20 - unmasked = 17.6 deg
null median = 0.2803 deg
null 5-95% = -13.61 to 9.827 deg
fraction null >= observed = 0
```

## Allowed Claims

1. This null quantifies how expensive the observed directional
   statistics are under an isotropic common-sky, calibrated-noise
   coefficient model.
2. A low tail fraction means the measured statistic is atypical under
   this specific null, not under every standard cosmology control.
3. The mask-state delta is tested only against a no-mode-coupling
   coefficient model; it is not a replacement for a real masked-sky
   CMB simulation.

## Forbidden Claims

1. This simulation proves AOC, a false bottom, cosmic torque, or
   apparatus-bound K.
2. This simulation refutes LambdaCDM.
3. This simulation fully explains the Planck low-ell anomaly literature.
4. The galcut20 result is a complete mask likelihood analysis.

## Limitations

- No Planck component-separation machinery is simulated.
- No mask-induced mode coupling is simulated.
- The galcut20 condition shares the same synthetic sky and differs only by calibrated operator-noise level.
- The statistic is evaluated on a finite axis grid using a Fibonacci projection quadrature, matching the published pipeline approximately.

## Next Control

Replace this coefficient-space null with a masked-sky CMB null: draw
Gaussian skies from a fiducial low-ell Cl, apply the same galactic mask
or official Planck common mask, extract pseudo-alms, and rerun this
directional statistic.
