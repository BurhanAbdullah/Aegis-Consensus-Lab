# IEEE Transactions Reviewer Audit — tag4

This audit is intentionally limited to the canonical repository artifact. It is **not** a manuscript acceptance certificate because the current branch does not contain the final manuscript source.

## Reviewer #1 — Mathematical rigor

| Check | Status | Finding |
|---|---|---|
| State variables and recursions are explicit | PASS | Canonical model and kernel are frozen. |
| Trust state separated from governance attenuation | PASS | The canonical policy explicitly separates these quantities. |
| Equilibrium characterization | PASS | Executable closed-form reference and projection tests exist. |
| Local stability | PASS | Jacobian/spectral-radius condition plus independent Jury cross-checks. |
| Quorum boundary | PASS | Strict boundary is explicitly `q > (1+b)/2` under stated assumptions. |
| Theorem assumptions | PASS | Unsupported PBFT/HotStuff theorem claims are prohibited. |
| Numerical verification | PASS | 1,911 analytical/kernel cases; max errors approximately `1.18e-14` and `2.33e-15`. |

## Reviewer #2 — Experimental validity

| Check | Status | Finding |
|---|---|---|
| Deterministic canonical benchmark | PASS | 6 scenarios × 10 seeds × 30 rounds = 1,800 rows; repeated generation is byte-identical. |
| Strong comparison | PASS | 4,200-case stress grid across all single/pair/triple attack sets, evidence, drift, and seeds. |
| Multiple baselines | PASS | Static `q=0.67` and stricter static `q=0.75` policies receive identical traces. |
| Ablation | PASS | Five variants with availability and certificate-boundary metrics. |
| Localization | PASS | Four locations, five evidence magnitudes, four drift levels, ten seeds. |
| Uncertainty | PASS | Seed-level 95% intervals are generated in the summary pipeline. |
| Publication figures | PASS | Comparative figures for both static baselines plus ablation and localization figures. |
| Leakage / unfair comparison | PASS | Baselines use identical generated traces. |

## Editor / scope audit

| Check | Status | Finding |
|---|---|---|
| Novelty claim is appropriately scoped | PASS | The repository guardrails prohibit claiming novelty from generic adaptive trust/quorum ingredients alone. |
| Attack terminology | PASS | No topology-attack claim is permitted without actual topology modification. |
| Resilience terminology | PASS | Claims must identify the metric; availability is not silently renamed resilience. |
| Unsupported physical-system claims | PASS | The old 9,450-case claim is explicitly excluded by policy. |
| Reproducibility | PASS | CI regenerates tests, benchmarks, figures, and artifact checks. |
| Legacy separation | PASS | Archived v4 material is explicitly non-authoritative. |

## Remaining manuscript-level gates

These cannot be truthfully marked PASS until the actual final manuscript source is supplied/placed in the release tree:

1. every numerical statement reconciled against the frozen CSVs;
2. every figure/table reference reconciled against generated artifacts;
3. every equation/theorem reference reconciled against the canonical model;
4. abstract, introduction, conclusion, and contribution claims rewritten to match the evidence;
5. citations and related-work novelty positioning checked;
6. statistical estimands, confidence intervals, and multiplicity treatment frozen;
7. final page/formatting/reference audit;
8. final reviewer #1/#2/editor pass on the actual manuscript;
9. exact manuscript commit frozen together with the experiment commit.

## Release rule

**Do not label the work submission-ready until every manuscript-level gate above passes.**
