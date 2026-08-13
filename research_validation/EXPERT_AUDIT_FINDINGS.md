# AEGIS Expert Audit Findings

## Scope

This document records conclusions from the reproducibility audit of the frozen `archive/final_run` evidence. It intentionally distinguishes direct evidence, independent numerical validation, and claims that require a separate mathematical-model implementation.

## 1. Phase-space experiment

The archived experiment contains 36 `(slash, recover)` cells. Direct recomputation from `phase_space_baseline.csv` and `phase_space_predictive.csv` gives:

| Metric | Baseline | Predictive | Paired difference |
|---|---:|---:|---:|
| Mean successes | 135.03 | 139.11 | +4.08 |

Predictive containment wins 20 cells, loses 15, and ties 1. The paired difference ranges from -76 to +58, with SD 29.86.

The current statistical audit runs a paired t-test, Wilcoxon signed-rank test, exact sign test, and deterministic bootstrap confidence interval. The paired t-test and Wilcoxon test are not significant at the 0.05 level. Accordingly, the experiment should be described as **phase-dependent restructuring of the success landscape**, not as universal predictive improvement.

## 2. Historical README inconsistency

The archived `archive/final_run/README.md` reports baseline/predictive means of 143.14 and 115.03. Those values do not match the means obtained by recomputing the archived 36-cell CSVs. The audit therefore marks those README values as stale metadata and uses the CSV-derived values for quantitative conclusions.

The frozen archive is not silently rewritten.

## 3. Recovery Elasticity Ratio Λ

The proposed condition

`Λ = ρ_recovery / (β_slash f_byz + δ_attenuation) >= 1`

may be a valid condition for a separately defined trust-mass recurrence, but the archived implementation does not itself encode that recurrence. The implementation uses fixed `SLASH=35`, `RECOVER=6`, heuristic trust updates, predictive attenuation, and adaptive quorum logic.

Therefore the present artifact can support **implementation behavior under the archived simulator**, but it cannot by itself establish the claimed necessary-and-sufficient Λ theorem. To establish that theorem empirically, the paper/code needs an explicit implementation of the mathematical recurrence, parameter mapping, equilibrium calculation, and controlled sweeps on both sides of Λ=1.

## 4. Physical AC-grid claim

The current expert-validation workflow independently solves standard pandapower test networks. That validates the installed numerical power-flow stack, not the previously stated 9,450-case AEGIS cyber-physical result.

The claim that predictive risk attenuation eliminated 100% of attack-induced overloads/voltage deviations therefore remains **unvalidated by this repository state** until the exact AC network, attack cases, controller mapping, outputs, and baseline/predictive comparison are reproducibly included.

## 5. Publication consequence

The strongest defensible story at this stage is:

> AEGIS introduces predictive epistemic containment into an adaptive trust-weighted consensus mechanism and changes the phase-space distribution of successful consensus outcomes. The effect is strongly phase-dependent: some attack/recovery regimes improve while others deteriorate. The proposed Recovery Elasticity Ratio is a mathematical condition that requires a separately implemented and validated recurrence before it can be presented as an empirically established necessary-and-sufficient theorem.

This wording is substantially safer and stronger scientifically than claiming universal performance gains or presenting the current simulator as proof of a theorem it does not explicitly implement.
