# ApparentOrigin

Reproducible experiments on observer-bounded reconstruction and apparent extrema.

## First empirical target: MoM-BH*-1

The first experiment uses the public JWST observations behind Naidu et al. (2026), **“A gas-enshrouded and gas-reddened black hole at cosmic dawn”** (`10.1038/s41586-026-10846-4`). The source is MoM-BH*-1 at `z = 7.7569`.

The repository does **not** vendor the telescope data. GitHub Actions starts from an empty runner and:

1. queries the authors' Zenodo record (`10.5281/zenodo.15059214`),
2. downloads only bounded FITS spectrum products,
3. recovers the target sky position from the public spectrum,
4. asks the DAWN JWST Archive for the matching EXCELS `G395M` extraction,
5. downloads only that reduced spectrum,
6. records source URLs, archive metadata, SHA-256 hashes, and the Python environment,
7. runs the observer-thinning experiment, and
8. publishes only small receipts, tables, and plots as workflow artifacts.

Raw telescope products die with the runner.

## Phase 0 experiment

The current workflow is deliberately narrower than the full radiative-transfer claim. It asks whether the non-virial structure in the H-beta profile becomes less distinguishable as spectral access is synthetically reduced.

For each target resolving power `R`, it compares:

- a **virial-like** single broad Gaussian emission profile, and
- a nested **structured** profile with an additional absorption component.

The operational access quantity is initially

```text
Omega(R) = Delta BIC = BIC_virial-like - BIC_structured
```

Positive `Delta BIC` favors the structured profile. The predeclared necessary-condition test asks whether `Omega` is strong at native G395M resolution and collapses under controlled thinning.

This does **not** reproduce the paper's Cloudy/COLT inference and does not claim a ground-truth black-hole mass. The reported mass column is only a literature-anchored `M ~ FWHM^2` virial proxy. A later phase can replace the empirical surrogate with the actual competing forward models if Phase 0 survives.

## Provenance rule

Upstream scientific artifacts remain upstream. This repository stores identities and transformations, not ownership-by-copying:

```text
official public source
        -> immutable/archive identity
        -> ephemeral retrieval
        -> checksum receipt
        -> deterministic transformation
        -> small result
```

See `provenance/mom_bh1.yaml` and `.github/workflows/mom-bh1.yml`.
