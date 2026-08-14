# Aegis Transactions Rebuild — tag4

## Objective
Rebuild the Aegis research artifact and manuscript into a mathematically rigorous, reproducible, and defensible IEEE Transactions-level study.

## Serial checklist

- [x] Create isolated `tag4` working ref.
- [x] Preserve existing research branches and `main`.
- [x] Audit current repository structure and identify legacy/placeholder artifacts.
- [x] Identify current manuscript/repository consistency risks from prior review.
- [ ] Freeze final research question.
- [ ] Freeze exact contribution claims.
- [x] Freeze terminology and threat-model scope for the canonical model: weighted certificates, authenticated context, honest non-equivocation; no PBFT/HotStuff theorem claim.
- [x] Rebuild the unified cyber-physical + governance mathematical reference model.
- [x] Separate trust state from governance-risk attenuation.
- [x] Define multidimensional trust dynamics rigorously.
- [x] Define predictive risk containment mathematically, including the explicit condition under which the unclipped recurrence is valid.
- [x] Define weighted/adaptive quorum mathematically.
- [x] Establish trust-state invariance through projection tests.
- [x] Establish scalar equilibrium existence/characterization and executable closed-form reference.
- [x] Establish interior local stability through the Jacobian/spectral-radius condition and independent Jury cross-checks.
- [x] Derive the governance feasibility/security-availability condition and the strict quorum boundary.
- [x] Align the canonical reference kernel with the frozen equations for the homogeneous-parameter implementation case.
- [x] Add unit tests for mathematical components.
- [x] Freeze experiment configuration and random seeds for the six-scenario benchmark.
- [x] Rebuild deterministic scenario coverage: clean, burst, slow-drift, stealth, equivocation, mixed.
- [ ] Rebuild localization experiments across multiple attack locations/magnitudes.
- [x] Add a fixed weighted-quorum reference comparator; it is explicitly not labeled PBFT/HotStuff.
- [ ] Add stronger governance baselines beyond the fixed-quorum reference.
- [ ] Add ablation studies.
- [x] Add parameter/boundary sensitivity through the analytical grid sweep.
- [x] Add seed-level uncertainty infrastructure to the fixed-quorum comparison.
- [x] Add analytical-vs-kernel phase-boundary cross-validation over 1,911 deterministic parameter cases; exact-boundary cases are reported separately because strict inequalities are numerically sensitive.
- [ ] Generate final publication-quality analytical-vs-empirical phase-boundary figures.
- [ ] Resolve every manuscript-vs-repository numerical discrepancy.
- [ ] Build one-command reproducibility pipeline that includes the final boundary sweep and manuscript artifacts.
- [ ] Clean legacy/placeholder research artifacts from the final release path.
- [ ] Rewrite Methods/Theory/Results around the verified model.
- [ ] Rewrite Introduction/Related Work/Abstract/Conclusion.
- [ ] Perform equation, dimensional, statistical, citation, and reproducibility audits.
- [ ] Perform simulated Transactions Reviewer #1/#2/editor audit.
- [ ] Mark `tag4` submission-ready only after all gates pass.

## Current verification checkpoint

- Canonical PR CI on the merge ref: **PASS**.
- Latest validated branch head: `d577b3079885c708fcbc3efb060462ff00b8e449`.
- Latest GitHub Actions run validated the full canonical test suite, the deterministic six-scenario benchmark, the fixed-quorum comparator, and the analytical boundary sweep.
- The immediately preceding full test run reported **95 passed, 0 failed**; the final CI run also completed successfully.
- The canonical benchmark contains 6 scenarios × 10 seeds × 30 rounds = **1,800 rows** and is byte-for-byte deterministic across repeated generation.
- The analytical boundary sweep contains **1,911 cases**; independent local execution found maximum equilibrium error below `1.2e-14`, maximum quorum error below `2.4e-15`, and zero analytical/empirical classification mismatches away from strict numerical boundary cases. There were 33 grid points within the explicit boundary tolerance and those are not silently classified as exact interior points.
- Exhaustive discrete quorum adversarial tests confirm the strict boundary: equality can admit conflicting certificates, while thresholds strictly above `(1+b)/2` eliminate the tested conflicting pairs under honest non-equivocation.
- The current branch remains a draft validation vehicle and is **not merged, tagged, or submission-ready**.

## Non-negotiable gates

1. Every headline number in the paper must be generated from repository artifacts.
2. Every theorem must follow from explicitly stated assumptions.
3. Every major equation must have an identifiable implementation/test counterpart.
4. No unsupported Byzantine/PBFT safety claims.
5. No "topology attack" terminology unless topology is actually modified.
6. No "resilience" claim unless the metric and definition are explicit.
7. The final manuscript and repository must correspond to a frozen commit.
