# Analytical Boundary v1 — tag4

## Scalar reference boundary
For stationary detector evidence e, trust equilibrium is

tau* = rho/(rho + ell e),

and unclipped adaptive quorum is

q* = q0 + alpha_q ell e/(rho + ell e).

The safety/availability conditions are

(1+b)/2 < q* <= 1-b.

## Interpretation
The lower inequality imposes sufficient weighted quorum intersection under the stated Byzantine-weight model. The upper inequality prevents the threshold from exceeding the conservative honest-weight bound.

## Boundary equations
The safety boundary satisfies

q0 + alpha_q ell e/(rho + ell e) = (1+b)/2.

The availability boundary satisfies

q0 + alpha_q ell e/(rho + ell e) = 1-b.

These equations can be solved for any one parameter conditional on the others. For example, with alpha_q > 0 and fixed q0,b, the ratio

r = ell e/rho

satisfies

r = (q_boundary-q0)/(alpha_q-(q_boundary-q0))

whenever the denominator is positive.

## Stability overlay
The scalar trust multiplier is

J_tau = 1-rho-ell e.

The reference trust dynamics are locally asymptotically stable when

0 < rho + ell e < 2.

The final analytical operating region is therefore the intersection of the quorum-feasibility interval and the trust-stability interval. For the full two-state risk/trust model, replace this scalar condition with rho(J_F)<1.

## Validation requirement
The empirical study must sweep parameters across both sides of each analytical boundary and report confusion rates for analytical classification versus observed safe-and-live behavior. The figure must distinguish points used for model construction from independent validation points.
