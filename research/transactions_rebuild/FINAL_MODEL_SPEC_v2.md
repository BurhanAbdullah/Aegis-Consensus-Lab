# Final Model Specification v2 — tag4

## 1. State
For validator i at round k:
T_{i,k} in [0,1]^m is the trust vector.
tau_{i,k}=w^T T_{i,k}, w>=0, 1^T w=1.
R_{i,k} in [0,1] is predictive risk.
E_{i,k} in [0,1] is normalized validated detector evidence.

## 2. Trust update
T_{i,k+1}=Pi_[0,1]^m[T_{i,k}+rho_i(1-T_{i,k})-ell_i E_{i,k} T_{i,k}].

This is the canonical state transition. The scalar recurrence is its one-dimensional reference case.

## 3. Risk update
Use a bounded state equation rather than a thresholded heuristic:
R_{i,k+1}=Pi_[0,1][a_i R_{i,k}+(1-a_i) E_{i,k}+c_i D_{i,k}],
where D_{i,k} is a normalized temporal-drift indicator and a_i in [0,1].

The final implementation must define D from observable trace quantities only. Ground-truth attack labels are not allowed in R.

## 4. Governance influence
G_{i,k}=tau_{i,k} phi(R_{i,k}),
phi(R)=Pi_[0,1](1-kappa R), kappa>=0.

This gives explicit predictive attenuation and a differentiable interior map.

## 5. Active governance set
A_k={i:G_{i,k}>=g_min}. Total governance weight W_k=sum_{i in A_k}G_{i,k}.

## 6. Adaptive quorum
q_k=Pi_[q_min,q_max](q0+alpha_q(1-tau_bar,k)),
tau_bar,k=sum_i G_{i,k} tau_{i,k}/max(W_k,epsilon).

The threshold is Q_k=q_k W_k.

## 7. Certificate semantics
A prepare/commit certificate is a set of authenticated validator votes for the same (height, view, proposal hash) whose governance weight is at least Q_k. Each validator contributes at most once per phase and height/view/proposal context. Equivocation is slashable and an equivocating vote is not counted toward an honest certificate.

## 8. Adversarial model
Let total normalized governance weight be 1 and Byzantine governance weight be at most b. Byzantine validators may equivocate and coordinate. Honest validators sign at most one proposal per height/view/phase. Safety claims are conditional on these assumptions.

## 9. Safety and availability
Safety requires q_k>(1+b)/2.
Availability requires q_k<=h_k, where h_k is the honest participating governance weight. Under the conservative bound h_k>=1-b, availability follows if q_k<=1-b.

## 10. Coupled stability
Let x_k=(tau_bar,k,R_bar,k)^T. The final reduced map x_{k+1}=F(x_k) is evaluated at an interior equilibrium x*. Stability requires rho(J_F(x*))<1. For a two-state differentiable reduction the Jury conditions are used.

## 11. Main analytical object
The final paper studies the feasible set
F={theta: rho(J_F(theta))<1, (1+b)/2<q*(theta)<=h*}.

This set, rather than a single accuracy number, is the central security–availability result.

## 12. Experimental separation
The protocol is deterministic conditional on scenario inputs. Random attack generation and detector noise are external to the kernel and controlled by explicit seeds. Every experiment records the full trace needed to reproduce q, W, trust, risk, certificate weight, and finalization.
