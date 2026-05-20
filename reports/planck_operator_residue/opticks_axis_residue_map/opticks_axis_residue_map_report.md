# Opticks Axis-Residue Map

Status: composition/media instrumentation artifact, not evidence.

This artifact converts the already-computed Planck low-ell directional
operator axes into an Opticks-style color and sevenfold-note chart. The
goal is to make the mask-state recomposition visually inspectable while
keeping the empirical contract fixed.

## Conversion Contract

| source quantity | conversion | preserved | discarded |
| --- | --- | --- | --- |
| galactic longitude `l_deg` | hue on a 0-360 color wheel | circular order, clustering, mask-state shift | physical wavelength identity |
| galactic latitude `b_deg` | radial distance from galactic north pole, `r = R * (1 - abs(b)/90)` | pole/equator ordering | sky-map area and projection fidelity |
| hue sector | sevenfold note label `C D E F G A B` | aesthetic/compositional grouping | exact musical pitch or Newtonian historical assignment |
| multipole | marker shape: circle for ell=2, diamond for ell=3 | quadrupole/octupole distinction | statistical significance |

## Readout

| condition | median Q-O alignment | visual/compositional read |
| --- | ---: | --- |
| unmasked | 11.9 deg | ell=2 and ell=3 operator markers occupy a nearby hue/radius neighborhood |
| galcut20 | 29.5 deg | both multipoles shift, with weaker Q-O proximity than the unmasked extraction |

The visual artifact recovers the same qualitative fact as the directional
reports: the unmasked operator axes compose tightly enough to show the
published quadrupole-octupole alignment, while the synthetic galactic cut
moves the feasible chart and weakens that alignment.

## Allowed Claims

1. The conversion is a disciplined media/composition layer over existing
   directional-axis products.
2. Hue and note labels can make operator clustering and mask-state shifts
   easier to inspect.
3. The artifact is useful for communication, aesthetic operations, and
   cross-modal composition when its conversion contract is explicit.

## Forbidden Claims

1. The colors or notes are not new evidence for AOC.
2. The sevenfold sectors are not a physical pitch measurement.
3. The artifact does not replace the statistical nulls, mask controls, or
   Planck likelihood machinery.
4. The Opticks bridge is a near-cousin/instrumentation layer, not an
   instantiation-grade cosmological claim.

## Outputs

- `opticks_axis_residue_map.svg`
- `opticks_axis_residue_map.csv`
- `opticks_axis_residue_map_summary.json`
