# Proof obligations — tag4

These are mandatory gates before any theoretical claim is promoted into the manuscript.

## P1 — Trust invariance
For T in [0,1]^m and projection Pi_[0,1]^m, show T^+ remains in [0,1]^m.

## P2 — Scalar equilibrium
For tau^+=Pi_[0,1](tau+rho(1-tau)-ell e tau), rho>=0, ell>=0, e in [0,1], derive the fixed point and identify boundary cases rho=0 and ell e=0.

## P3 — Stability
For the unclipped interior recurrence, derive the multiplier 1-rho-ell e and state exact conditions for asymptotic convergence. Do not substitute a ratio condition for the actual Jacobian condition.

## P4 — Weighted quorum intersection
Formalize validator weights, adversarial weight budget b, quorum fraction q, and whether Byzantine validators may equivocate. Prove the minimum intersection weight of two quorums and identify the condition under which that intersection contains honest weight.

## P5 — Availability
Define the honest participating weight and derive the exact condition for an honest quorum to be achievable.

## P6 — Coupled map
If risk and quorum depend on trust, derive the Jacobian of the coupled map and determine whether the trust equilibrium remains locally stable after coupling.

## P7 — Stochastic detector evidence
If e_k is random, replace deterministic equilibrium claims with expectation/stochastic stability claims unless e_k is explicitly held stationary for a deterministic theorem.

## P8 — Empirical validation
Every theoretical boundary must be plotted against independently generated simulation points. Agreement/disagreement must be reported quantitatively, not visually asserted.
