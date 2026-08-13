# Code-to-Model Audit v1 — tag4

## Canonical implementation decision
The existing `core/consensus.sh` is legacy scalar-trust code and is not mathematically equivalent to the multidimensional AEGIS design. The v5-style implementation is the closest existing prototype, but it also uses heuristic risk and quorum laws. Neither is promoted as the final Transactions implementation.

## Mismatch ledger

| Model object | Existing implementation | Required tag4 form | Disposition |
|---|---|---|---|
| Trust state T_i | crypto/behavior/latency/sensor | bounded vector T_i | retain concept; formalize update |
| Effective trust | fixed 0.40/0.30/0.15/0.15 weighted sum | w^T T_i | retain weights initially; expose as parameters |
| Evidence e_i | implicit/random events | explicit normalized detector evidence | replace |
| Risk R_i | integer heuristic from confidence delta/oscillation/latency | explicit state/function E(T,R) | replace |
| Influence G_i | 15% hard attenuation when R>15 | tau_i phi(R_i) | replace |
| Quorum q | safety heuristic 50%..66% | q0 + alpha_q(1-tau_bar), clipped | replace |
| Primary | highest effective trust | highest governance weight, tie-broken deterministically | retain with deterministic tie break |
| Recovery | fixed +6 behavior per round | rho recovery map | replace |
| Slashing | fixed -35 behavior | explicit degradation term ell e T | replace |
| Randomness | shell RANDOM in dynamics | seeded/exogenous scenario process | remove from core dynamics |
| Finalization | weighted threshold | formal certificate semantics | redesign |

## Critical findings
1. Existing v5 risk is not differentiable as written because it is integer-valued, thresholded, and partly based on state that is not persistently updated (`PREV_CONFIDENCE` is initialized per run).
2. The existing safety estimate uses confidence >=55 as a proxy for honesty; this is not a Byzantine ground-truth variable and cannot appear as a theorem assumption without explicit interpretation.
3. The current quorum is capped at 66%, which conflicts with the general weighted safety condition when adversarial weight b requires q>(1+b)/2. The final controller must expose q_max and report infeasible states.
4. Existing trust updates are per-dimension and asymmetric; the final paper must state whether the model is a vector recurrence or a scalar aggregate recurrence.
5. Random Byzantine events inside the protocol executable mix the stochastic attack generator with the protocol dynamics. These must be separated for reproducible experiments.
6. The old scalar implementation has a fixed 2/3 quorum and therefore cannot be used to validate the adaptive-quorum theorem.

## Refactor target
Implement one deterministic protocol kernel driven by an explicit scenario input. Attack generation, detector evidence, trust dynamics, governance weighting, quorum calculation, and PBFT certificate verification must be separate modules.

The protocol kernel must emit a machine-readable trace containing at least:
- round
- validator
- trust vector
- aggregate trust
- evidence
- risk
- governance weight
- total active weight
- quorum fraction
- quorum weight
- prepare weight
- commit weight
- finalization outcome
- adversarial ground truth

The experiment runner, not the protocol kernel, controls random seeds and attack schedules.
