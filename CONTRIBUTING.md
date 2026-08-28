# Contributing

ApparentOrigin is a reproducible research repository. Contributions are welcome when they preserve the distinction between **data identity**, **measurement**, **model**, and **interpretation**.

## Before changing science

Open an issue or pull request that states:

1. the scientific question or failure mode,
2. the exact data product or simulated input used,
3. the transformation or estimator being changed,
4. the expected observable consequence, and
5. what result would count against the proposed interpretation.

Negative scientific results are valid results. Do not turn a falsifying result into a CI failure unless the computation itself is broken.

## Reproducibility

- Do not commit raw telescope products unless redistribution is explicitly appropriate and necessary.
- Prefer stable upstream identifiers, retrieval URLs, checksums, and small derived artifacts.
- Keep acquisition bounded and validate target identity before analysis.
- Record software versions for computational results.
- Separate exploratory discovery scripts from the minimal reproducible path.

## Scientific claims

A successful test of a necessary condition is not evidence that a stronger theory has been established. State the boundary of every result plainly.

For MoM-BH*-1 in particular, the Phase-0 observer-thinning experiment does not reproduce the full Cloudy/COLT radiative-transfer inference and does not establish a ground-truth black-hole mass.

## Licensing

By contributing code, you agree that your contribution may be distributed under the repository's MIT License. Original research prose, figures, and tables contributed to the repository are made available under CC BY 4.0 unless otherwise marked. Upstream astronomical data and third-party material retain their original terms and attribution requirements.
