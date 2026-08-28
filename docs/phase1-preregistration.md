# Phase 1A preregistration: observer access and virial mass residue

## Question

Does controlled loss of access to the resolved H-beta absorption structure produce a directional change in the black-hole mass reconstructed from the same source?

Phase 0 established only the necessary condition that a structured H-beta model is strongly preferred at native G395M resolution and loses that preference under controlled spectral thinning. Phase 1A tests whether that loss of distinguishability is accompanied by a directional mass reconstruction residue.

## Operators

Two reconstructions are run on the same thinned spectrum.

**V — virial-like operator**

A continuum plus one broad Gaussian emission line. This is intentionally the information-poor reconstruction: all resolved H-beta structure is forced into one broad component.

**S — absorption-aware operator**

The same broad Gaussian emission component plus one bounded absorption component. This is the Phase-0 structured surrogate. It is not Cloudy or COLT and must not be described as a physical radiative-transfer posterior.

The full-access S reconstruction at native G395M resolution is the reference reconstruction, not ground truth.

## Relative mass coordinate

For one source at fixed redshift, the Greene & Ho style H-beta virial scaling has the form

```text
M_BH ∝ L_Hbeta^0.59 FWHM_Hbeta^2
```

Therefore the relative mass coordinate is independent of luminosity distance and absolute flux units:

```text
q = 0.59 log10(F_Hbeta) + 2 log10(FWHM_Hbeta)
rho_M = q(operator, access) - q(S, native)
```

`F_Hbeta` is the integrated positive broad-emission Gaussian component from the fitted operator. `rho_M` is a reconstruction residue in dex. It is not an absolute black-hole mass.

Primary calibration reference: Greene & Ho (2005), DOI `10.1086/431897`. The local virial calibration is being used here as an estimator under test, not assumed valid at z=7.7569.

## Access intervention

Use the exact frozen DJA v3 G395M product already validated by Phase 0 and the same deterministic resolution ladder:

```text
native, 800, 600, 400, 250, 150, 100
```

No new telescope data are introduced.

A second control masks the three absorption regions motivated by the Nature line fit: systemic and approximately +/-1500 km/s. Masking is applied at native resolution so that loss of diagnostic access can be distinguished from instrumental smoothing alone.

## Quantities reported

For every access level and both operators:

- broad-emission integrated flux coordinate;
- FWHM;
- relative mass coordinate `rho_M`;
- Phase-0 `Delta BIC` model distinguishability.

Primary plot: `rho_M` versus `Delta BIC`.

Secondary plot: `rho_M` versus resolving power.

## Predeclared directional test

The stronger observer-access claim is supported in Phase 1A only if all of the following hold:

1. the Phase-0 distinguishability collapse remains present;
2. the virial-like operator ends at least `+0.30 dex` above the full-access structured reference at the lowest tested resolution;
3. the virial-like residue increases by at least `+0.20 dex` from native to the lowest tested resolution;
4. the sign is not produced solely by one pathological failed fit.

The masking control is reported independently and is not required to pass the resolution criterion.

## Falsification

The directional claim is **not supported** if thinning merely broadens/changes model preference while the virial-like mass coordinate remains stable, drifts downward, or changes by less than the thresholds above.

A negative scientific result must still produce green CI. CI failure is reserved for broken acquisition, invalid identity/provenance, malformed data, or computational failure.

## Boundary

Phase 1A does not reproduce Naidu et al.'s Cloudy/COLT model. The Nature paper states that the results can be reproduced using public reduced data and public software, but it does not publish the approximately million-model Cloudy grid or posterior as a reusable upstream artifact. A future Phase 1B may implement a genuine envelope forward model only when its assumptions and parameter grid can be reproduced explicitly and independently.
