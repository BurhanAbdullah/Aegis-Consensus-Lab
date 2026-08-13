# Aegis Transactions Rebuild — tag4

## Current objective
Rebuild the research artifact and manuscript into a technically defensible IEEE Transactions-level contribution, with exact alignment among mathematical model, implementation, experiments, and reported results.

## Status

- [x] Dedicated `tag4` working ref created
- [x] Existing branches left untouched
- [x] Initial repository audit completed
- [x] Initial paper/repository discrepancy audit completed
- [x] Rebuild roadmap committed
- [x] Critical implementation/data inconsistencies recorded
- [x] Freeze central research question
- [x] Freeze novelty/contributions
- [x] Freeze terminology and initial threat-model direction
- [x] Define canonical mathematical rebuild specification
- [x] Derive scalar trust equilibrium and exact local stability condition
- [x] Derive candidate weighted-quorum safety condition
- [x] Derive candidate availability condition
- [x] Derive candidate nonempty safety/availability interval
- [x] Define coupled Jacobian analysis target
- [x] Define implementation module boundaries
- [x] Define deterministic trace schema
- [x] Define analytical boundary and validation protocol
- [x] Define validation gates
- [x] Implement deterministic reference kernel
- [x] Implement weighted certificate semantics
- [x] Add certificate/quorum regression tests
- [x] Formalize protocol safety assumptions
- [x] Complete unified reduced mathematical state model
- [x] Complete predictive risk containment law
- [ ] Complete weighted quorum proof with final adversary semantics
- [ ] Prove all theorem candidates under final assumptions
- [ ] Execute tests in runtime
- [ ] Align production implementation with equations
- [ ] Rebuild reproducible experiments
- [ ] Reconcile all manuscript numbers with generated results
- [ ] Add strong baselines
- [ ] Add ablations
- [ ] Add sensitivity analysis
- [ ] Add statistical confidence intervals
- [ ] Generate analytical-vs-empirical phase boundary
- [ ] Rewrite manuscript
- [ ] Final equation/dimension audit
- [ ] Final citation audit
- [ ] Final professor/referee audit
- [ ] Submission-ready release

## Verified design freeze
Central question: under what conditions can predictive trust adaptation improve cyber-physical false-data attack governance while preserving consensus availability, and can the resulting security–availability boundary be analytically characterized and experimentally validated?

Core contribution direction: multidimensional trust + predictive influence attenuation + adaptive weighted quorum + formal equilibrium/stability/quorum-feasibility analysis + empirical phase-boundary validation.

## Current mathematical gate
The coupled system is treated as a dynamical system rather than a collection of independent mechanisms. The reduced analytical state is x=(tau,R), with stationary evidence and drift treated as exogenous inputs. The interior Jacobian and Jury conditions are implemented in `unified_state_model.py`. Risk containment is explicit: `(1-a)e + c d < 1-a` for an interior risk equilibrium, with boundary cases excluded from the interior differentiable theorem.

The target operating set remains
F={theta: spectral_radius(J(theta))<1 and (1+b)/2<q*(theta)<=h*}.

The weighted certificate semantics are explicit: votes are bound to height/view/phase/proposal context, duplicate validator votes are rejected, certificates require distinct-voter governance weight at least the active quorum weight, and safety is conditional on honest validators not signing conflicting proposals.

## Current implementation gate
The final kernel must be deterministic conditional on scenario inputs. Attack generation and detector noise are external. The production kernel must emit round-level state and certificate traces sufficient to reproduce every paper metric.

## Known critical issues to resolve
1. Full multidimensional trust dynamics still need exact production-to-equation alignment beyond the reduced analytical model.
2. Weighted quorum proof must be completed under the final adversarial certificate semantics.
3. Current production kernel and final manuscript must use the same multidimensional parameterization.
4. Existing manuscript governance headline results must be regenerated and reconciled against repository CSVs.
5. Current theoretical claims must be weakened or replaced by proofs that follow from explicit assumptions.
6. Attack terminology must distinguish FDIA/measurement attacks from actual topology manipulation.
7. Consensus survivability must be defined separately from broad resilience unless a formal resilience definition is introduced.
8. Runtime execution of the new kernel/tests has not yet been verified through an execution environment.

## Rule
A checklist item is marked complete only after implementation/evidence is verified. No manual headline numbers will be accepted into the final manuscript; results must flow from reproducible experiment artifacts.
