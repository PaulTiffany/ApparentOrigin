# lambda_K Operator-Prism Contract Gate

Status: executable readiness gate for the Episode 4 Planck operator-prism contract.

Phase: TTCS contract readiness. This report is not an observed-value claim and does not turn Episode 3 into a prediction.

Contract coordinate:

```text
C_axis = (D_res - D_op) / 57 deg
```

Live predeclared target:

```text
C_axis(ell=3, official-mask-base) > 0
and remains > 0 for official-mask-dilate1.
```

## Live Contract Gate

Verdict: `contract_success_if_inputs_were_predeclared`.

| mask | D_op | D_res | C_axis | status |
| --- | ---: | ---: | ---: | --- |
| `base` | 4.088 | 20.133 | 0.281497 | `live_contract_input_present` |
| `dilate1` | 1.363 | 25.625 | 0.425643 | `live_contract_input_present` |

The required official-mask ell=3 operator axes and pair-residue
axes are present for both live masks. The verdict above is therefore
an evaluation of the predeclared operator-prism channel contract.

## Retrospective Context

These rows use existing full summaries. They are coordinate checks only;
they do not confirm the contract because they were not the predeclared
official-mask base/dilate1 pair-residue run.

| label | ell | D_op | D_res | C_axis | claim status |
| --- | ---: | ---: | ---: | ---: | --- |

## Next Required Artifact

Archive the cloud artifact locally and run an independent replication or sensitivity check.

## Allowed Claims

1. The operator-prism coordinate has an executable readiness gate.
2. The live official-mask `base -> dilate1` run satisfies the sign condition for this Planck operator-prism channel.
3. This is a channel-contract success, not an AOC confirmation.

## Forbidden Claims

1. The retrospective rows confirm `lambda_K`.
2. A positive `C_axis` is AOC evidence.
3. The missing `D_res` value may be inferred from operator-axis survival alone.
4. Contract success derives an observed `lambda_K` amplitude.
