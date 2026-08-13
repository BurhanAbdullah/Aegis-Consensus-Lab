# Experimental Protocol v1 — tag4

## Goal
Validate the analytical feasible region independently of the implementation used to derive it.

## Factors
1. Byzantine governance weight b.
2. Base quorum q0.
3. Quorum adaptation gain alpha_q.
4. Recovery rho.
5. Degradation ell.
6. Risk memory a.
7. Risk gain c.
8. Risk attenuation kappa.
9. Attack intensity and persistence.
10. Network participation loss.

## Required experiment families
- No attack / nominal operation.
- Burst false-data injection.
- Slow-drift attack.
- Stealth attack.
- Equivocation.
- Mixed attack.
- Honest participation degradation.
- Byzantine-weight sweep.
- Recovery/degradation sweep.

## Baselines
At minimum compare:
1. Static PBFT 2f+1 / equivalent fixed threshold.
2. Fixed weighted quorum without prediction.
3. Adaptive trust without predictive risk.
4. Full tag4 model.

The baseline implementations must use the same scenario seeds and attack schedules.

## Primary metrics
Safety violation rate, liveness/finalization rate, false acceptance rate, false rejection rate, detection latency, mean quorum margin, minimum quorum margin, trust recovery time, and computational overhead.

## Theoretical validation
For each parameter point classify the analytical model as feasible/infeasible and independently classify the empirical protocol as safe-and-live/unsafe-or-unavailable. Report:
- true-safe rate
- false-safe rate
- true-unsafe rate
- false-unsafe rate
- boundary distance error
- confidence intervals over independent seeds.

## Reproducibility
Every run records seed, parameter vector, attack schedule, initial state, code commit, and full round-level trace. No figure may be populated from manually edited CSV values.
