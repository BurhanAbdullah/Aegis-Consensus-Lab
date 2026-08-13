# Projection Boundary Stability Note v1 — tag4

The projected trust map is

T^+=Π_[0,1]^m(T+ρ(1-T)-ℓET).

Projection guarantees invariance of the state domain. It does not establish global convergence.

## Interior
Use the differentiable Jacobian and Jury/spectral-radius conditions.

## Lower boundary
If the unprojected update is nonpositive, the next state is exactly zero in that component. A local one-sided analysis is required to determine whether trajectories remain at the boundary or re-enter the interior.

## Upper boundary
If the unprojected update is at least one, the next state is exactly one in that component. Again, clipping alone does not establish attraction.

## Manuscript rule
Do not draw a smooth Jacobian phase boundary through clipping regimes. Mark projected/boundary regions separately in analytical figures.
