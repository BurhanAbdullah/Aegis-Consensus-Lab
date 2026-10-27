# Manuscript–Repository Audit — 27 October 2026

**Repository:** `BurhanAbdullah/Aegis-Consensus-Lab`  
**Audited manuscript:** `research/transactions_rebuild/manuscript/AEGIS_Tag4_Transactions_Draft.tex`  
**Comparison baseline:** `tag4`, source commit `f5a13a0570a1bdb3bfaa9a1102b0951b7fe76d4e`  
**Audit type:** Static claim and artifact audit against source files and recorded GitHub Actions evidence.  
**Overall disposition:** **PARTIALLY ALIGNED; NOT YET CERTIFIED FOR SUBMISSION.**

This audit distinguishes: (1) source/model consistency, (2) recorded software and numerical validation, (3) empirical interpretation, and (4) a complete reproducible manuscript build. Passing CI does not automatically certify the latter two.

## Executive finding

The manuscript is notably cautious about key theoretical assumptions: it separates the heterogeneous canonical model from a homogeneous scalar reference reduction; limits its exact Jacobian theorem to interior dynamics with fixed exogenous detector evidence/drift; conditions weighted-quorum safety on authenticated vote context and honest non-equivocation; and excludes the historical 9,450-case physical-system claim because its raw case-level evidence is absent.

However, the complete paper is **not fully reproducible from the pinned `tag4` snapshot using the manuscript source alone**. The manuscript inputs `PROOFS.tex` and `../../experiments/publication_tables.tex` are not present at the paths referenced by the manuscript in the audited `tag4` snapshot. The generator source exists and references the frozen 200-round CSVs, but the generated publication outputs are not committed at the referenced `experiments/` paths in this snapshot. Strict CI reports successful generation/checking, yet its Actions run reports zero downloadable artifacts. Thus a recorded successful workflow supports that the steps passed but does not give a reader a downloadable copy of the exact generated outputs/log bundle from that run.

The source file uses IEEEtran and includes a title, abstract, model, derivations, experiment section and conclusion. No evidence in the inspected manifest or workflow outputs certifies that the exact manuscript PDF was compiled and visually inspected. Submission readiness therefore remains **NOT CERTIFIED**.

## Claim-by-claim audit

| Paper topic / claim | Evidence examined | Verdict | Required action |
|---|---|---|---|
| Trust-weighted consensus and adaptive quorum | Manuscript equations; `FINAL_MODEL_SPEC_v2.md`; certificate/quorum sections | **Aligned, conditional** | Keep explicit state and assumptions; do not imply production deployment. |
| Detector evidence and temporal drift are observable, not attack ground truth | Manuscript detector interface; canonical model spec | **Aligned by definition** | State detector normalization/thresholds and input provenance for every experiment. |
| Exact full interior Jacobian | Manuscript theorem and canonical specification define `J_i = diag((1-rho_i-ell_i E_i) I_m, a_i)` for fixed exogenous `E_i,D_i` and an interior point | **Consistent under stated assumptions** | Keep the exogenous-input and differentiable-interior conditions adjacent to theorem/result. If evidence/drift is endogenous, use the augmented state/Jacobian. |
| Heterogeneous equilibrium versus homogeneous closed-form quorum boundary | Manuscript explicitly labels the scalar expression as a homogeneous reference reduction | **Properly qualified** | Keep the label “reference reduction”; do not plot it as the exact boundary of heterogeneous governance. |
| Weighted-certificate safety | Manuscript and spec condition safety on quorum intersection, authenticated context, honest non-equivocation, and a Byzantine weight bound | **Conditionally stated** | Show the exact assumptions and define normalized versus active/participating governance weight in theorem statements. Avoid unconditional Byzantine-safety wording. |
| Availability / liveness | Manuscript requires `q <= h_k`; conservative interval uses `h_k >= 1-b` | **Sufficient-condition statement, not general liveness proof** | Do not claim general asynchronous liveness, eventual synchrony guarantees, or production availability without a separate protocol-level argument. |
| Full Transactions test suite passes | CI run #30 / #121 on PR head `261f05cfbbe1a3198c64b9816271d7c77e959fc0`; historical #24 and the recorded 77-test run on their own commits | **Recorded CI evidence passes; commit scopes differ** | Cite each run with its precise SHA. Do not imply an old run tested the current release commit. |
| 1,000 mathematical cross-validation cases | Provenance manifest; strict workflow succeeded | **Recorded numerical validation** | Include exact seed, environment and full stdout/CSV in a retrievable audit artifact. It supports implementation consistency, not theorem proof by itself. |
| Maximum equilibrium residual `1.1102230246251565e-16` | Provenance manifest | **Recorded metric** | Keep enough significant figures but describe as observed maximum for the recorded validation run. |
| Maximum finite-difference Jacobian relative error `9.648334450896133e-11` | Provenance manifest / independent validation script | **Recorded metric** | State the finite-difference step and error normalization; treat as numerical agreement only. |
| Zero stability-classification mismatches | Provenance manifest / cross-validation source | **Recorded metric** | Scope to the generated 1,000-case cross-validation suite and tested implementation. |
| Deterministic repeat is byte-identical | Provenance manifest and strict workflow step | **Recorded workflow check** | Archive run output and exact generated file hashes so readers can independently verify the bytes. |
| Publication tables are generated from frozen data | Generator source and strict workflow steps | **Generation logic exists; snapshot artifact path gap** | Commit the generated CSV and LaTeX table or attach them to the release. Verify output paths and manuscript `\input` paths agree. |
| Predictive method outperforms baseline | Frozen 200-round paired traces and prior phase-space interpretation; recorded earlier comparison described as inconclusive (p approximately 0.42) | **NOT established** | Avoid superiority claim. Re-run the exact paired analysis from raw rows, state statistical test/effect size/uncertainty, and report negative/inconclusive results. Do not quote p≈0.42 as independently reproduced in this audit unless its source output is packaged. |
| Historical 9,450-case physical-grid validation | Provenance manifest explicitly excludes it due to missing raw case-level/controller evidence | **UNVERIFIED; excluded** | Do not present as validated. To reinstate, add all raw cases, scenario/controller configs, seeds, metric scripts, per-case outputs and an independently rerunnable validation workflow. |
| Physical grid or real-world deployment demonstrated | Manuscript itself says deterministic scenario model, not a demonstrated physical-grid deployment | **Not demonstrated** | Use “model/simulation” terminology; no deployment, physical mitigation, or real-time readiness claim. |
| Manuscript compilation/submission readiness | Manifest states compilation is not certified; no authoritative compiled PDF/build evidence inspected | **NOT CERTIFIED** | Ensure all `\input` dependencies exist, run the exact LaTeX build in CI, archive PDF/log/auxiliary file and inspect references, tables, figures, overflow and warnings. |
| Tables/figures all regenerated and inspected | Generator can derive publication table; frozen figure files and blob SHAs are indexed by manifest; current strict run has zero downloadable artifacts | **Partially supported** | Attach or commit exact generated outputs; record hashes and environment; visually inspect the PDF and figures. A passing data-provenance step alone does not establish visual quality. |

## Concrete reproducibility blockers

### 1. Manuscript input paths do not resolve in the audited `tag4` snapshot

The manuscript has:
- `\input{PROOFS.tex}`
- `\input{../../experiments/publication_tables.tex}`

The audited repository lookup could not find `research/transactions_rebuild/PROOFS.tex`, `experiments/publication_tables.tex`, or `experiments/publication_comparison.csv` at those `tag4` paths. There may be a differently located proof file; the manuscript's relative inputs still need to resolve from the directory in which LaTeX is invoked. As written, a clean build from this snapshot cannot be presumed.

**Fix:** make the proof source location explicit and consistent, commit the exact generated publication table/CSV or generate them as an explicit pre-build step, and run LaTeX from a documented working directory. Add a CI job that fails if any manuscript input or figure is missing.

### 2. Generated outputs are not downloadable from the checked CI run

The strict Transactions workflow run on the documentation PR head succeeded, including test, cross-validation, repeatability, publication generation, comparison validation and frozen provenance steps. GitHub Actions returned **zero uploaded artifacts** for that run.

**Fix:** upload a release bundle containing:
- strict validation stdout/stderr and summaries;
- `experiments/strict_cross_validation.csv` and its SHA-256;
- generated `publication_comparison.csv` and `publication_tables.tex`;
- exact environment / dependency versions and commit SHA;
- LaTeX build log and compiled PDF, only after successful build;
- a manifest mapping figures and tables to their source data/scripts and hashes.

### 3. Historical and current validation lineages must remain distinct

Evidence reviewed uses more than one commit:
- `f5a13a0570a1bdb3bfaa9a1102b0951b7fe76d4e`: recorded 77-test run (reported as 77 passed in 0.47 s).
- `7e947a7606ba9e091358a9c5f6b6a29850dd643b`: successful historical strict workflow run #24.
- `261f05cfbbe1a3198c64b9816271d7c77e959fc0`: documentation PR head, strict run #30 and tag4 validation run #121 succeeded.

These are useful separate evidence points, not one combined run on one SHA. The final release should identify its exact tagged commit and show CI for that commit or its merge commit.

## Model/theory review observations

1. **Trust state:** component-wise equilibrium and diagonal Jacobian are consistent with the trust update for fixed evidence and an interior point. At projection boundaries the derivative can change; results must not be extended there without a nonsmooth/projected-map argument.
2. **Risk state:** the formula `R_i^* = ((1-a_i)E_i+c_iD_i)/(1-a_i)` only applies when the risk-containment/invariant-region condition holds. Keep it conditional.
3. **Detector-to-state feedback:** the theorem holds with detector evidence/drift exogenous. If detector values depend on trust, risk, or the physical system state, the presented Jacobian is not the Jacobian of that augmented closed loop.
4. **Weighted quorum:** intersection arguments need a consistent normalization of total governance weight and assumptions that honest validators do not sign conflicting values in the same certificate context. Availability uses honest *participating* weight, not merely honest weight present in the system.
5. **Stochastic claims:** deterministic recurrence and sampled numerical validation do not by themselves prove stochastic convergence or robustness under all adversarial schedules.
6. **Comparative claims:** paired reference/predictive traces can provide descriptive results, but do not establish a general predictive advantage without a suitable pre-specified statistical analysis and evidence on matched cases/seeds.
7. **Physical validation:** the repository manifest explicitly excludes the 9,450-case claim. Keep it out of abstract, headline contribution, conclusion and any figure caption unless the raw evidence is restored and independently reproduced.

## Evidence links (recorded)

- Strict Transactions gate on docs PR head: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40480570506
- tag4 validation on docs PR head: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40480570404
- Historical strict Transactions run #24: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/31870468981
- Recorded 77-test run: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/38173887211
- Canonical model specification: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md
- Provenance manifest: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/TRANSACTIONS_RELEASE_PROVENANCE_MANIFEST_v1.md
- Manuscript draft: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/manuscript/AEGIS_Tag4_Transactions_Draft.tex
- Cross-validation source: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/benchmarks/strict_cross_validation.py
- Publication generator: https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/benchmarks/generate_publication_tables.py

## Release checklist

- [x] Identify audited source manuscript and canonical model source.
- [x] Review stated assumptions and theorem claim boundaries.
- [x] Record the 77-test and strict numerical validation figures with scope limitations.
- [x] Identify unsupported 9,450-case physical validation claim as excluded.
- [x] Identify predictive superiority as not established.
- [x] Check workflow statuses for the documentation PR.
- [ ] Repair and validate LaTeX input paths in the exact tagged snapshot.
- [ ] Regenerate and attach/commit publication CSV and LaTeX table.
- [ ] Upload strict validation logs, environment and artifact hashes.
- [ ] Compile the exact paper and visually inspect the PDF, tables, figures and references.
- [ ] Reproduce comparative statistics from the paired traces and package the full output.
- [ ] Run final checks on the exact release commit and then publish.

## Final verdict

**The paper is structurally and conceptually aligned with the canonical model where it states its assumptions, but the full manuscript-and-results package is not yet submission-ready.** The strongest supported claim today is a condition-qualified deterministic model with recorded passing implementation and numerical validation checks. Predictive superiority is not established; the 9,450-case physical-grid claim is unverified/excluded; and the exact paper build and generated table artifacts need to be made reproducible before claiming full validation.
