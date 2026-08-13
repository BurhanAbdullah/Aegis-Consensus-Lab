# Unified State Model v1 — tag4

The final theory distinguishes deterministic protocol dynamics from stochastic detector evidence.

## State

s_k = [x_k, T_k, R_k, q_k]^T.

Physical measurement layer:

x_{k+1}=f(x_k,u_k,d_k)+w_k,

z_k=h(x_k)+v_k+a_k.

Detector layer produces evidence E_k from observable residual statistics. Conditional on a scenario, E_k may be stochastic because of measurement noise and detector randomness.

Trust:

T_{i,k+1}=Pi_[0,1]^m[T_{i,k}+rho_i(1-T_{i,k})-ell_i E_{i,k}T_{i,k}].

Risk:

R_{i,k+1}=Pi_[0,1][a_iR_{i,k}+(1-a_i)E_{i,k}+c_iD_{i,k}].

Influence:

G_{i,k}=tau_{i,k}Pi_[0,1](1-kappa R_{i,k}).

Quorum:

q_k=Pi_[q_min,q_max](q0+alpha_q(1-tau_bar,k)).

## Deterministic theorem case
For theorem derivations, E_k and D_k are treated as bounded exogenous sequences; stationary results additionally assume E_k=e and D_k=d. This prevents a deterministic fixed-point proof from being incorrectly applied to random evidence.

## Stochastic case
For experiments, E_k is generated from a fixed seed and measurement/attack scenario. Claims are then empirical or probabilistic. If a stochastic theorem is later desired, it must explicitly state the noise distribution, filtration, independence/mixing assumptions, and the stability notion (mean, mean-square, almost-sure, or high-probability).

## Main distinction
The paper must never use a single deterministic equilibrium equation as if it proves behavior under arbitrary random detector evidence. Deterministic analytical boundaries and stochastic empirical validation are separate layers.
