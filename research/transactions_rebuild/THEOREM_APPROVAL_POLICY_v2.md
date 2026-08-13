# AEGIS tag4 — Full Theorem Approval Policy v2

The completed AEGIS mathematical results are to be presented as **PROVED** theorems within their explicitly defined mathematical model. Model assumptions are part of each theorem statement and are not described as a weaker "conditionally proved" status.

## Approved theorem package

1. Weighted quorum intersection — PROVED.
2. Honest quorum intersection — PROVED for Byzantine governance weight bounded by b and q>(1+b)/2.
3. Certificate-level safety — PROVED for authenticated unique votes and honest non-equivocation.
4. Availability — PROVED when quorum weight does not exceed participating honest weight h.
5. Nonempty sufficient safety/availability interval — PROVED; it exists iff b<1/3.
6. Stationary interior trust equilibrium — PROVED.
7. Scalar local stability — PROVED for 0<rho+ell e<2.
8. Interior coupled trust-risk local stability — PROVED using the stated C1-map and Jury/spectral-radius theorem.
9. Predictive-risk containment — PROVED within the defined bounded-risk model and its interior-equilibrium domain.
10. Stochastic mean contraction — PROVED for the explicitly defined exogenous bounded-evidence stochastic model with finite mean.
11. Projected-state invariance — PROVED for projection onto [0,1]^m.

## Claims deliberately outside the theorem package

- Projected-boundary global convergence is not required for the main interior theorem.
- Full PBFT liveness is outside the present mathematical contribution.
- Detector correctness is evaluated experimentally rather than asserted as a theorem.
- Universal cyber-physical resilience is not claimed.

## Manuscript wording rule
Use **PROVED** for every item in the approved theorem package. State the mathematical assumptions as part of each theorem. Do not use the phrase "conditionally proved" for these completed results. Do not remove assumptions merely to make a theorem appear stronger than its actual scope.
