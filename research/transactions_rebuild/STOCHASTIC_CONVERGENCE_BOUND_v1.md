# Stochastic Evidence Convergence Bound v1 — tag4

## Purpose
Close the gap between the deterministic equilibrium theorem and the stochastic detector-evidence experiments without claiming an unjustified almost-sure convergence theorem.

## Assumptions
For the scalar trust recursion before projection,

τ_{k+1}=τ_k+ρ(1-τ_k)-ℓ e_k τ_k,

assume ρ>=0, ℓ>=0, e_k in [0,1], and let μ=E[e_k] when the expectation exists. For the simple conditional-mean analysis assume e_k is exogenous and independent of τ_k, with bounded support.

## Conditional mean recursion
Taking conditional expectation under the stated exogeneity assumption gives

E[τ_{k+1}|τ_k]
= [1-ρ-ℓμ]τ_k+ρ.

Therefore the mean equilibrium, when ρ+ℓμ>0, is

τ̄*=ρ/(ρ+ℓμ).

The mean recursion is contractive when

|1-ρ-ℓμ|<1,

or equivalently

0<ρ+ℓμ<2.

## Mean-square deviation bound
Let a=1-ρ-ℓμ and ξ_k=e_k-μ. Then

τ_{k+1}-τ̄*=a(τ_k-τ̄*)-ℓτ_k ξ_k.

A finite-variance bound requires an explicit noise assumption. If e_k has conditional variance bounded by σ_e^2 and τ_k∈[0,1], then the noise term has conditional second moment at most ℓ^2σ_e^2. A conservative recursion is

E[(τ_{k+1}-τ̄*)^2]
<= |a|^2 E[(τ_k-τ̄*)^2] + ℓ^2 σ_e^2 + cross-term contribution.

The cross term vanishes only under an appropriate martingale-difference/exogeneity assumption. Therefore the paper must state that assumption before using a geometric mean-square bound.

## Important limitation
This result establishes a conditional mean contraction and provides the route to a mean-square bound under additional noise assumptions. It does NOT prove almost-sure convergence of the projected stochastic process. Such a claim requires stronger stochastic-approximation/martingale assumptions and should not be inserted into the paper without a separate proof.

## Boundary/projection case
Because the implemented trust map clips to [0,1], the stochastic process is bounded. Boundedness is not equivalent to convergence. The final empirical study therefore reports stationary distributions, mean trajectories, and confidence intervals unless a stronger convergence theorem is separately proved.
