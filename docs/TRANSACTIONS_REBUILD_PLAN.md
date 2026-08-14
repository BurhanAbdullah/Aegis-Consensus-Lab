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
- [x] Add a fixed weighted-quorum reference comparator; it is explicitly not labeled PBFT/HotStuff.
- [ ] Add stronger governance baselines beyond the fixed-quorum reference.
- [x] Add ablation studies.
- [x] Add parameter/boundary sensitivity through the analytical grid sweep.
- [x] Add seed-level uncertainty infrastructure to the fixed-quorum comparison.
- [x] Add analytical-vs-kernel phase-boundary cross-validation over 1,911 deterministic parameter cases; exact-boundary cases are reported separately because strict inequalities are numerically sensitive.
- [x] Generate final publication-quality comparative, ablation, safety-boundary, and localization figures from frozen CSV artifacts.
- [ ] Resolve every manuscript-vs-repository numerical discrepancy.
- [x] Build one-command reproducibility pipeline for all current experiments and figures.
- [ ] Clean legacy/placeholder research artifacts from the final release path.
- [ ] Rewrite Methods/Theory/Results around the verified model.
- [ ] Rewrite Introduction/Related Work/Abstract/Conclusion.
- [ ] Perform equation, dimensional, statistical, citation, and reproducibility audits.
- [ ] Perform simulated Transactions Reviewer #1/#2/editor audit.
- [ ] Mark `tag4` submission-ready only after all manuscript gates pass.

## Current verification checkpoint

- Latest full PR validation run: **PASS** on merge ref `378c6d018e1eb49dbe4774d1cc322a8fad006e1c`.
- Latest validation reported **102 passed, 0 failed**.
- Canonical benchmark: 6 scenarios × 10 seeds × 30 rounds = **1,800 deterministic rows**, byte-for-byte identical across repeated generation.
- Analytical boundary sweep: **1,911 cases**, maximum equilibrium error `1.1768e-14`, maximum quorum error `2.3315e-15`, zero classification mismatches away from strict numerical boundary cases, with 33 explicit boundary-near cases.
- Comparative stress grid: **4,200 rows**, covering all 14 single/pair/triple attack sets × 6 evidence levels × 5 drift levels × 10 seeds. Mean AEGIS-minus-fixed attack finalization difference = **0.05345** (95% CI approximately 0.05018–0.05672); the two-validator attack stratum gives **0.12472** (95% CI approximately 0.11845–0.13099). Single- and triple-validator strata are zero in this configuration, so the claim must be limited to the operational two-validator boundary regime rather than generalized to every attack size.
- Ablation: 50 rows. Availability varies materially by component; the full model gives 0.857 attack-period finalization, while removing predictive attenuation falls to 0.571. The analytical certificate-boundary metric is also tracked, preventing an ablation from being judged by availability alone.
- Localization: 800 rows across four validator locations, five evidence magnitudes, four drift levels, and ten seeds. Risk activation is ~0.986 across locations, while influence reduction differs by location (approximately A 0.573, B 0.556, C 0.538, D 0.521 mean drop), giving a location-sensitive output rather than only a binary detector rate.
- Publication artifacts are generated successfully as PDF/PNG from the experiment CSVs: comparative phase figure, component availability ablation, component safety-boundary ablation, and attack-localization influence figure.
- The validation pipeline is now green, but the PR remains a **draft validation vehicle** and is not merged or submission-ready.

## Scientific interpretation guardrails

1. The strong comparative result is specifically an availability result under the tested two-validator commit-withholding regime. It is not a blanket resilience claim.
2. The fixed-quorum comparator is a mathematical reference policy, not PBFT/HotStuff.
3. The safety result must be stated through the explicit certificate-boundary condition `q > (1+b)/2` under the stated honest non-equivocation assumptions.
4. The six nominal scenarios alone do not establish superiority; the stress grid and ablations are required evidence.
5. The localization experiment demonstrates state/influence response across locations; it does not by itself prove attack attribution accuracy.
6. Every headline paper number must be regenerated from the frozen repository artifacts before submission.

## Remaining hard blockers

1. **Manuscript reconciliation:** the repository currently does not contain the final manuscript source needed to reconcile every paper number, equation reference, figure, and claim.
2. **Final contribution freeze:** exact claims must be fixed only after manuscript reconciliation.
3. **Additional governance baseline:** add at least one stronger non-fixed-quorum reference before making broad comparative claims.
4. **Final statistical audit:** choose the final reported estimands, confidence intervals, and multiple-comparison treatment before writing Results.
5. **Transactions reviewer audit:** perform the final theorem-assumption, threat-model, novelty, citation, and claim-strength audit on the actual manuscript.
6. **Release cleanup:** remove or quarantine legacy/placeholder artifacts and freeze the exact submission commit.

## Non-negotiable gates

1. Every headline number in the paper must be generated from repository artifacts.
2. Every theorem must follow from explicitly stated assumptions.
3. Every major equation must have an identifiable implementation/test counterpart.
4. No unsupported Byzantine/PBFT safety claims.
5. No "topology attack" terminology unless topology is actually modified.
6. No "resilience" claim unless the metric and definition are explicit.
7. The final manuscript and repository must correspond to a frozen commit.
