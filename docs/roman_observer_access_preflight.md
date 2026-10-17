# Roman observer-access contract — commissioning preflight (no science run)

**Status (2026-10-17): PRE-RELEASE PREPARATION ONLY.** No Roman flight science dataset has been selected, downloaded, fitted or used to test AOC. This is a prospective access contract, not a preregistered numerical claim. A later version must freeze exact product IDs, uncertainties and thresholds **before inspecting science residuals**.

## Instrument and release boundary

NASA reports Roman launched on **2026-08-30** and is in commissioning. The first public mission science products are anticipated in early 2027; data access follows pipeline processing. Source-backed pointers:

- NASA launch/commissioning statement: https://www.nasa.gov/news-release/nasas-dark-universe-seeking-nancy-grace-roman-space-telescope-launches/
- Official WFI technical information (prism P127: 0.75–1.80 μm, R about 80–180; grism G150: 1.00–1.93 μm, R about 600): https://science.nasa.gov/mission/roman-space-telescope/wfi-technical/
- Roman survey designs: https://roman.gsfc.nasa.gov/science/High_Latitude_Time_Domain_Survey.html
- Roman science product documentation: https://roman-docs.ipac.caltech.edu/roman-proposals-home/cycle-1-call-for-proposals/roman-observations
- Roman data product levels, revisions and prompt vs release products: https://roman-docs.stsci.edu/data-handbook/wfi-data-levels-and-products/data-releases

The source product route is official Roman flight products in **MAST** with archived pipeline/calibration provenance, not news items, simulations passed off as observations or re-hosted telescope archives. Prompt data and later survey releases must be treated as *different reductions*, not silently swapped within a frozen test.

### A crucial non-overlap with MoM-BH*-1

**Do not claim Roman directly re-observes the MoM Hβ experiment in the same wavelength channel.** At z = 7.7569, Hβ lies near 4.26 μm observed-frame, well outside both Roman WFI slitless spectroscopic bands. Roman is a **new observer/operator family**, not an interchangeable replication of JWST G395M. A cross-instrument transfer requires genuinely overlapping targets, wavelengths and selection functions, separately preregistered.

## First eligible data product

Primary candidate: **High-Latitude Time-Domain Survey (HLTDS)** repeated WFI imaging and, when available for appropriate sources, prism spectroscopy.

Prospective data order:
1. Same-source, repeated-epoch **WFI photometric** measurements/uncertainties, along with visit metadata, bandpass, exposure duration, quality and calibration flags (prompt L2 rate images and/or validated L4 catalogs).
2. WFI prism **L4 extracted spectra** with extraction/decontamination provenance; grism only where its spectral support and extraction configuration overlap the declared target.
3. Repeated processing of a single exposure/release through a *controlled observer-access operator*. Never substitute different astrophysical epochs for synthetic spectral thinning without modeling variability.

Do not choose the most visually interesting transient *after* inspecting its reconstruction residue. Source/selection class, detection criteria, missing-data rules and time-window rules must be frozen against a catalog version before fitting.

## Prospective operators (definitions, no hidden tuning)

Let `D` be an immutable, timestamp-sorted, source-identity-checked observation collection and `A` the observer-access operator. Define the following candidate operators now; freeze the chosen primary operator, exact indexing/tie-break, sample and numerical thresholds in a later executable preregistration:

- **Temporal thinning T2:** retain every other eligible observation in a deterministic sort of public exposure identifiers within each source and filter. Report both parity choices as a robustness control, never select the better-looking parity.
- **Band suppression B:** fit using all predeclared available filters, then systematically remove one predeclared filter. No implicit substitution of a nearby band or population-derived photometric prior.
- **Spectral operator S_R (conditional):** if a suitable G150 spectrum exists, degrade it using an explicitly specified line-spread kernel within **1.00–1.80 μm** shared support. Do not compare non-overlapping bandpasses as if differences were only resolving power. A prism/grism observational comparison must model distinct pipeline and contamination effects.

At fixed source and physical hypothesis family, measure how model distinguishability, held-out predictions and parameter intervals change under `A`. Use the **same physical forward family** in full and thinned views; report both model fit and its degradation. Baselines must include ordinary noise, sampling/completeness, calibration, contamination, transient evolution and realistic synthetic light curves. Distinguish **access loss** from an intrinsically new physical signal.

No AOC-specific residual threshold is claimed here. The preregistration must name the exact statistic, null distribution, effect size, uncertainty/correlation handling, multiplicity adjustment and stop rule *before seeing outcomes*. Until then, `NO_SCIENCE_GATE_EXECUTED` is the only status.

## Provenance and Actions-only execution

The eventual workflow must follow:

```text
official MAST / released Roman product + release identity
  -> ephemeral Actions retrieval + source identity and SHA-256 receipt
  -> pinned calibration / extraction metadata
  -> deterministic access operator + predeclared model comparison
  -> small table, figure, test report and hashes
  -> allowed claim / forbidden claim / science-log entry
```

Actions uploads may contain only small reproducibility receipts and derived products, with no bulk Roman archives. Record the tested public release and *all* pipeline versions, including reprocessing/correction notices. A nondetection is data when its sensitivity/selection is declared, not a zero flux.

## Allowed / forbidden claims

**Allowed:** a specified Roman observation family could test whether observer-access thinning changes *reconstruction under that particular operator*; the study is pre-positioned to make the comparison reproducible.

**Forbidden:** Roman has found evidence of an apparent origin; AOC is confirmed by a mismatch; Roman WFI can observe MoM-BH*-1 Hβ; ordinary survey selection or pipeline effects constitute a cosmological reconstruction boundary; a preflight plan is an executed preregistered test.

## Next gate

Once relevant products appear: (1) register the exact MAST collection/product IDs, sample selection, versions and model family; (2) freeze `T2` or `B` or `S_R` as **one primary operator** plus controls; (3) set a numerical null and stopping rule; (4) execute via GitHub Actions; (5) publish the science-log allowed/forbidden pair regardless of sign. If products or overlapping support are insufficient, record **UNTESTABLE_WITH_RELEASE** without inventing a result.
