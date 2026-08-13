# Transactions Rebuild — Research Design Freeze

## Central research question
Under what conditions can predictive trust adaptation improve cyber-physical false-data attack governance while preserving consensus availability, and can the resulting security–availability boundary be analytically characterized and experimentally validated?

## Core hypothesis
Predictive trust attenuation is not universally beneficial. Its effect depends on the balance among trust recovery, trust degradation/slashing, risk attenuation strength, and quorum adaptation. There exists a feasible parameter region in which anomaly containment is improved without making the weighted quorum infeasible.

## Proposed contribution set
1. A cyber-physical detection layer combining normalized innovation squared (NIS), sequential CUSUM, and innovation-volatility features for attack detection and localization.
2. A multidimensional validator-trust state that separates trust level from risk/volatility rather than treating reputation as a single undifferentiated scalar.
3. A predictive risk-containment mechanism that maps detector/governance evidence to validator influence attenuation, explicitly separated from the underlying trust-state recursion.
4. A mathematically defined adaptive weighted-quorum dynamical system with equilibrium, local-stability, and quorum-feasibility analysis.
5. An analytical-versus-empirical characterization of the security–availability boundary and its sensitivity to recovery, slashing, attenuation, and risk-threshold parameters.

## Terminology freeze
- Primary cyber attack term: false-data injection attack (FDIA) / measurement attack. Do not call a measurement attack a topology attack unless the network topology itself is modified.
- Consensus performance metric: consensus survivability/availability unless a formal resilience definition is supplied.
- Governance mechanism: trust-adaptive predictive governance.
- Trust attenuation: modification of governance influence; it must not silently alter the trust state unless the state equation explicitly defines that coupling.

## Mathematical architecture to be developed
Electrical/measurement state:
  x_{k+1} = f(x_k,u_k,d_k) + w_k
  z_k = h(x_k) + v_k + a_k

Validator trust state:
  T_{i,k} in [0,1]^m

Risk state:
  R_{i,k} = r(T_{i,k}, detector evidence, temporal evidence)

Governance influence:
  G_{i,k} = g(T_{i,k},R_{i,k})

Adaptive quorum:
  Q_k = q({G_{i,k}})

Consensus transition:
  s_{k+1} = F(s_k, z_k, a_k, eta_k)

The final paper must instantiate these equations completely, define every variable and assumption, and prove only claims that follow from them.

## Intended theoretical results
- Trust-state invariance/boundedness.
- Existence and characterization of stationary trust equilibrium under explicit stationary assumptions.
- Local stability using the Jacobian/spectral-radius condition where differentiability permits.
- Quorum-feasibility condition linking equilibrium trust/influence to the adaptive threshold.
- A security–availability feasible-region/boundary result; no unconditional 'resilience theorem' unless the assumptions support it.

## Experimental design principle
All reported values must be generated from the final implementation and committed result artifacts. Manuscript tables and figures will not contain hand-entered values. The repository will record the exact commit/configuration used for the final paper.
