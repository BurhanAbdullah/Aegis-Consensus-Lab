# Transactions 10/10 Gate — tag4

This is the release gate for the Transactions-targeted tag4 rebuild.

## A. Mathematical model

- [x] Canonical state explicitly defined.
- [x] Trust recursion closed and bounded by projection.
- [x] Risk recursion closed with an explicit containment condition.
- [x] Observable drift mathematically defined from detector traces.
- [x] Governance influence separated from trust state.
- [x] Adaptive quorum explicitly defined.
- [x] Certificate semantics and honest non-equivocation assumptions explicit.
- [x] Safety/availability inequalities explicit.
- [x] Full interior Jacobian derived.
- [x] Spectral-radius stability condition derived.
- [x] 2-D Jury cross-check specified.
- [x] Security–availability feasible set defined.

## B. Mathematical validation

- [x] Closed-form equilibrium vs executable map.
- [x] Exact Jacobian vs finite-difference Jacobian.
- [x] Spectral radius vs direct eigenvalues.
- [x] Jury conditions vs direct Schur stability.
- [x] Containment boundary tests.
- [x] Projection/interior distinction tested.
- [x] Independent 1000-case numerical cross-validation script.
- [ ] Final manuscript equations independently typeset and audited against the canonical source.

## C. Empirical validation

- [x] Canonical six-scenario benchmark.
- [x] Frozen seeds.
- [x] Fixed-quorum comparison at two reference thresholds.
- [x] Comparative stress grid.
- [x] Component ablation.
- [x] Attack localization.
- [x] Publication artifact generation.
- [x] Repeated deterministic generation.
- [ ] Final manuscript tables regenerated from release artifacts.

## D. Scientific comparison

The principal comparison is against fixed weighted-quorum policies under identical traces. The comparator is intentionally not called PBFT or HotStuff. Broader protocol claims require protocol-equivalent implementation and theorem assumptions.

The main empirical claim is limited to the tested operational regime. In particular, a positive availability difference must not be generalized to arbitrary attack cardinality, topology, or Byzantine protocol behavior.

## E. Reviewer attack surface

### Reviewer 1 — theory

Check every theorem assumption, boundary condition, differentiability statement, equilibrium condition, and stability implication. Reject any claim that silently crosses from exogenous detector inputs to endogenous detector dynamics.

### Reviewer 2 — experiments

Check identical traces, attack timing, evidence magnitude, drift, seeds, sample counts, confidence intervals, baselines, ablations, and localization coverage. Recompute headline values from raw/frozen CSVs.

### Editor — contribution and scope

Check whether the paper makes one precise contribution, whether the mathematical object is genuinely new or materially useful, whether the comparison is fair, and whether every claim is proportionate to the evidence.

## F. Final release rule

10/10 means **all gates are green**, not that the current code merely passes tests. The release remains blocked until the actual manuscript is reconciled to the canonical model and frozen experiment artifacts.