# Validation Gates v1 — tag4

The rebuild cannot advance to manuscript rewriting until all gates below pass.

## Gate A — Equation equivalence
Reference equations and production kernel agree on fixed deterministic traces to numerical tolerance.

## Gate B — Domain invariance
Trust, risk, influence and quorum remain in declared domains for all tested parameter boundaries.

## Gate C — Determinism
Same seed + scenario + parameters => identical trace.

## Gate D — Safety
Under theorem assumptions, no conflicting finalization is observed. Deliberately test adversarial boundary cases.

## Gate E — Availability
Under declared honest participation, valid proposals finalize whenever q <= h.

## Gate F — Boundary fidelity
Analytical safe/unsafe classification is compared with independent simulation. Report false-safe and false-unsafe rates.

## Gate G — Robustness
Main conclusions survive parameter sweeps, attack durations, detector noise and independent seeds.

## Gate H — Baseline fairness
Every baseline uses identical scenario inputs, seeds, observation budget and stopping criteria.

## Gate I — Statistical reporting
Headline metrics include uncertainty intervals and sample counts.

## Gate J — Manuscript consistency
Every number, equation, figure and table can be traced to a generated artifact and current commit.
