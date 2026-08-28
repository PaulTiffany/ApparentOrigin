# ApparentOrigin

[![MoM-BH*-1 observer thinning](https://github.com/PaulTiffany/ApparentOrigin/actions/workflows/mom-bh1.yml/badge.svg)](https://github.com/PaulTiffany/ApparentOrigin/actions/workflows/mom-bh1.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Research text: CC BY 4.0](https://img.shields.io/badge/research%20text-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Reproducible experiments on observer-bounded reconstruction and apparent extrema.

## First empirical target: MoM-BH*-1

The first experiment uses the public JWST observations behind Naidu et al. (2026), **“A gas-enshrouded and gas-reddened black hole at cosmic dawn”** (`10.1038/s41586-026-10846-4`). The source is MoM-BH*-1 at `z = 7.7569`.

The repository does **not** vendor the telescope data. GitHub Actions starts from an empty runner and:

1. queries the authors' Zenodo record (`10.5281/zenodo.15059214`),
2. selects the pinned MoM source `150135` and reads its sky position from FITS metadata,
3. asks the DAWN JWST Archive for the matching EXCELS `G395M` extraction,
4. identifies EXCELS source `119077` at 0.064 arcsec separation,
5. retrieves the frozen v3 product used for the experiment,
6. validates its FITS position and H-beta wavelength coverage,
7. records source URLs, archive metadata, SHA-256 hashes, and the Python environment,
8. runs the observer-thinning experiment, and
9. publishes only small receipts, tables, and plots as workflow artifacts.

The selected EXCELS input is:

```text
excels-uds01-v3_g395m-f290lp_3543_119077.spec.fits
SHA-256 f155a6038bf0f47a61ae76ed535532e00962bade3ec5ed1c8a41b2ff0498fdbd
```

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

Positive `Delta BIC` favors the structured profile. The predeclared necessary-condition test required `Delta BIC >= 10` at native resolution and a drop of at least `5` under thinning.

### First CI result

The first green run supports that necessary condition:

| Resolving power R | Delta BIC |
| ---: | ---: |
| 1000 | 32.48 |
| 800 | 21.48 |
| 600 | 12.17 |
| 400 | -1.46 |
| 250 | -10.84 |
| 150 | -13.02 |
| 100 | -13.20 |

Across the ladder, `Delta BIC` drops by `45.67` with Spearman `rho = 1.000` for resolving power versus distinguishability. The structured H-beta model is strongly preferred at native G395M resolution and loses that preference under controlled spectral thinning.

This is a **necessary-condition preflight**, not the final dual-operator mass experiment. It does **not** reproduce the paper's Cloudy/COLT inference, establish a ground-truth black-hole mass, or yet show the predicted 1-2 dex mass-reconstruction trajectory. The reported mass column is only a literature-anchored `M ~ FWHM^2` virial proxy. The next scientific phase is to replace the empirical structured surrogate with the competing radiative-transfer reconstruction and test mass drift directly.

## Repository layout

- `src/` — bounded acquisition and analysis code.
- `provenance/` — pinned target identities, upstream sources, and experiment declarations.
- `.github/workflows/` — clean-run reproduction on GitHub-hosted runners.
- `CITATION.cff` — machine-readable citation metadata.
- `CONTRIBUTING.md` — contribution and falsification rules for scientific changes.

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

## Citation

GitHub reads `CITATION.cff` and exposes a **Cite this repository** control. Until this project has its own archived release DOI, cite the repository by version/commit and also cite the astronomical paper and upstream data product used by the experiment.

Primary astronomical reference: Naidu et al. (2026), DOI `10.1038/s41586-026-10846-4`.

Public MoM spectrum products: Zenodo DOI `10.5281/zenodo.15059214`.

## License and data rights

This repository uses a split research license:

- **Software** in `src/` and repository automation/configuration is licensed under the **MIT License**. See `LICENSE`.
- **Original research prose, figures, plots, and tables authored for this repository** are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)** unless a file says otherwise.
- **Upstream astronomical data, published papers, third-party software, and third-party material are not relicensed by this repository.** They remain governed by their original terms, data-rights policies, and attribution requirements.

The workflow deliberately retrieves public telescope products from their authoritative upstream locations and records provenance rather than republishing them as project-owned assets.
