# Coupled Trust–Risk Stability Proof v1 — tag4

## 1. Reduced interior map
Let
x_k=(tau_k,R_k)^T,

F_1(tau,R)=tau+rho(1-tau)-ell E(R)tau,
F_2(tau,R)=aR+(1-a)E(tau,R)+cD(tau,R).

The projection operators are inactive in the interior theorem. The final projected system is treated separately as a bounded state map.

## 2. Jacobian
At an interior equilibrium x*=(tau*,R*),

J = [[1-rho-ell E*, -ell tau* E_R*],
     [(1-a)E_tau*+cD_tau*, a+(1-a)E_R*+cD_R*]].

## 3. Local stability theorem
If F is continuously differentiable in a neighborhood of x* and every eigenvalue of J(x*) has modulus strictly below one, then x* is locally asymptotically stable for the discrete-time system x_{k+1}=F(x_k).

For a real 2x2 Jacobian, this is equivalent to the Jury inequalities:

1 - tr(J) + det(J) > 0,
1 + tr(J) + det(J) > 0,
1 - det(J) > 0.

This is the theorem used by the tag4 reduced model.

## 4. Scalar reference corollary
If E is held constant at e and D is constant at d, then E_tau=E_R=D_tau=D_R=0. The trust eigenvalue reduces to

lambda_tau=1-rho-ell e,

and the risk eigenvalue reduces to

lambda_R=a.

Thus the uncoupled reference system is locally asymptotically stable whenever

0<rho+ell e<2,
0<=a<1.

## 5. Coupled-feedback interpretation
When E or D depends on tau/R, cross terms change the eigenvalues. Therefore the scalar condition 0<rho+ell e<2 is NOT sufficient for the full coupled model. The paper must use the coupled Jacobian whenever endogenous feedback is claimed.

## 6. Projection boundary
The clipped map is globally bounded in its declared state domain by construction, but clipping makes the map piecewise differentiable. A local smooth stability theorem cannot automatically be extended across an active clipping boundary. Boundary equilibria require a separate one-sided/piecewise analysis or a contraction argument.

## 7. Research claim permitted
The rigorous claim is therefore: interior equilibria satisfying the stated differentiability assumptions and Jury conditions are locally asymptotically stable. The bounded projection guarantees state-domain invariance, not convergence by itself.
