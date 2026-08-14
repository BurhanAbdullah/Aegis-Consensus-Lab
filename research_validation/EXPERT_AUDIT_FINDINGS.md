# AEGIS Expert Audit Findings

## Scope

This document records conclusions from the reproducibility audit of the frozen `archive/final_run` evidence and the canonical tag4 mathematical implementation. It distinguishes historical evidence, independent numerical validation, and claims that remain unsupported.

## 1. Historical phase-space experiment

The archived experiment contains 36 `(slash, recover)` cells. Direct recomputation from the archived phase-space CSVs gives:

| Metric | Baseline | Predictive | Paired difference |
|---|---:|---:|---:|
| Mean successes | 135.03 | 139.11 | +4.08 |

Predictive containment wins 20 cells, loses 15, and ties 1. The paired difference ranges from -76 to +58, with SD 29.86.

The paired t-test and Wilcoxon test are not significant at the 0.05 level. The correct description is **phase-dependent restructuring of the success landscape**, not universal predictive improvement.

## 2. Historical README inconsistency

The archived `archive/final_run/README.md` reports baseline/predictive means of 143.14 and 115.03. Those values do not match the means obtained by recomputing the archived 36-cell CSVs. Those README values remain preserved as stale historical metadata. The CSV-derived values remain canonical for the archived experiment.

No historical artifact is silently rewritten.

## 3. Canonical recurrence and code mapping

The repository now contains an explicit canonical mathematical specification in `research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md` and a deterministic reference implementation in `research/transactions_rebuild/kernel/tag4_kernel.py`.

The canonical implementation explicitly separates:

- bounded trust vector `T`;
- aggregate trust `tau`;
- validated detector evidence `E`;
- observable detector drift `D`;
- predictive risk `R`;
- governance influence `G`;
- adaptive quorum `q`;
- context-bound weighted certificates.

Attack generation and detector noise are external scenario inputs. The legacy shell simulator remains historical and is not used to establish canonical mathematical claims.

For fixed exogenous `E,D`, the implementation matches the stated trust/risk recurrences and the corresponding interior Jacobian. The scalar equilibrium and stability conditions are independently tested. The coupled endogenous case remains a separate mathematical case and must include detector-state derivatives before a stronger Jacobian claim is made.

## 4. Recovery Elasticity Ratio

The proposed condition

`Lambda = rho_recovery / (beta_slash f_byz + delta_attenuation) >= 1`

may be a valid condition for a separately defined trust-mass recurrence, but it is **not** an empirical theorem of the archived simulator. It must remain conditional on its explicit recurrence, assumptions, parameter mapping, and independent sweeps across both sides of the boundary.

No universal `Lambda >= 1` claim is permitted for the archived affine simulator.

## 5. Physical AC-grid claim

The expert-validation workflow independently solves standard pandapower test networks. That validates the numerical power-flow stack, not the previously stated 9,450-case AEGIS cyber-physical result.

The claim that predictive risk attenuation eliminated 100% of attack-induced overloads/voltage deviations remains **unvalidated** until the exact AC network, attack cases, controller mapping, outputs, and baseline/predictive comparison are reproducibly included.

## 6. Current validation status

The canonical kernel now has deterministic replay, state-domain, observable-drift, scalar-equilibrium, strict quorum-boundary, certificate-threshold, and scenario-input tests. These tests are validation of the implementation contract; they are not a substitute for the missing physical-grid evidence or a manuscript-level audit.

## 7. Publication consequence

The strongest defensible story at this stage is:

> AEGIS defines a predictive epistemic containment mechanism within an adaptive trust-weighted consensus model. The canonical implementation is deterministic conditional on explicit detector/scenario inputs and is mathematically aligned with the stated trust, risk, influence, quorum, and certificate rules. The archived empirical study shows phase-dependent changes rather than a universal predictive advantage. The Recovery Elasticity Ratio remains a conditional analytical result until its recurrence and boundary sweeps are independently validated. The previously stated 9,450-case physical-grid result is not established by the current repository evidence.

This wording is substantially safer and stronger scientifically than claiming universal performance gains or using the historical shell simulator as proof of a theorem it does not explicitly implement.
