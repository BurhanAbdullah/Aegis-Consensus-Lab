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
| Coupled trust-risk stability | PENDING FINAL REVIEW | Requires final reduced map and parameter domain |
| Predictive risk containment | PENDING FINAL REVIEW | Need final assumptions and projection/boundary treatment |
| Full PBFT liveness | NOT CLAIMED | Requires network/view-change assumptions |
| Detector correctness | NOT CLAIMED | Empirical/estimation property, not implied by quorum theorem |

## Reviewer discipline
Only claims marked PROVED may be written as unconditional theorem statements. Conditional results must retain their assumptions in the manuscript. Experimental observations must not be promoted to mathematical guarantees.
