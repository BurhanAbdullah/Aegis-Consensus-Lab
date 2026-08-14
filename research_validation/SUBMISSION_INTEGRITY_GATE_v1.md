# Transactions Submission Integrity Gate — tag4

This gate is intentionally conservative. A green unit-test suite is not sufficient for submission.

## Hard blockers

- [ ] A manuscript artifact is present in the repository and is the exact version being submitted.
- [ ] Every headline numerical value is regenerated from versioned raw data and scripts.
- [ ] No stale README/table/figure value conflicts with recomputed data.
- [ ] Every theorem is proved from explicitly stated assumptions.
- [ ] No universal `Lambda >= 1` claim is made for the affine trust recurrence.
- [ ] Weighted quorum safety is stated only under normalized-weight, Byzantine-weight, context-binding, and honest non-equivocation assumptions.
- [ ] Stability claims use the actual state-transition map and an appropriate Jacobian/spectral-radius condition; clipping regimes are treated separately.
- [ ] Physical-grid claims have the exact raw experiment/controller artifacts and an independently reproducible recomputation.
- [ ] Statistical claims report the actual sample definition, paired structure, uncertainty, and non-significant results where applicable.
- [ ] Attack terminology matches what was actually changed; measurement/FDI attacks are not called topology attacks unless topology was modified.
- [ ] All experiments have frozen seeds/configuration and a documented construction/validation separation where applicable.
- [ ] Repository code, equations, figures, tables, and manuscript are frozen to one commit before submission.

## Resolved in the canonical validation work

- [x] Historical simulator outputs are explicitly treated as historical and are not used as canonical theorem evidence.
- [x] Canonical numerical semantics are defined by `FINAL_MODEL_SPEC_v2.md` and implemented by `kernel/tag4_kernel.py`.
- [x] Detector evidence and observable drift are deterministic functions of explicit detector inputs.
- [x] Random attack generation is outside the canonical protocol kernel.
- [x] Persistent trust/risk state is carried by the canonical kernel across calls.
- [x] Weighted certificate context binding and duplicate-voter rejection are implemented and tested.
- [x] Strict quorum safety boundary handling is implemented and tested.
- [x] Scalar trust-equilibrium and stability conditions are explicitly tested against the mathematical reference case.

## Remaining blockers

1. The archived 36-cell phase-space experiment remains historical evidence. Its CSV-derived means are canonical for that archived experiment, while the contradictory archived README means remain preserved as stale metadata. The archived study does **not** support a universal predictive-improvement claim.
2. The repository does not contain the exact raw/controller artifacts required to verify the previously stated 9,450-case AC-grid result. That claim remains unverified and must not appear as an established result.
3. The repository contains no `.tex` or `.pdf` manuscript artifact. Manuscript-level equation/table/figure/reference consistency cannot be certified until the exact submission manuscript is added.
4. The Recovery Elasticity Ratio is a mathematical condition for its explicitly defined recurrence. It must not be presented as an empirically established necessary-and-sufficient theorem until the recurrence-to-code parameter mapping and independent sweeps across both sides of the boundary are included.
5. Final publication performance comparisons against external consensus baselines are not certified by the archived simulator alone. They require canonical-kernel experiments with frozen scenarios/seeds and matched metrics.

## Release rule

Do not merge PR #2, create a submission tag, or describe `tag4` as submission-ready until every hard blocker above is checked and the final CI run is green.
