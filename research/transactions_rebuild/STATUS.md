# Aegis Transactions Rebuild — tag4 finalization status

## Completed in this finalization branch

- Canonical mathematical model frozen in `FINAL_MODEL_SPEC_v2.md`.
- Observable temporal drift `D_{i,k}` formally defined from consecutive normalized detector observations.
- Risk-containment condition made explicit.
- Full `(m+1)`-state interior Jacobian implemented as `diag(beta I_m, a)`.
- Full Jacobian finite-difference tests added.
- Drift bounds, first-round behavior, maximum-distance normalization, and determinism tests added.
- Certificate construction is now the source of finalization in the reference kernel.
- Certificate weight and voters are emitted in the round trace.
- Historical v4 material is explicitly marked non-canonical.
- A Transactions-style manuscript draft is added under `research/transactions_rebuild/manuscript/`.
- The unsupported 9,450-case physical claim is excluded from the manuscript rather than fabricated.

## Mathematical gate

For fixed exogenous detector evidence and drift, the exact full Jacobian is
`J=diag((1-rho-ell E)I_m,a)`, with spectral radius
`max(|1-rho-ell E|,|a|)`. The theorem is interior and does not cover projection boundaries or endogenous detector dynamics.

## Evidence gate

The repository contains direct numerical validation of the archived phase-space CSVs, but not the raw case-level evidence required to independently reproduce the previously stated 9,450-case physical claim. That claim is therefore not part of the final paper.

## Runtime gate

GitHub Actions must execute the complete `research/transactions_rebuild` pytest suite on the finalization PR. No green status is inferred from static inspection.

## Release gate

Do not tag the final release until CI is green and the final audit confirms that manuscript equations, code, tests, and claims agree.
