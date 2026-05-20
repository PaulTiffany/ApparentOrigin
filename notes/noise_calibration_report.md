# Noise Calibration Report: Pantheon+ "Thickness"

## Summary
We have calibrated the noise growth exponent $p$ using the Pantheon+ covariance diagonal. This measurement replaces the toy model assumption ($p=1.8$) with an empirical value derived from the actual instrument/pipeline performance.

## Results
- **Model:** $\sigma_\mu = \sigma_0 (1+z)^p$
- **Derived Exponent $p$:** $0.050 \pm 0.047$
- **Base Uncertainty $\sigma_0$:** $0.168$ mag
- **Source:** `Pantheon+SH0ES_STAT+SYS.cov` diagonal.

## Interpretation: The Thick Observer
The measured $p \approx 0.05$ is nearly zero. This indicates that the Pantheon+ pipeline is a **Thick Observer**: it maintains nearly constant distance-modulus uncertainty across its entire observed redshift range ($z \in [0, 2.3]$). 

In AOC terms:
- A "Thin" observer ($p \gg 1$) would see a sharp reconstruction cliff as redshift increases.
- A "Thick" observer ($p \to 0$) distributes the reconstruction cost across the entire observed volume, pushing the "Atlas Fracture" floor much deeper.

## Comparison to Toy Models
| Model | Exponent $p$ | Meaning |
| :--- | :--- | :--- |
| **Toy v0** | $1.8$ | Rapid noise growth; sharp $K$ wall. |
| **Measured v1.1** | $0.05$ | Flat noise; high dynamic range. |

## Strategic Impact
The "v1 Proof-Derived Deformation" previously used $p=1.8$. Since the actual pipeline demonstrates $p \approx 0.05$, the next contract iteration (v1.2) should use this empirical $p$ to evaluate the deformation. This anchors the AOC claim in the **actual recorded capability of the instrument** rather than a theoretical guess.

If AOC is a "Science of the Interface," then $p=0.05$ is our first measured parameter of that interface for the supernova probe.
