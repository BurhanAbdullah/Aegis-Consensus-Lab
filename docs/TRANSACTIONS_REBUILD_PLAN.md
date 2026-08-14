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
- [x] Rebuild localization experiments across four attack locations and five magnitudes/four drift levels.
- [x] Add static weighted-quorum reference comparators at `q=0.67` and `q=0.75`; neither is labeled PBFT/HotStuff.
- [x] Add ablation studies.
- [x] Add parameter/boundary sensitivity through the analytical grid sweep.
- [x] Add seed-level uncertainty infrastructure to the comparative experiments.
- [x] Add analytical-vs-kernel phase-boundary cross-validation over 1,911 deterministic parameter cases; exact-boundary cases are reported separately because strict inequalities are numerically sensitive.
- [x] Generate publication-quality comparative figures for both static baselines, ablations, safety boundary, and localization from frozen CSV artifacts.
- [x] Build one-command reproducibility pipeline for all current experiments and figures.
- [x] Add explicit Transactions reviewer audit and release guardrails.
- [ ] Resolve every manuscript-vs-repository numerical discrepancy.
- [ ] Clean legacy/placeholder research artifacts from the final release path.
- [ ] Rewrite Methods/Theory/Results around the verified model.
- [ ] Rewrite Introduction/Related Work/Abstract/Conclusion.
- [ ] Perform equation, dimensional, statistical, citation, and reproducibility audits on the final manuscript.
- [ ] Perform simulated Transactions Reviewer #1/#2/editor audit on the final manuscript.
- [ ] Freeze final research question and contribution claims after manuscript reconciliation.
- [ ] Mark `tag4` submission-ready only after all manuscript gates pass.

## Current verification checkpoint

- Latest completed PR validation run: **PASS** on merge ref `67a83c589687abb739e33ef49550d9ba44e3ebff`.
- All validation stages passed, including the updated dual-baseline publication figures.
- The canonical benchmark remains 6 scenarios × 10 seeds × 30 rounds = **1,800 deterministic rows**, byte-for-byte identical across repeated generation.
- Analytical boundary sweep remains **1,911 cases**, with maximum equilibrium error approximately `1.1768e-14` and maximum quorum error approximately `2.3315e-15`; 33 boundary-near cases are explicitly separated.
- Comparative stress grid: **4,200 rows**, all 14 single/pair/triple attack sets × 6 evidence levels × 5 drift levels × 10 seeds. The previously established q=0.67 mean AEGIS advantage is approximately 0.05345 with 95% CI approximately 0.05018–0.05672; the two-validator stratum is approximately 0.12472 with 95% CI approximately 0.11845–0.13099. The stricter q=0.75 baseline is now generated from the same traces and is separately reported.
- Ablation: 50 rows with attack-period availability, unsafe-certificate-boundary fraction, and safety margin.
- Localization: 800 rows across four validator locations, five evidence magnitudes, four drift levels, and ten seeds; both risk activation and influence reduction are reported.
- Publication figures are generated for q=0.67 and q=0.75 comparisons, component availability, component safety boundary, and attack localization.
- The current computational artifact is green, but it is still a **validation branch**, not a submission release.

## Scientific interpretation guardrails

1. The strongest comparative result is an availability result under the tested two-validator commit-withholding regime. It is not a blanket resilience claim.
2. Static quorum comparators are mathematical reference policies, not PBFT/HotStuff implementations.
3. The safety result must be stated through the explicit certificate-boundary condition `q > (1+b)/2` under the stated honest non-equivocation assumptions.
4. The six nominal scenarios alone do not establish superiority; stress-grid, ablation, localization, and analytical-boundary evidence are required.
5. Localization demonstrates state/influence response across locations; it does not by itself prove attack attribution accuracy.
6. Every headline paper number must be regenerated from the frozen repository artifacts before submission.
7. The old unsupported 9,450-case physical-system claim remains excluded.

## Remaining hard blockers

1. **Manuscript reconciliation:** the current GitHub validation branch does not contain the final manuscript source needed to reconcile every paper number, equation reference, figure, table, and claim.
2. **Final contribution freeze:** exact claims must be fixed only after manuscript reconciliation.
3. **Final statistical audit:** choose the final estimands, confidence intervals, and multiple-comparison treatment before writing Results.
4. **Transactions manuscript audit:** theorem assumptions, threat model, novelty positioning, citations, and claim strength must be checked against the actual final manuscript.
5. **Release cleanup:** quarantine/remove legacy placeholders from the submission path and freeze the exact experiment+manuscript commit.

## Non-negotiable gates

1. Every headline number in the paper must be generated from repository artifacts.
2. Every theorem must follow from explicitly stated assumptions.
3. Every major equation must have an identifiable implementation/test counterpart.
4. No unsupported Byzantine/PBFT safety claims.
5. No "topology attack" terminology unless topology is actually modified.
6. No "resilience" claim unless the metric and definition are explicit.
7. The final manuscript and repository must correspond to a frozen commit.
8. No submission-ready label until the manuscript-level reviewer audit passes.
