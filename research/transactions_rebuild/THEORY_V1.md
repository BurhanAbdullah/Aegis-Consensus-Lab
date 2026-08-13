# Theory V1 — Candidate Transactions-Level Core

## Purpose
This is the first explicit analytical model proposed for the rebuild. It replaces the previously unsupported universal recovery-ratio claim with a recurrence-specific result and a weighted-quorum feasibility result.

## A. Scalar aggregate trust dynamics
For the theorem layer, let t_k in [0,1] denote the aggregate normalized trust of an honest validator population under a stationary operating regime. Define recovery toward unit trust and proportional degradation by

 t_{k+1} = Pi_[0,1]( t_k + rho(1-t_k) - ell t_k ),

where rho >= 0 is the recovery coefficient and ell >= 0 is the stationary degradation coefficient.

Before projection,

 t_{k+1} = rho + (1-rho-ell)t_k.

### Proposition 1 — Equilibrium and local/global convergence
If rho + ell > 0, the unique unconstrained fixed point is

 t* = rho/(rho+ell).

For 0 <= rho,ell <= 1, the fixed point belongs to [0,1] and the recurrence is globally convergent because

 |1-rho-ell| < 1

whenever 0 < rho+ell < 2. With the stated parameter bounds, this condition holds except the degenerate endpoint rho=ell=0. If rho>0, then t*>0; if ell>0, then t*<1.

This result shows that a ratio Lambda=rho/ell is not, by itself, a universal necessary-and-sufficient condition for positive asymptotic trust. The threshold depends on the actual recurrence.

## B. Trust-weighted governance influence
For validator i, retain the multidimensional state

 T_i,k = [C_i,k, B_i,k, L_i,k, S_i,k]^T,

with normalized aggregate trust

 t_i,k = w^T T_i,k,

where w >= 0 and 1^T w = 1.

Define a risk score r_i,k separately from trust. Governance influence is

 g_i,k = t_i,k phi(r_i,k),

where 0 <= phi(r) <= 1 is non-increasing in r. This separation is mandatory: risk containment changes influence unless an explicit alternative trust-state coupling is defined.

## C. Weighted quorum safety/liveness window
Let W be total active governance weight and let b in [0,1) be the adversarial governance-weight fraction. A quorum threshold q is defined as a fraction of W.

### Lemma 2 — Weighted quorum intersection
Any two quorums each carrying at least qW weight have intersection weight at least

 (2q-1)W.

If adversarial weight is at most bW, a sufficient condition for every two quorums to share positive honest weight is

 q > (1+b)/2.

### Lemma 3 — Honest liveness
If honest validators hold at least (1-b)W total active weight, an honest decision can reach quorum whenever

 q <= 1-b.

### Theorem 4 — Weighted quorum feasibility region
A non-empty safety-and-liveness interval exists when

 (1+b)/2 < q <= 1-b,

which is feasible if and only if

 b < 1/3.

This recovers the classical one-third boundary as a special case while expressing it in governance-weight rather than validator-count terms. The theorem does not claim that arbitrary trust weighting automatically satisfies the assumptions; the adversarial weight bound b must be independently established or bounded.

## D. Adaptive quorum and security–availability boundary
Use

 q* = clip(q0 + alpha_q(1-t*), q_min, q_max).

For the unclipped regime and the equilibrium above,

 q* = q0 + alpha_q ell/(rho+ell).

Therefore the feasible security–availability region is defined by

 (1+b)/2 < q0 + alpha_q ell/(rho+ell) <= 1-b.

This is the central analytical boundary candidate for the paper. It links recovery rho, degradation ell, quorum adaptation alpha_q, baseline quorum q0, and adversarial weight b.

## E. Interpretation
Increasing degradation ell lowers t* and therefore raises adaptive quorum q*. This can improve safety against low-trust participants but can eventually violate the liveness upper bound q <= 1-b. Increasing recovery rho raises t* and lowers the adaptive quorum, improving availability, provided the influence/risk layer does not independently suppress honest weight.

This creates the intended security–availability tradeoff and gives the empirical phase-space experiments a precise analytical target.

## F. Required proof/implementation gates
This candidate theory is not yet final. Before it is promoted to the manuscript:
1. Verify the exact implemented trust update against the recurrence.
2. Define the mapping from the four-dimensional trust vector to t and establish its invariance.
3. Define the risk/influence function phi and analyze its effect on adversarial weight b and honest active weight.
4. Handle quorum clipping explicitly; the boundary above applies only to the unclipped regime.
5. Extend the homogeneous scalar result to heterogeneous validator weights if the experiments use heterogeneous trust.
6. Add a formal theorem for the coupled trust-risk-quorum map only if its assumptions can be satisfied by the implementation.
7. Validate the analytical boundary against independent Monte Carlo phase-space experiments.
