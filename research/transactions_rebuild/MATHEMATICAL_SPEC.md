# Mathematical Specification — Work in Progress

This document is the canonical target specification for the mathematical rebuild. It is intentionally not marked complete until the equations are derived, dimension-checked, and mapped to code.

## 1. Cyber-physical measurement model
Use an explicit state/measurement model of the form

x_{k+1}=f(x_k,u_k,d_k)+w_k,

z_k=h(x_k)+v_k+a_k,

where x is the electrical state, u controls/inputs, d disturbances, w process noise, v measurement noise, and a the adversarial measurement perturbation.

For a DC/quasi-static benchmark, define the reference-bus convention and reduced state dimension explicitly rather than using an unconstrained full angle vector.

## 2. Detector statistics
Define the innovation

nu_k = z_k - h(xhat_{k|k-1}),

and innovation covariance

S_k = H_k P_{k|k-1} H_k^T + R.

Define NIS by

NIS_k = nu_k^T S_k^{-1} nu_k,

with numerical implementation using a linear solve/factorization rather than explicit matrix inversion.

Define the sequential change statistic and a separately named innovation-volatility statistic. Their assumptions, thresholds, and training/calibration procedure must be explicit.

## 3. Multidimensional trust
For validator i define

T_{i,k} = [C_{i,k}, B_{i,k}, L_{i,k}, S_{i,k}]^T in [0,1]^4,

or a justified general m-dimensional version. Aggregate trust only with an explicitly defined weight vector w satisfying w >= 0 and 1^T w = 1:

bar{T}_{i,k}=w^T T_{i,k}.

## 4. Risk
Risk must distinguish low trust from internal inconsistency. A candidate structure is

R_{i,k}=alpha(1-bar{T}_{i,k}) + beta V_{i,k} + gamma O_{i,k} + delta D_{i,k},

where V is trust volatility, O is detector/observation evidence, and D is temporal degradation. Final terms and normalizations require derivation/experimental justification.

## 5. Trust dynamics
The trust-state recursion must be explicit and bounded, e.g.

T_{i,k+1}=Pi_[0,1]^4(T_{i,k}+U_{i,k}-P_{i,k}),

where U is recovery/update and P is degradation/slashing. The exact forms must be derived from the intended protocol. If predictive risk containment changes governance influence only, it must not appear as an unannounced direct subtraction from T.

## 6. Governance influence / PRC
Define an influence multiplier phi(R) in [0,1] and governance weight

G_{i,k}=bar{T}_{i,k} phi(R_{i,k}).

The piecewise/continuous form, monotonicity, saturation, and threshold behavior must be specified and analyzed.

## 7. Adaptive quorum
Define the quorum rule over governance weights, for example

Q_k = clip(Q_0 + alpha_Q(1-bar{T}_k), Q_min, Q_max),

and define the decision condition directly in terms of weighted affirmative influence:

sum_i G_{i,k} v_{i,k} >= Q_k sum_i G_{i,k}.

No PBFT/Byzantine safety guarantee is claimed until a weighted quorum-intersection proof is supplied under explicit assumptions.

## 8. Unified state map
The final governance dynamics should be represented as

s_{k+1}=F(s_k, y_k, a_k, eta_k),

with s containing the electrical/detector/governance state required for the claimed theorems. The Jacobian J_F(s*) and the conditions for local stability must be derived from this map.

## 9. Intended analytical boundary
The final theory should identify a feasible region satisfying both trust recovery and quorum feasibility. Candidate conditions include a positive equilibrium trust/influence condition and a quorum-achievability inequality. The final result must be derived, not assumed.

## Completion gate
This specification is complete only when:
- every symbol has one definition;
- all matrix dimensions are explicit;
- the reference/slack state is handled correctly;
- trust and influence are mathematically separated;
- equilibrium equations are solved under explicit assumptions;
- stability follows from a stated theorem/proposition;
- code implements the exact equations;
- tests verify the key invariants.
