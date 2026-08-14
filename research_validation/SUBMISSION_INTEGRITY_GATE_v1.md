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
- [ ] All experiments have frozen seeds/configuration and a documented train/test or construction/validation separation where applicable.
- [ ] Repository code, equations, figures, tables, and manuscript are frozen to one commit before submission.

## Current known blockers

1. The current expert audit reports a mismatch between historical README means and recomputed phase-space CSV means.
2. The archived 36-cell phase-space experiment does not show a statistically significant global predictive advantage at alpha=0.05.
3. The current repository does not contain the complete exact raw evidence required to verify the previously reported 9,450-case AC-grid claim.
4. The repository currently has no `.tex` or `.pdf` manuscript artifact, so manuscript-level word/equation/reference verification cannot yet be certified from the repository.
5. The corrected recurrence audit must pass analytically; finite-horizon simulation values must not be used as asymptotic proof.

## Release rule

Do not merge PR #2, create a submission tag, or describe `tag4` as submission-ready until every hard blocker above is checked and the final CI run is green.
