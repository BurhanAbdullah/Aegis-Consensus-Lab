# AEGIS tag4 — Transactions Strict Validation Protocol

## Purpose

This document defines the release-gated validation protocol for the Transactions-targeted tag4 rebuild. No manuscript claim is accepted unless it is supported by the canonical mathematical model, executable implementation, and an independently reproducible validation result.

## 1. Canonical mathematical contract

The authoritative state is `x_i=(T_{i,1},...,T_{i,m},R_i)`. Evidence `E_i` and observable detector drift `D_i` are exogenous inputs unless their generating dynamics are explicitly appended to the state.

Trust:

`T^+ = Pi_[0,1]^m[T + rho(1-T) - ell E T]`.

Risk:

`R^+ = Pi_[0,1][aR+(1-a)E+cD]`.

Governance influence:

`G=tau phi(R)`, with `tau=w^T T` and `phi(R)=Pi_[0,1](1-kappa R)`.

Adaptive quorum:

`q=Pi_[q_min,q_max](q0+alpha_q(1-tau_bar))`.

The safety/availability operating condition is tested as

`(1+b)/2 < q <= h`.

For the unclipped interior model, the exact Jacobian is

`J=diag(beta I_m,a)`, `beta=1-rho-ell E`,

and local asymptotic stability requires `rho(J)<1`.

## 2. Mathematical validation layers

### Layer A — symbolic/reference identities

Verify closed-form equilibrium, Jacobian entries, spectral radius, governance/quorum equations, and certificate boundary identities against independently written reference expressions.

### Layer B — numerical finite-difference cross-validation

For randomly sampled interior parameter points, compare the analytical Jacobian with a central finite-difference Jacobian. The relative Frobenius error must remain below the configured numerical tolerance.

### Layer C — equilibrium residual validation

For every sampled contained equilibrium, evaluate `||F(x*)-x*||_inf`. The residual must be below tolerance.

### Layer D — stability cross-check

Compare analytical spectral-radius classification with direct eigenvalue computation and, for the 2-D reduction, with all three Jury inequalities. No disagreement is permitted away from numerical boundary cases.

### Layer E — boundary validation

Sweep the security/availability boundary and separately record points numerically indistinguishable from equality. Strict inequalities must never be converted into non-strict claims.

### Layer F — implementation/model equivalence

The executable canonical kernel must reproduce the mathematical reference transition for homogeneous-parameter interior cases. Projection-active cases are validated separately and are not used to justify interior differentiability claims.

### Layer G — stochastic reproducibility

All empirical comparisons use frozen scenario definitions and explicit seeds. Repeated generation must be byte-identical for deterministic artifacts. Seed-level uncertainty is reported separately from deterministic mathematical validation.

### Layer H — comparative validation

Compare AEGIS against fixed quorum baselines under identical traces, attack sets, evidence levels, drift levels, seeds, and rounds. The comparator is a mathematical reference policy and is not described as PBFT/HotStuff unless an actual protocol-level theorem is established.

### Layer I — ablation validation

Remove one governance component at a time and report both availability and analytical safety-boundary metrics. No component is declared necessary using availability alone.

### Layer J — localization validation

Run all designated validator locations and evidence/drift levels. Localization results measure state/influence response; they do not imply attack attribution accuracy unless attribution labels and a separate attribution metric are supplied.

## 3. Transactions claim discipline

The paper must not claim:

- classical PBFT/HotStuff safety or performance without protocol-equivalent assumptions and proofs;
- topology attacks when only measurements or certificates are manipulated;
- unconditional resilience;
- an attack-detection accuracy metric from influence attenuation alone;
- an interior Jacobian theorem when projection is active;
- an endogenous-detector stability theorem from an exogenous-input Jacobian;
- numerical results not regenerated from the frozen release artifacts.

## 4. Release gates

A release candidate is blocked unless all of the following are green:

1. unit/property tests;
2. equilibrium residual tests;
3. analytical-vs-finite-difference Jacobian cross-validation;
4. spectral-radius/Jury agreement;
5. safety/availability boundary agreement;
6. canonical-kernel/model equivalence;
7. deterministic repeated-run identity;
8. dual fixed-quorum comparison;
9. ablation and localization sweeps;
10. publication-artifact generation;
11. manuscript-to-artifact numerical audit;
12. independent Transactions reviewer audit.

The final manuscript, experiment configuration, CSV artifacts, figures, tests, and commit must form one frozen provenance chain.