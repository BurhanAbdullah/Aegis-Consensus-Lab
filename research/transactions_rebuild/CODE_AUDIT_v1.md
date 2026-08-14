# Code-to-Model Audit v1 — tag4

## Canonical implementation decision
`research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md` is the canonical mathematical specification. `research/transactions_rebuild/kernel/tag4_kernel.py` is the deterministic executable reference for that specification. The legacy shell simulators (`core/consensus_v4.sh` and `archive/final_run/consensus_v4.sh`) are historical artifacts and are **not** used as evidence for canonical-model theorem or performance claims.

The canonical kernel is deterministic conditional on explicit scenario inputs. Attack generation and detector noise are external to the kernel. Detector evidence and observable temporal drift are implemented separately in `detector_evidence.py`.

## Mismatch ledger

| Model object | Historical implementation | Canonical tag4 form | Disposition |
|---|---|---|---|
| Trust state `T_i` | crypto/behavior/latency/sensor shell fields | bounded vector `T_i in [0,1]^m` | canonical kernel |
| Effective trust | fixed shell weighted sum | `tau_i=w^T T_i` | canonical kernel |
| Evidence `E_i` | implicit/random shell events | normalized detector evidence | canonical `detector_evidence.py` |
| Drift `D_i` | shell-local/random state | observable normalized detector-score drift | canonical `detector_evidence.py` |
| Risk `R_i` | integer heuristic | bounded recurrence `aR+(1-a)E+cD` | canonical kernel |
| Influence `G_i` | hard 15% attenuation | `tau_i clip(1-kappa R_i)` | canonical kernel |
| Quorum `q` | shell heuristic | clipped adaptive law from `tau_bar` | canonical kernel |
| Primary selection | highest shell trust | not used as a theorem primitive | historical only |
| Recovery/slashing | fixed shell `+6/-35` | explicit `rho/ell` recurrence | canonical kernel |
| Randomness | shell `RANDOM` inside dynamics | external deterministic scenario inputs | removed from canonical path |
| Finalization | shell weighted threshold | context-bound weighted certificate semantics | canonical certificate kernel |

## Critical findings and resolution

1. The old v4/v5 shell risk was non-differentiable and mixed stochastic attack generation with protocol dynamics. **Resolved for canonical evidence:** the submission reference is now the deterministic Python kernel; shell output remains historical only.
2. The old shell `CONFIDENCE >= 55` proxy for honesty is not a theorem variable. **Resolved by separation:** adversarial ground truth is an experiment input; confidence is not used as a theorem assumption in the canonical kernel.
3. The old shell quorum cap was not a general safety theorem. **Resolved in the canonical model:** the admissible safety/availability inequalities are explicit and strict; feasibility is tested independently.
4. The canonical state is explicitly `(T_i,R_i)` and detector evidence/drift are exogenous inputs. **Resolved.** If evidence becomes endogenous, its state must be appended before differentiating.
5. Random attack generation is external to the canonical protocol kernel. **Resolved.**
6. Certificate semantics are context-bound and reject duplicate voters, context mismatches, and insufficient weight. **Resolved and tested.**

## Canonical trace contract

The executable reference records, per round:

- round
- validator
- trust vector
- aggregate trust
- evidence
- observable drift
- risk
- governance influence
- total active governance weight
- quorum fraction
- quorum weight
- prepare weight
- commit/certificate weight
- finalization outcome

## Historical evidence rule

Historical simulator outputs are retained unchanged for auditability. They may be used only when explicitly labeled historical. Submission numerical claims must be regenerated from canonical inputs and the deterministic kernel. A disagreement between a historical artifact and canonical CSV-derived evidence must remain visible in the audit ledger; it must never be silently overwritten.
