# Coupled Jacobian Analysis v1 — tag4

## 1. Reduced coupled map
For the first analytically tractable coupled system, define

e_k = E(R_k),
R_k = R(\tau_k),
\tau_{k+1}=F(\tau_k,R_k),
q_k=Q(\tau_k).

The canonical scalar trust map is
F(\tau,R)=\Pi_{[0,1]}[\tau+\rho(1-\tau)-\ell E(R)\tau].

Inside the unclipped interior,
F_\tau = 1-\rho-\ell E(R),
F_R=-\ell\tau E'(R).

If R=R(\tau), the reduced one-dimensional Jacobian is
J_{red}=1-\rho-\ell E(R)-\ell\tau E'(R)R'(\tau).

Local asymptotic stability requires |J_red|<1.

## 2. Explicit two-state formulation
To avoid hiding feedback inside E(R), use
R_{k+1}=aR_k+(1-a)E_k,
0<=a<1,
E_k=E(\tau_k,R_k).

Then the interior Jacobian at an equilibrium (tau*,R*) is
J = [[1-rho-ell E*, -ell tau* E_R*],
     [(1-a)E_tau*, a+(1-a)E_R*]].

The equilibrium is locally asymptotically stable when both eigenvalues of J lie strictly inside the unit disk. For a 2x2 real matrix J, this is equivalent to the Jury conditions:
1 - tr(J) + det(J) > 0,
1 + tr(J) + det(J) > 0,
1 - det(J) > 0.

These conditions are the formal stability gate for the coupled model.

## 3. Quorum coupling
For the unclipped quorum law
q*=q0+alpha_q(1-tau*),
its local sensitivity is
Dq/Dtau=-alpha_q.

Thus the governance controller is monotone decreasing in aggregate trust when alpha_q>0. Any manuscript claim about increased security from lowering trust must additionally establish that the resulting q remains feasible; otherwise adaptive hardening can destroy availability.

## 4. Security–availability feasibility
Under adversarial governance weight b, the candidate interval remains
(1+b)/2 < q* <= 1-b.

Substituting q* gives
(1+b)/2 < q0+alpha_q(1-tau*) <= 1-b.

For the stationary scalar trust equilibrium tau*=rho/(rho+ell e), this becomes
(1+b)/2 < q0+alpha_q ell e/(rho+ell e) <= 1-b.

This is an analytical phase-boundary candidate. It is not a theorem until the weighted-quorum adversary and participation assumptions are formally fixed.

## 5. Key research implication
The coupled analysis changes the contribution from a collection of mechanisms into a parameterized dynamical system. The main theoretical object is the feasible set
F={theta: spectral_radius(J(theta))<1 and (1+b)/2<q*(theta)<=1-b}.

The empirical study must estimate the boundary of F independently and compare it against the analytical boundary. The paper should report false-safe and false-unsafe classification rates of the analytical boundary, not merely visual agreement.
