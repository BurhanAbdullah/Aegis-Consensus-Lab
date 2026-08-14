# Final Model Specification v2 — tag4 canonical

## 1. State
For validator i at round k:

- `T_{i,k} in [0,1]^m` is the trust vector.
- `tau_{i,k}=w^T T_{i,k}`, with `w>=0` and `1^T w=1`.
- `R_{i,k} in [0,1]` is predictive risk.
- `E_{i,k} in [0,1]` is normalized validated detector evidence.
- `D_{i,k} in [0,1]` is the observable temporal-drift indicator defined below.

The canonical state is `(T_i,R_i)`. Evidence and drift are exogenous inputs to the deterministic state transition; if a future model makes them endogenous, their generating state must be appended before differentiating the map.

## 2. Trust update

`T_{i,k+1}=Pi_[0,1]^m[T_{i,k}+rho_i(1-T_{i,k})-ell_i E_{i,k} T_{i,k}]`.

This is the canonical state transition. The scalar recurrence is its one-dimensional reference case.

For fixed exogenous `E_{i,k}=E_i`, every trust component has the same interior multiplier
`beta_i = 1-rho_i-ell_i E_i`.

## 3. Risk update

`R_{i,k+1}=Pi_[0,1][a_i R_{i,k}+(1-a_i)E_{i,k}+c_i D_{i,k}]`,

where `0<=a_i<1` and `c_i>=0`.

The risk map is closed on `[0,1]` provided

`(1-a_i)E_{i,k}+c_iD_{i,k} <= 1-a_i`.

This is the explicit risk-containment condition. Without it, the projection remains part of the implementation and the unclipped equilibrium/Jacobian theorem does not apply.

## 4. Observable drift definition

The temporal-drift input is not a ground-truth attack label. Let the normalized detector-score vector be

`d_{i,k}=(d^N_{i,k},d^C_{i,k},d^J_{i,k},d^R_{i,k}) in [0,1]^4`.

For `k>=1`, define

`D_{i,k}=Pi_[0,1]( ||d_{i,k}-d_{i,k-1}||_2 / 2 )`.

The denominator is `sqrt(4)=2`, so `D_{i,k}` is the normalized Euclidean change of the four observable detector channels. For the first round use `D_{i,0}=0` unless an explicitly supplied prior detector vector is available.

Thus `D_{i,k}` is fully observable from the detector trace and is independent of attack ground truth.

## 5. Governance influence

`G_{i,k}=tau_{i,k} phi(R_{i,k})`,

`phi(R)=Pi_[0,1](1-kappa R)`, `kappa>=0`.

## 6. Active governance set

`A_k={i:G_{i,k}>=g_min}` and `W_k=sum_{i in A_k}G_{i,k}`.

## 7. Adaptive quorum

`q_k=Pi_[q_min,q_max](q0+alpha_q(1-tau_bar,k))`,

`tau_bar,k=sum_i G_{i,k}tau_{i,k}/max(W_k,epsilon)`.

The threshold is `Q_k=q_k W_k`.

## 8. Certificate semantics

A prepare/commit certificate is a set of authenticated validator votes for the same `(height, view, phase, proposal hash)` whose governance weight is at least `Q_k`. Each validator contributes at most once per context. Honest validators sign at most one proposal per height/view/phase.

## 9. Adversarial model

Let normalized governance weight be one and Byzantine governance weight be at most `b`. Byzantine validators may equivocate and coordinate. Safety claims are conditional on honest non-equivocation and authenticated certificate context.

## 10. Safety and availability

Safety requires `q_k>(1+b)/2`.

Availability requires `q_k<=h_k`, where `h_k` is honest participating governance weight. The conservative sufficient condition is `q_k<=1-b` when `h_k>=1-b`.

## 11. Full interior Jacobian

For fixed exogenous `(E_i,D_i)`, the differentiable interior state is

`x_i=(T_{i,1},...,T_{i,m},R_i)^T`.

Its Jacobian is

`J_i = diag(beta_i I_m, a_i)`,

with `beta_i=1-rho_i-ell_iE_i`.

Hence

`rho(J_i)=max(|beta_i|,|a_i|)`.

The interior equilibrium is locally asymptotically stable iff

`|1-rho_i-ell_iE_i|<1` and `0<=a_i<1`.

For endogenous evidence/drift, the corresponding detector-state derivatives must be included; the exogenous-input result must not be presented as that stronger theorem.

## 12. Reduced coupled stability

For an explicit two-state differentiable reduction `x_k=(tau_bar,k,R_bar,k)^T`, evaluate `J_F(x*)` at an interior equilibrium. Stability requires `rho(J_F(x*))<1`. For a real 2x2 reduction the equivalent Jury conditions are

`1-tr(J)+det(J)>0`,
`1+tr(J)+det(J)>0`,
`1-det(J)>0`.

## 13. Security–availability operating set

The final analytical object is

`F={theta: rho(J_F(theta))<1 and (1+b)/2<q*(theta)<=h*}`.

The empirical study must compare observed safe/available outcomes against this analytical set. A visual phase plot alone is insufficient.

## 14. Experimental separation

The protocol is deterministic conditional on scenario inputs. Attack generation and detector noise are external and controlled by explicit seeds. Every experiment records the detector vector, normalized scores, `D`, evidence, trust, risk, governance weight, quorum, certificate weight, and finalization outcome.
