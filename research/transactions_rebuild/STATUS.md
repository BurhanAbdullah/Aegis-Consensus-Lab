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
- [ ] Complete unified mathematical state model
- [ ] Complete trust dynamics
- [ ] Complete predictive risk containment
- [ ] Complete weighted quorum model
- [ ] Derive equilibrium conditions
- [ ] Derive local stability conditions
- [ ] Derive security–availability feasibility boundary
- [ ] Align implementation with equations
- [ ] Add unit/property tests
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

## Known critical issues to resolve
1. Manuscript trust dynamics are not yet a single internally consistent state transition system.
2. Manuscript PRC description and trust update need to be separated or unified explicitly.
3. Current code uses a simpler scalar trust/quorum implementation than the manuscript's multidimensional formulation.
4. Existing manuscript governance headline results must be regenerated and reconciled against repository CSVs.
5. Current theoretical claims must be weakened or replaced by proofs that follow from explicit assumptions.
6. Attack terminology must distinguish FDIA/measurement attacks from actual topology manipulation.
7. Consensus survivability must be defined separately from broad resilience unless a formal resilience definition is introduced.

## Rule
A checklist item is marked complete only after implementation/evidence is verified. No manual headline numbers will be accepted into the final manuscript; results must flow from reproducible experiment artifacts.
