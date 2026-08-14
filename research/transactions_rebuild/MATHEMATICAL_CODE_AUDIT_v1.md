# Mathematical–Code Audit v1 — tag4

## Purpose

This audit is a submission-integrity gate. A claim is promotable only when the equation, implementation, experiment, and reported result are mutually consistent.

## Canonical equations checked

### Trust

T⁺ = Pi_[0,1]^m[T + rho(1-T) - ell E T]

The production Python kernel implements this componentwise with projection after the update.

### Risk

R⁺ = Pi_[0,1][aR + (1-a)E + cD]

The production Python kernel implements this recurrence using the supplied detector evidence and drift. Risk is persistent in ValidatorState across calls to `step`.

### Governance influence

G = tau phi(R), phi(R)=Pi_[0,1](1-kappa R)

The production kernel computes this after the state update.

### Active set and total governance weight

A={i:G_i>=g_min}, W=sum_{i in A}G_i.

The production kernel applies the configured `g_min` threshold.

### Adaptive quorum

q=Pi_[q_min,q_max][q0+alpha_q(1-tau_bar)],

tau_bar=sum(G_i tau_i)/max(W,epsilon).

The production kernel implements this relation and Q=qW.

### Certificate safety

For normalized total weight 1, two q-quorums have intersection at least 2q-1. Honest intersection is guaranteed only when

2q-1>b,

with honest non-equivocation in the certificate context. Equality is not sufficient.

## Findings

### A. Core Python kernel

The current `AegisKernel` is structurally aligned with the final model specification for trust, risk, influence, active governance, adaptive quorum, and quorum threshold. The implementation is deterministic conditional on supplied evidence, drift, and vote maps.

### B. Independent reference model

The reference oracle reproduces the same core equations independently. One equivalence detail must be hardened: the reference active-set threshold should use the configured `params.g_min`, not a duplicated literal `1e-12`. This is a test-oracle correctness issue, not a scientific result, and must be corrected before claiming parameter-complete equivalence.

### C. Archived shell implementation

`archive/final_run/consensus_v4.sh` is not the canonical implementation of `FINAL_MODEL_SPEC_v2`. It uses integer heuristic trust components, shell `RANDOM`, hard-coded thresholds, and a non-persistent `PREV_CONFIDENCE` array. It therefore must not be cited as an implementation of the continuous trust-risk model or used as evidence for the analytical recurrence. It remains historical/legacy evidence only.

### D. Temporal prediction claim

The final model defines D as a normalized temporal-drift observable, but the archived shell implementation does not persist the previous confidence state across invocations. Therefore it does not implement a genuine C(t)-C(t-1) predictor. No manuscript claim may infer temporal predictive behavior from that shell implementation.

### E. Recovery-elasticity theorem

The affine trust recurrence has equilibrium

T*=rho/(rho+ell E)

for constant E with rho+ell E>0. Its interior scalar multiplier is

1-rho-ell E.

The ratio rho/(ell E) is not itself the local stability condition. Any Lambda-based statement must be explicitly derived for a different recurrence and must not be attributed to the affine model without proof.

### F. Experimental results

The archived phase-space CSVs are valid evidence for the reported 36 paired cells, but the old README headline values are inconsistent with those CSVs. The CSV-derived values must be treated as authoritative until the generation pipeline is independently reconstructed.

The 36-cell comparison does not establish a statistically significant global predictive improvement. It supports phase-dependent restructuring only.

### G. Physical-grid claim

The current repository artifacts do not constitute sufficient evidence for a universal 9,450-case physical AC-grid claim. That claim remains blocked unless the complete raw inputs, solver configuration, seeds, outputs, and reconstruction script are available and independently rerunnable.

## Mandatory pre-submission gates

1. Correct the independent oracle threshold parameterization.
2. Execute reference-vs-production equivalence tests over deterministic multi-round traces.
3. Separate canonical Python implementation from legacy shell experiments.
4. Reconstruct the experiment-generation pipeline from equations to CSV.
5. Recompute every headline number from generated artifacts.
6. Remove or label unsupported physical-grid claims.
7. Prove the final coupled Jacobian theorem under explicit interior assumptions.
8. Validate active-set and clipping boundary cases separately from interior analysis.
9. Add analytical-vs-empirical phase-boundary comparison.
10. Only then perform the manuscript-level equation/figure/table audit.

## Integrity rule

No number is to be changed merely to make a result look stronger. If source data contradict an old headline, the old headline is wrong or stale and must be corrected or removed. No fabricated experiment, seed, confidence interval, theorem verification, or physical-grid result is permitted.
