# Transactions Project 10/10 Gate — tag4

This gate evaluates the **research implementation and validation package**, independently of manuscript writing.

## 1. Mathematical correctness

- [x] Canonical state and recursions are explicit.
- [x] Trust state is projected to its admissible domain.
- [x] Risk containment condition is explicit.
- [x] Observable temporal drift is defined without attack ground truth.
- [x] Full interior Jacobian is implemented analytically.
- [x] Spectral-radius stability criterion is explicit.
- [x] Coupled two-state Jacobian/Jury analysis is documented.
- [x] Weighted quorum safety/availability assumptions are explicit.
- [x] Heterogeneous-validator behavior is distinguished from scalar reference reductions.

## 2. Independent mathematical validation

- [x] Closed-form equilibria are checked against the executable recurrence.
- [x] Exact Jacobian is checked against finite differences.
- [x] Spectral radius is checked against direct eigenvalues.
- [x] Jury conditions are checked against direct Schur stability.
- [x] Risk-containment boundaries are tested.
- [x] Projection/interior behavior is distinguished.
- [x] Independent 1000-case cross-validation exists.
- [x] Deterministic repeat cross-validation exists.

## 3. Adversarial validation

- [x] Exact quorum safety boundary is tested.
- [x] Below/above-boundary cases are included.
- [x] Byzantine concentration in the intersection is considered.
- [x] Conflicting certificates are targeted.
- [x] Duplicate voters and replay contexts are targeted.
- [x] Honest non-equivocation is explicit in the theorem assumptions.

## 4. Empirical validation

- [x] Six canonical scenarios are retained.
- [x] Frozen seeds are used.
- [x] Fixed-quorum references use identical traces.
- [x] Stress grid and component ablations exist.
- [x] Attack localization exists.
- [x] Repeated deterministic generation is required.
- [x] Publication metrics are generated from frozen artifacts, not hard-coded values.
- [x] Publication generator validates schema, round coverage, numeric fields, and paired traces.

## 5. Reproducibility

- [x] Tests are runnable through GitHub Actions.
- [x] Independent validation is runnable through GitHub Actions.
- [x] Frozen 200-round release traces are checked exactly.
- [x] Generated artifacts are fail-closed on missing or malformed inputs.
- [x] No unsupported physical-system result is fabricated or promoted.

## 6. Release rule

A new Transactions tag is allowed only after the latest commit has:

1. green complete Transactions tests;
2. green independent mathematical cross-validation;
3. green deterministic repeat audit;
4. green adversarial/security validation;
5. successful frozen-artifact comparison generation;
6. successful artifact verification; and
7. no unresolved scientific correctness blocker.

**Paper drafting is not a gate here. The implementation/research package must stand on its own.**
