# Aegis Transactions Rebuild — tag4 finalization status

## Completed

- Canonical mathematical model frozen in `FINAL_MODEL_SPEC_v2.md`.
- Observable temporal drift `D_{i,k}` formally defined from consecutive normalized detector observations.
- Risk-containment condition made explicit.
- Full `(m+1)`-state interior Jacobian implemented as `diag(beta I_m, a)`.
- Full Jacobian finite-difference tests added.
- Drift bounds, first-round behavior, maximum-distance normalization, and determinism tests added.
- Certificate construction is now the source of finalization in the reference kernel.
- Certificate weight and voters are emitted in the round trace.
- Explicit certificate-finalization regression tests added.
- Historical v4 material is explicitly marked non-canonical.
- Transactions-style manuscript draft added under `research/transactions_rebuild/manuscript/`.
- Unsupported 9,450-case physical claim excluded from final claims rather than fabricated.
- Tag4 GitHub Actions runtime suite executed successfully after the CI import-path fix.

## Verified runtime result

The final tag4 validation run (`run 42`) completed with a green `validate` job. The workflow executed the complete `python -m pytest -q research/transactions_rebuild` suite, including the new full-Jacobian, observable-drift, and certificate-finalization tests.

## Mathematical gate

For fixed exogenous detector evidence and drift, the exact full Jacobian is
`J=diag((1-rho-ell E)I_m,a)`, with spectral radius
`max(|1-rho-ell E|,|a|)`. The theorem is interior and does not cover projection boundaries or endogenous detector dynamics.

## Evidence gate

The repository contains direct numerical validation of the archived phase-space CSVs, but not the raw case-level evidence required to independently reproduce the previously stated 9,450-case physical claim. That claim is therefore not part of the final paper.

## Release gate

The implementation is now tested and committed on `tag4-finalization-v2`. Final release tagging/merge should occur only after the tag4 PR is accepted. No unsupported physical validation claim is being promoted to a release claim.
