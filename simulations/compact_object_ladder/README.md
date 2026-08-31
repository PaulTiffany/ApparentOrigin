# Natural compact-object transfer ladder

This is a fixed astronomical calibration exercise.

The code evaluates the same textbook quantities for five natural/theoretical
reference cases:

1. Earth
2. Sun
3. canonical `0.6 M_sun` white dwarf
4. canonical `1.4 M_sun`, `12 km` neutron star
5. a `1 M_sun` Schwarzschild boundary

It accepts no external mass/radius inputs and contains no model of construction,
growth, replication, confinement, or intervention.

## Question

How does gravitational compactness change across familiar natural objects, and
can two independently stated entropy relations provide a mechanical
transferability check?

For each case:

```text
r_s = 2GM/c^2
C   = r_s / R
```

The script also evaluates:

```text
Bekenstein bound(R, M)
Bekenstein-Hawking entropy(M)
```

For fixed `M`, their ratio reduces to

```text
Bekenstein bound / BH entropy = R/r_s = 1/C
```

so the expressions meet at the Schwarzschild boundary.

That identity is the transferable object: another observer can start from the
two published formulae, derive the ratio independently, and compare it with the
checked-in numerical ladder.

## Result

| Reference case | Compactness `C` | `R/r_s` |
| --- | ---: | ---: |
| Earth | `1.392e-9` | `7.183e8` |
| Sun | `4.245e-6` | `2.356e5` |
| canonical white dwarf | `2.123e-4` | `4.711e3` |
| canonical neutron star | `0.3446` | `2.902` |
| 1-solar-mass Schwarzschild boundary | `1` | `1` |

The large jump between white-dwarf and neutron-star compactness is visible
without invoking any speculative mechanism.

## Reproduce

```bash
cd simulations/compact_object_ladder
python -m unittest -v test_compact_object_ladder.py
python compact_object_ladder.py
git diff --exit-code reference_results.csv
```

The implementation uses only the Python standard library and declared SI
constants.

## Boundary

This exercise does not establish a technological path to strong gravity and
does not test claims about quantum foam, artificial collapse, cosmological
reproduction, or causal loops. It is an astronomy/theory calibration artifact.

The white-dwarf and neutron-star entries are canonical approximations, not
catalog measurements.

## Primary references

- J. D. Bekenstein, “Universal upper bound on the entropy-to-energy ratio for
  bounded systems,” *Physical Review D* 23, 287 (1981).
  DOI `10.1103/PhysRevD.23.287`
- J. D. Bekenstein, “Black holes and entropy,” *Physical Review D* 7, 2333
  (1973). DOI `10.1103/PhysRevD.7.2333`
- S. W. Hawking, “Particle creation by black holes,” *Communications in
  Mathematical Physics* 43, 199–220 (1975).
  DOI `10.1007/BF02345020`
