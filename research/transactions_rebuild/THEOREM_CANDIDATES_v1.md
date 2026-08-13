# Theorem Candidates v1 — tag4

## Theorem 1 — Trust-state invariance
For any initial trust vector T_0 in [0,1]^m, the projected recursion T_{k+1}=Pi_[0,1]^m(G(T_k,e_k,r_k)) remains in [0,1]^m for all k.

Status: proof is immediate from the definition of Euclidean box projection. Publication requires the exact pre-projection map and all parameter domains to be stated.

## Theorem 2 — Scalar stationary trust equilibrium and convergence
For tau_{k+1}=Pi_[0,1](tau_k+rho(1-tau_k)-ell e tau_k), rho>=0, ell>=0, e in [0,1], the interior fixed point for rho+ell e>0 is tau*=rho/(rho+ell e). In the unclipped interior, local asymptotic stability is equivalent to |1-rho-ell e|<1, i.e. 0<rho+ell e<2.

Status: candidate theorem; boundary cases must be stated separately.

## Theorem 3 — Weighted-quorum safety
Assume total governance weight is normalized to 1, Byzantine validators have total weight at most b, validators may equivocate, and a quorum is any set of validators of total weight at least q. If 2q-1>b, any two quorums have an intersection containing positive honest weight; hence two conflicting quorum certificates cannot both be formed if honest validators sign at most one value per round.

Status: candidate theorem. The exact certificate/signing semantics must be formalized.

## Theorem 4 — Availability
If honest participating governance weight is at least 1-b, an honest quorum can be formed whenever q<=1-b.

Status: candidate theorem under synchronous/participation assumptions that must be explicit.

## Corollary — Nonempty safety/availability interval
Combining Theorems 3 and 4 yields a nonempty interval only when b<1/3:
(1+b)/2<q<=1-b.

## Theorem 5 — Coupled local stability
For the two-state interior map in COUPLED_JACOBIAN_v1.md, local asymptotic stability holds if the Jury inequalities are satisfied, equivalently all eigenvalues of the Jacobian lie inside the unit disk.

Status: candidate theorem. The final paper must substitute the actual E_tau and E_R expressions used by the implementation.

## Theorem 6 — Security–availability feasibility set
Under the assumptions of Theorems 3–5, the admissible operating set is
F={theta: spectral_radius(J(theta))<1 and (1+b)/2<q*(theta)<=1-b}.

Status: research-defining proposition/corollary. Empirical validation must estimate the same set independently.
