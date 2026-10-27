# Paper-to-Repository Point-by-Point Verification Checklist — 27 October 2026

**Repository snapshot under test:** `tag4` at `f5a13a0570a1bdb3bfaa9a1102b0951b7fe76d4e`  
**Paper under test:** `research/transactions_rebuild/manuscript/AEGIS_Tag4_Transactions_Draft.tex`  
**Purpose:** determine whether every mathematical statement, empirical result, table, figure and reproducibility statement in the manuscript is directly supported by the exact repository snapshot.

## Result at a glance

**Verdict: NO — the repository is not yet a 100% complete, directly reproducible implementation/evidence package for everything implied by the paper.**

This does **not** mean all paper mathematics is wrong. The core deterministic equations and several proof/test pairs align well. The release fails full paper-to-repo completeness because the LaTeX build paths are inconsistent, the manuscript does not actually include the repository's figures, generated comparison-table outputs are not tracked in the `tag4` tree, the claimed coupled feedback reduction has no fully specified executable AEGIS map, and the empirical data do not validate the full analytical operating set.

Status definitions:
- **PASS** = exact source and relevant executable test/evidence found.
- **PARTIAL** = some direct support exists, but coverage or reproducibility is incomplete.
- **FAIL** = the paper's claimed reproducible path cannot work as written or the assertion overreaches the evidence.
- **MISSING** = no corresponding implementation/artifact/evidence found in the inspected snapshot.

## A. Manuscript structure and build

| # | Paper item | Repository check | Result | Why / fix |
|---:|---|---|---|---|
| A1 | Exact manuscript source exists | `research/transactions_rebuild/manuscript/AEGIS_Tag4_Transactions_Draft.tex` exists at blob `3a8338abbd03ed7ac7e8caf4f627b9931d72c84f` | PASS | This is the exact source reviewed. |
| A2 | Proof appendix/input exists | `research/transactions_rebuild/manuscript/PROOFS.tex` exists at blob `57c0b55f2231571f940919ef21fc99c9d298b333` | PASS | Correction to the earlier audit: the proof file does exist alongside the manuscript. |
| A3 | Proof input resolves from a documented clean build | Manuscript says `\\input{PROOFS.tex}`; no build script documents a working directory that also resolves the next table input | FAIL | If run from the manuscript directory, the proof resolves, but the table path below resolves to the wrong directory. If run from repository root, `PROOFS.tex` does not resolve. Use root-relative paths or a Makefile with a single documented working directory. |
| A4 | Comparison table input exists at manuscript-referenced path | Manuscript says `\\input{../../experiments/publication_tables.tex}`. From manuscript directory this resolves to `research/experiments/publication_tables.tex`; from repository root it resolves outside the repository. The generator writes `experiments/publication_tables.tex` at repo root, but that generated file is not tracked in `tag4`. | FAIL | Change to a build path that resolves from the chosen working directory, run the generator before LaTeX, and verify the generated file is present. |
| A5 | Paper build CI | Strict workflow runs Python tests, numerical validation and table generation; it does not run LaTeX or archive a compiled paper PDF | MISSING | Add a clean-checkout LaTeX build, fail on missing inputs, save the PDF and logs as workflow artifacts, and inspect them. |
| A6 | Bibliography/citations | The draft has no bibliography commands, bibliography file, or `\\cite` references | PARTIAL | For a Transactions-style research paper, add appropriate prior-work and protocol references. A mathematically self-contained draft is not yet a complete literature-grounded submission. |
| A7 | Actual figures in the paper | Manuscript contains no `\\includegraphics` commands; its only generated artifact input is a table | FAIL | The repository has figures, but the current manuscript does not include them. If figures are required to support claims, add the correct figures/captions/labels and verify the compiled PDF. |
| A8 | Figure/table captions and cross-references | No in-manuscript figure captions/labels/references were found in the source; the generated table has a label but is not currently resolvable from the paper | FAIL | Include and reference the actual artifacts, use unique labels, and check the final PDF. |

## B. Mathematical claims, equation by equation

| # | Manuscript claim | Code/proof/test evidence | Result | Gap / required test |
|---:|---|---|---|---|
| B1 | Trust vector and weighted aggregate `tau = w^T T` | `FINAL_MODEL_SPEC_v2.md`, `kernel/tag4_kernel.py`, `test_math_code_alignment.py` | PASS | Weight dimension and normalization are checked by the kernel. |
| B2 | Projected trust update | Canonical spec, kernel update, `test_reference_kernel_equivalence.py`, `test_reference_model.py` | PASS | Projection makes state bounded; this alone is not a convergence proof. |
| B3 | Trust equilibrium `rho/(rho+ell E)` | `unified_state_model.py`, `PROOFS.tex`, `tests/test_strict_mathematical_validation.py` | PASS, conditional | Valid for fixed exogenous evidence and positive denominator; boundary/degenerate cases must remain qualified. |
| B4 | Trust stability multiplier `1-rho-ell E` | Exact Jacobian code and finite-difference tests | PASS, conditional | Only the unclipped differentiable interior; not a global projected-map stability theorem. |
| B5 | Risk recurrence and equilibrium | `unified_state_model.py`, risk-containment tests, proof proposition 3 | PASS, conditional | The fixed point lies in `[0,1]` only if the stated containment condition holds. |
| B6 | Detector score normalization | `detector_evidence.py`, `test_detector_evidence.py` | PASS for normalization logic | Experiments must also document actual detector source signals, thresholds, weights and their provenance. The archived 200-round consensus CSVs do not themselves contain all raw detector channels. |
| B7 | Temporal drift is normalized from four consecutive observable channels | `test_full_jacobian_and_drift.py` tests first-round zero, identical observations and maximum distance | PASS for helper behavior | Frozen consensus traces do not record the full four-channel detector vector history, so the table data alone cannot reproduce a detector-to-consensus causal chain. |
| B8 | Risk is a predictive risk state and uses no attack ground truth in the update | Kernel accepts evidence/drift inputs; detector code maps observable scores | PARTIAL | Need a complete experiment trace proving inputs were generated without ground-truth leakage and showing channel scores → evidence/drift → risk/trust/quorum → certificate outcome. |
| B9 | Governance influence `G = tau clip(1-kappa R)` | `kernel/tag4_kernel.py`, `test_math_code_alignment.py`, reference/kernel equivalence test | PASS | Direct equation-to-code comparison exists. |
| B10 | Active governance weight and adaptive quorum | Kernel and reference model equivalence tests | PASS for deterministic implementation | The manuscript's active set and threshold need to be tied to the same exact state snapshot in certificate validation. |
| B11 | Certificate-driven finalization | `kernel/certificates.py`, `test_certificate_finalization.py`, `test_certificates.py`, adversarial tests | PASS for tested certificate semantics | Check all certificate contexts and weight-snapshot rules. The quorum proof itself notes that governance weights must be fixed/bound to the certificate context. |
| B12 | Weighted quorum intersection lower bound `2q-1` | `QUORUM_SAFETY_PROOF_v1.md`, `test_quorum_proof.py`, `tests/test_weighted_quorum_validation.py` | PASS, conditional | Proof assumes total normalized weight 1 and honest non-equivocation; do not imply unconditional protocol safety. |
| B13 | Safety condition `q>(1+b)/2` | Proof and threshold tests | PASS, conditional | Applies to conflicting certificates with common context and authenticated distinct voters. |
| B14 | Availability condition `q<=h` and conservative `q<=1-b` | Proof and weighted-quorum tests | PASS as a sufficient condition | Does not prove asynchronous PBFT liveness, view-change progress, or communication availability. |
| B15 | Nonempty conservative interval iff `b<1/3` | Proof and randomized/parametric test | PASS | Correct for the stated sufficient safety/availability interval. |
| B16 | Exact full interior Jacobian `diag(beta I_m, a)` | `unified_state_model.py`, `test_full_jacobian_and_drift.py`, strict finite-difference tests | PASS, conditional | This is the state-transition Jacobian for fixed exogenous E,D, not the Jacobian of an endogenous detector/physical feedback loop. |
| B17 | Coupled two-state Jury stability | Generic Jury helper and tests against random 2×2 matrices; symbolic `COUPLED_STABILITY_PROOF_v1.md` | PARTIAL | Tests verify the Jury criterion itself, not an actual fully specified AEGIS feedback function `E(tau,R)`, `D(tau,R)` with its equilibrium and analytic Jacobian. Specify and test the actual coupled map before claiming that the model's coupled dynamics were numerically validated. |
| B18 | Full operating set `F={theta: rho(J)<1, (1+b)/2<q<=h}` | The set is defined in the manuscript; proof obligations explicitly require independently generated simulation points and quantitative agreement | PARTIAL / MISSING empirical validation | No inspected experiment maps independent simulation cases to the complete theta vector, spectral radius, Byzantine weight, honest participating weight, quorum and observed safe/available outcome. A phase-space heatmap alone is not validation of this set. |
| B19 | Projection boundaries are handled by theorem | Manuscript explicitly excludes them from the interior theorem | PASS as qualified | Do not extend interior Jacobian conclusions to clipping boundaries without a separate piecewise/nonsmooth argument. |
| B20 | Stochastic convergence | Manuscript says it is not inferred | PASS as qualified | The stochastic test file is not by itself proof of stochastic convergence; do not claim such a theorem. |

## C. Tables and numerical results

### C1. Table actually specified by the manuscript

The manuscript includes `publication_tables.tex` through an input command. The generator is `research/transactions_rebuild/benchmarks/generate_publication_tables.py`. It uses the frozen paired files:

- `archive/final_run/experiments/results.csv` (Git blob `21399bd0ccf0d883e22743a390afc10ecc47083f`)
- `archive/final_run/experiments/results_predictive.csv` (Git blob `e930530eb4fd11c5a64b002d67922f27a2eb99c3`)

The generator checks required columns, numeric values, exactly 200 rows, round IDs 1–200 and matching round IDs between files. This is useful fail-closed validation. However, the generated output `experiments/publication_comparison.csv` and `experiments/publication_tables.tex` are created during CI and are not tracked in the inspected `tag4` tree, and no LaTeX build consumes them successfully.

### C2. Recomputed descriptive values from the two frozen CSV files

These are recomputed from the checked-in 200-round rows using the same fields as the generator, not copied from a prebuilt LaTeX table.

| Metric | Reference | Predictive | Predictive − reference | Interpretation |
|---|---:|---:|---:|---|
| Successful rounds / 200 | 110 / 200 | 125 / 200 | +15 rounds | Descriptive outcome count |
| Finalization rate | 55.00% | 62.50% | +7.50 percentage points | Not, by itself, proof of a general predictive advantage |
| Mean quorum field | 136.945 | 137.970 | +1.025 | Field units/meaning should be explicitly defined |
| Mean safety field | 51.890 | 50.790 | −1.100 | Metric definition/range/interpretation needs to be documented |
| Mean commit weight | 163.090 | 160.155 | −2.935 | Descriptive only |
| Mean total governance weight | 234.115 | 233.970 | −0.145 | Descriptive only |

**Important:** these are two frozen traces, not necessarily independent replicates. The current table generator computes descriptive averages only; it does not perform a hypothesis test, estimate uncertainty, correct for multiple comparisons, or establish causality. A previous exploratory comparison was described as inconclusive (approximately p=0.42), so the paper must not state that the predictive regime is generally superior without a properly specified paired analysis and uncertainty reporting.

**Required table fix:** define each field (`safety`, `quorum`, `total_weight`, `commit_weight`), state the denominator and unit, add the table to the actual PDF, and package both generated output files and their hashes. Ensure the values in the PDF exactly match a fresh generator run.

### C3. Phase-space grids

Three CSVs exist:
- `experiments/phase_space.csv`
- `experiments/phase_space_baseline.csv`
- `experiments/phase_space_predictive.csv`

The baseline and predictive grids each contain 36 combinations (6 slashing values × 6 recovery values) with success counts from 200 rounds per combination. The plotting scripts exist. This supports the existence of a historical parameter sweep, but the manuscript does not include these heatmaps and the current manuscript does not report a full reproducible statistical analysis of them. These grids do not, by themselves, validate the analytical security–availability set `F`.

## D. Figures: every figure found in the repository vs the paper

**Critical distinction:** the repository contains figures, but the manuscript source contains no `\\includegraphics` command. Therefore none of the repository figures is currently demonstrated to be a figure in the submitted paper.

| Figure artifact | Source data/script evidence | In manuscript? | Status |
|---|---|---|---|
| `baseline_heatmap_publication.pdf/.png` | Frozen phase-space grid; `make_baseline_heatmap.py` | No | PARTIAL: archived figure/source exist; not included or rebuilt by manuscript workflow |
| `predictive_heatmap_publication.pdf/.png` | Frozen predictive grid; `make_predictive_heatmap.py` | No | PARTIAL |
| `difference_heatmap_publication.pdf/.png` | Baseline/predictive grid; `make_difference_heatmap.py` | No | PARTIAL |
| `comparative_governance_landscapes_publication.pdf/.png` | Baseline/predictive grids; comparison-panel script | No | PARTIAL |
| `phase_space_publication.png` | Phase-space CSVs and plotting scripts | No | PARTIAL |
| `regime_classification_map.pdf/.png` | Regime-map script and phase-space data | No | PARTIAL |

The release provenance checker verifies fixed Git blob hashes for selected archived figure/data files. That confirms the checked-in bytes match the manifest; it does **not** prove that each figure was regenerated in the current run or is correctly placed/labeled in the manuscript. The strict workflow's provenance step is not a substitute for a visual PDF review.

**Required figure fix:** for every figure actually used, record (i) manuscript figure number and caption, (ii) exact source CSV, (iii) generating script and command, (iv) environment, (v) output hash, (vi) whether freshly regenerated output matches the frozen version, and (vii) a successful visual review of the final PDF.

## E. Test suite coverage vs paper claims

| # | Test coverage | What it supports | What it does not establish |
|---:|---|---|---|
| E1 | Full `python -m pytest -q research/transactions_rebuild` run recorded green | Test suite passes for the exact workflow commit | Does not compile the paper or prove untested claims |
| E2 | Trust/risk equilibrium tests | Closed-form fixed-point identities over sampled parameters | Not a theorem beyond the stated assumptions; tests alone are not proof |
| E3 | Finite-difference Jacobian tests | Numerical agreement of coded Jacobian with coded state map in sampled interior points | Not the endogenous detector/physical-loop Jacobian |
| E4 | Spectral radius and Jury tests | Algebraic implementation cross-checks | Not validation of an actual coupled AEGIS feedback equilibrium |
| E5 | Reference-vs-kernel equivalence tests | Independent reference and implementation agree on specified scenarios | Shared conceptual mistakes can remain; these tests do not establish real-world effectiveness |
| E6 | Detector evidence normalization tests | Bounded score, normalized weights, deterministic mapping | Not detector accuracy, precision/recall, false alarm rate, latency, or robustness on labeled attacks |
| E7 | Certificate and adversarial tests | Selected certificate-context, distinct-voter and finalization behavior | Not a complete formal verification of all PBFT safety/liveness and all schedules |
| E8 | 1,000-case strict cross-validation | Independent sampled equations/implementation checks, reported zero classification mismatches | Does not validate physical data, all parameter space, the paper build, or causal predictive superiority |
| E9 | Deterministic repeated CSV comparison | Repeated strict validation output byte-identical in CI | Does not guarantee every figure/table/PDF is included or reproducible |
| E10 | Frozen-data provenance checker | Expected source artifact Git blob hashes match | Does not regenerate/visually inspect all outputs; it checks listed frozen inputs |
| E11 | Publication-table generator | Recomputes five descriptive fields from two 200-row traces | Does not conduct significance testing or prove the proposed method is better |
| E12 | LaTeX build and visual review | No workflow step found | MISSING — must add |

## F. Experiments/claims that are absent or not supported

| Claim/experiment | Status | What would be needed |
|---|---|---|
| Full 9,450-case physical-grid validation | **UNVERIFIED / EXCLUDED** | Raw case-level results, configs, seeds, controller traces, metric scripts and rerun workflow |
| General predictive method superiority | **NOT ESTABLISHED** | Matched repeated runs, pre-specified primary metric, paired test, effect size, confidence interval and complete raw outcomes |
| Detector performance against ground-truth attack labels | **MISSING from the current manuscript evidence package** | Labeled test set, definitions, confusion matrix, precision/recall/FPR, latency and split protocol |
| Validation of the complete analytical operating set `F` | **MISSING** | Independently generated parameter points and a table of predicted stable/safe/available versus observed outcomes |
| Full endogenous detector-to-risk-to-quorum feedback stability | **PARTIAL** | Specify executable feedback functions, derive/test their actual Jacobian and equilibrium, then run independent validation |
| Physical testbed or deployed cyber-physical validation | **NOT DEMONSTRATED** | Hardware/testbed logs and reproducible experiment protocol; otherwise use simulation wording |
| PBFT/HotStuff-equivalent baseline comparison | **NOT ESTABLISHED** | Protocol-equivalent implementations and matched assumptions; do not infer from the two internal regimes |
| Complete manuscript build from a clean checkout | **FAIL / NOT CERTIFIED** | Fix inputs, add LaTeX CI, archive PDF/logs and inspect all pages |

## G. Reproducibility / release blockers in priority order

1. **P0 — Fix LaTeX inputs.** The proof file exists at the manuscript directory, but no single documented working directory resolves both `\\input{PROOFS.tex}` and `\\input{../../experiments/publication_tables.tex}`. Change paths and add a reproducible build command.
2. **P0 — Add paper-build CI.** Compile exact manuscript from a clean checkout; fail on missing inputs; archive the PDF and logs.
3. **P0 — Include figures deliberately.** Decide which repository figures actually belong in the paper; add `\\includegraphics`, captions, labels and text references. Do not imply they are in the paper while they are only archived in the repository.
4. **P0 — Generate and package table artifacts.** Run `generate_publication_tables.py`, save the generated CSV and TeX output as release artifacts, and ensure the paper uses those exact bytes.
5. **P1 — Test the full coupled feedback claim.** Either narrow the manuscript to the exogenous-input Jacobian actually implemented, or specify and test the endogenous coupled map.
6. **P1 — Validate the analytical operating set.** Generate independent cases covering stability, Byzantine fraction, honest participation, quorum and outcomes; report quantitative agreement.
7. **P1 — Correct empirical framing.** Keep the 9,450-case physical claim excluded; do not claim predictive superiority based on descriptive 200-round traces.
8. **P1 — Define data fields.** Explain the units and semantics of `safety`, `quorum`, `total_weight`, and `commit_weight`; describe what “success” means.
9. **P2 — Complete scholarly apparatus.** Add citations/references and verify all claims against the cited prior work.
10. **P2 — Freeze the final snapshot.** Re-run tests, cross-validation, artifact generation, provenance and PDF build on the exact final commit/tag; include SHA and downloadable outputs.

## Final conclusion

The canonical trust/risk equations, interior Jacobian, certificate-level quorum inequalities and several reference-vs-kernel tests are supported by source code and recorded CI. That is meaningful support for the theory-first core.

But **the answer to “is the repository 100% everything mentioned in the paper?” is no**. The paper's current build path is inconsistent; the paper contains no figures even though figures are archived in the repository; generated table outputs are not tracked; the coupled feedback claim lacks a fully specified executable feedback experiment; and the empirical traces do not establish predictive superiority or validate the complete analytical operating set. The 9,450-case physical claim remains excluded. The exact paper PDF has not been compiled and reviewed by CI.

The paper should not be described as fully validated until the P0 and P1 items above are closed and the final tagged commit passes the combined software + data + manuscript build.
