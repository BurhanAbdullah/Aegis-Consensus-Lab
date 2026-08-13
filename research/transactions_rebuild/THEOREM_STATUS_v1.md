# Theorem Status v1 — tag4

| Claim | Status | Reason |
|---|---|---|
| Weighted quorum intersection | PROVED | Inclusion-exclusion |
| Honest quorum intersection | PROVED | q>(1+b)/2 and Byzantine weight <=b |
| Certificate-level safety | PROVED | Honest non-equivocation + authenticated unique votes |
| Conservative availability | PROVED CONDITIONALLY | Requires q<=h; q<=1-b is sufficient if h>=1-b |
| Nonempty safety/availability interval | PROVED | Equivalent to b<1/3 |
| Trust equilibrium | PROVED for stationary interior scalar case | Fixed evidence e and no active projection |
| Scalar local stability | PROVED for reference case | |1-rho-ell e|<1 |
| Coupled trust-risk stability | PROVED CONDITIONALLY | Interior C1 map + Jury/spectral-radius condition |
| Predictive risk containment | PROVED CONDITIONALLY | Interior equilibrium requires (1-a)e+cd<1-a |
| Stochastic mean contraction | PROVED CONDITIONALLY | Exogenous bounded evidence + finite expectation; stronger mean-square claims need noise assumptions |
| Projected boundary convergence | NOT CLAIMED | Projection gives invariance, not convergence |
| Full PBFT liveness | NOT CLAIMED | Requires network/view-change assumptions |
| Detector correctness | NOT CLAIMED | Empirical/estimation property, not implied by quorum theorem |
| End-to-end cyber-physical resilience guarantee | NOT CLAIMED | Requires separate detector, attack, network and control assumptions |

## Reviewer discipline
Only claims marked PROVED may be written as unconditional theorem statements. Conditional results must retain their assumptions in the manuscript. Experimental observations must not be promoted to mathematical guarantees.
