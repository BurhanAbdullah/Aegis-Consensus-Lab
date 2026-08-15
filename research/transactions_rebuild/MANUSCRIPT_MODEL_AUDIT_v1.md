# Manuscript–Canonical Model Audit v1 — Transactions tag4

## Purpose

This audit is a release-control document. It checks that the Transactions manuscript does not silently promote a scalar or reduced result into a theorem about the full heterogeneous canonical model.

## Canonical source

`research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md` on the frozen tag4 lineage is authoritative for the state transition, detector interface, governance law, certificate semantics, safety/availability assumptions, and Jacobian definition.

## Audit findings

### A. State and trust dynamics — PASS

The manuscript now defines the validator trust vector, weighted aggregate trust, predictive risk, projection, and the per-validator trust/risk recursions consistently with the canonical source.

### B. Heterogeneous equilibrium — PASS

For fixed exogenous evidence `E_i=E` and drift `D_i=D`, the manuscript derives the exact componentwise interior equilibrium

`T_i^* = rho_i/(rho_i + ell_i E) 1`.

It then derives `tau_i^* = rho_i/(rho_i + ell_i E)`. The manuscript explicitly states that a common scalar `tau^*` requires the homogeneous reduction `rho_i=rho`, `ell_i=ell`.

### C. Risk equilibrium and containment — PASS

The manuscript uses

`R_i^* = ((1-a_i)E+c_iD)/(1-a_i)`

and explicitly conditions the interior result on the canonical containment inequality. If containment fails, the projection model is not treated as differentiable interior dynamics.

### D. Full Jacobian — PASS

The manuscript uses the exact canonical interior Jacobian

`J_i = diag((1-rho_i-ell_i E_i) I_m, a_i)`

and the corresponding spectral-radius condition. The theorem is explicitly limited to exogenous detector inputs and interior points.

### E. Coupled dynamics — PASS

The manuscript distinguishes the full exogenous-input Jacobian from an explicit coupled two-state reduction. Jury conditions are presented only for the real `2 x 2` reduction.

### F. Governance quorum boundary — CORRECTED

The previous draft could be read as treating

`q^* = q0 + alpha_q ell E/(rho+ell E)`

as the equilibrium quorum of the general model. That was too strong because the canonical quorum uses the state-dependent weighted quantity `bar tau`, while governance influence also depends on risk and active-set membership.

The manuscript now labels this expression `q_ref^*` and states explicitly that it is a homogeneous scalar reference boundary. The general operating set uses the full state-dependent `q^*(theta)` and `h^*(theta)`.

### G. Safety and availability — PASS

Safety is stated conditionally on authenticated certificate context and honest non-equivocation. Availability is expressed as `q <= h_k`. The `q <= 1-b` expression is labeled a conservative sufficient condition when `h_k >= 1-b`, rather than an unconditional liveness theorem.

### H. Empirical evidence — PASS WITH RELEASE BLOCK

The manuscript does not claim independent reproduction of the historical 9,450-case physical validation because the raw case-level evidence is absent from the canonical rebuild. This claim remains excluded.

## Remaining release gates

1. Compile the manuscript with the exact Transactions release environment.
2. Regenerate any manuscript tables from frozen release artifacts rather than hand-entering values.
3. Attach the final figure/table provenance manifest to the release.
4. Run the complete validation workflow on the successor branch.
5. Perform one final theorem-to-equation-to-code audit after the release artifacts are frozen.

## Non-negotiable claim discipline

- Do not call the scalar reference boundary the full heterogeneous boundary.
- Do not claim endogenous-detector stability from the exogenous-input Jacobian.
- Do not claim stochastic convergence from deterministic recurrence tests.
- Do not claim physical validation without raw reproducible physical evidence.
- Do not compare against PBFT/HotStuff as protocol-equivalent baselines unless an equivalent implementation and assumptions are present.
