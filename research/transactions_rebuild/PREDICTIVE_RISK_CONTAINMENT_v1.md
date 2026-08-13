# Predictive-risk containment law — tag4

For the reduced risk state

`R_{k+1} = Pi_[0,1](a R_k + (1-a)e_k + c d_k)`,

with `0 <= a < 1`, `e_k,d_k in [0,1]`, the unconstrained fixed point for stationary inputs `(e,d)` is

`R* = e + c d/(1-a)`.

An interior equilibrium exists only when

`0 < e + c d/(1-a) < 1`.

Equivalently, the containment condition is

`(1-a)e + c d < 1-a`.

If this condition fails, the projected system reaches or approaches the
boundary `R=1`; the interior Jacobian theorem must not be applied there.

For the interior map, the risk eigenvalue is `a`. Thus risk-state local
stability requires `|a|<1`; under the model restriction `0<=a<1` this is
satisfied automatically.

The governance attenuation `phi(R)=1-kappa R` is strictly nonnegative on the
interior if `0<=kappa<=1`. If `kappa>1`, the projection creates a piecewise
map and the differentiable interior analysis no longer covers the entire
state space.

Therefore the analytical stability/feasibility gate must check both:

1. risk containment: `(1-a)e + c d < 1-a`;
2. interior attenuation: `0<=kappa<=1` (unless a separate piecewise proof is supplied).

Ground-truth attack labels do not enter the risk recursion.
