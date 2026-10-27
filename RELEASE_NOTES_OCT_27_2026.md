# AEGIS Consensus Lab — 27 October 2026 Release Candidate (Architecture, Tests, Results & Manuscript Audit)

**Status:** evidence-qualified release candidate. The source-level test and numerical validation records below are not a certification of manuscript compilation, predictive superiority, or physical-grid deployment.

## Reader entry points
- [Architecture, Tests & Results reader guide](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/docs/reader-guide-architecture-tests-results/READER_GUIDE_ARCHITECTURE_TESTS_RESULTS.md)
- [Manuscript–Repository Audit, 27 October 2026](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/docs/oct-27-2026-paper-audit/MANUSCRIPT_REPOSITORY_AUDIT_2026-10-27.md)
- [Canonical model specification](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md)
- [Transactions rebuild README](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/README.md)
- [Proof obligations](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/PROOF_OBLIGATIONS.md)
- [Adversarial validation scope](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/ADVERSARIAL_VALIDATION_v1.md)
- [Release provenance manifest](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/TRANSACTIONS_RELEASE_PROVENANCE_MANIFEST_v1.md)
- [Manuscript draft](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/manuscript/AEGIS_Tag4_Transactions_Draft.tex)
- [Independent cross-validation code](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/benchmarks/strict_cross_validation.py)
- [Publication table generator](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/research/transactions_rebuild/benchmarks/generate_publication_tables.py)

## Architecture summary
The model connects multidimensional trust, normalized observable detector evidence, temporal detector drift, predictive risk, governance influence, an adaptive quorum, and authenticated prepare/commit certificates. Certificates are tied to a common height, view, phase, and proposal hash; each validator is counted at most once per context. The deterministic implementation consumes scenario inputs. It is not itself evidence of physical-grid deployment.

## Recorded test and numerical results
The provenance manifest records the following results for its specified validation lineage:
- 77 Transactions tests passed.
- 1,000 independent mathematical cross-validation cases.
- Maximum equilibrium residual: `1.1102230246251565e-16`.
- Maximum finite-difference Jacobian relative error: `9.648334450896133e-11`.
- Zero stability-classification mismatches.
- Repeated cross-validation output was byte-identical.
- Publication comparison generation and data/figure provenance checks passed in the historical successful strict workflow.

These figures must be attached to their exact run/commit, not treated as results for every branch or commit.

## Relevant CI runs
- [Strict Transactions gate — docs guide PR, run #30](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40480570506) — success on commit `261f05cfbbe1a3198c64b9816271d7c77e959fc0`.
- [tag4 validation — docs guide PR, run #121](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40480570404) — success on the same commit.
- [Historical strict Transactions run #24](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/31870468981) — success on commit `7e947a7606ba9e091358a9c5f6b6a29850dd643b`.
- [Recorded 77-test run](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/38173887211) — 77 passed in 0.47s on commit `f5a13a0570a1bdb3bfaa9a1102b0951b7fe76d4e`.
- [Audit PR strict workflow — run #31](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40481058939) — status was in progress when this package was prepared.
- [Audit PR tag4 validation — run #122](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/actions/runs/40481058849) — status was in progress when this package was prepared.

The strict run on the docs-guide PR had **zero downloadable Actions artifacts**. This release candidate therefore links evidence but does not claim to bundle the CI logs/outputs.

## Reproduction command
Use Python 3.12 as configured by the tag4 validation workflow:

```bash
python -m pip install --upgrade pip pytest numpy
PYTHONPATH="$PWD/research:$PWD/research/transactions_rebuild:$PWD/research/transactions_rebuild/kernel" \
  python -m pytest -q research/transactions_rebuild
```

Follow [the strict workflow](https://github.com/BurhanAbdullah/Aegis-Consensus-Lab/blob/tag4/.github/workflows/tag4-transactions-strict.yml) for independent mathematical cross-validation, deterministic repetition, publication-table generation and frozen-provenance checks. Preserve complete stdout/stderr, dependency versions, commit SHA and generated outputs in any independent rerun.

## Manuscript alignment and limitations
- The exact interior Jacobian theorem is conditional on fixed exogenous evidence/drift and a differentiable interior point. Endogenous detector states need an augmented Jacobian.
- The scalar quorum expression is a homogeneous reference reduction; it is not the exact boundary for all heterogeneous governance states.
- Weighted certificate safety depends on authenticated context, honest non-equivocation and the stated Byzantine governance-weight bound. Availability depends on honest *participating* weight.
- The archived phase-space comparison does not establish a statistically significant global predictive advantage. Do not state general predictive superiority.
- The 9,450-case physical-grid validation claim is **excluded and unverified** because raw case-level/controller evidence is missing. Do not present it as an independently reproduced result.
- The historical frozen baseline/predictive traces are 200 rounds each. Derived tables should only be generated from those frozen inputs and not hand-edited.
- The manuscript draft references `PROOFS.tex` and `../../experiments/publication_tables.tex`; these inputs could not be found at the manuscript-referenced paths in the audited `tag4` snapshot. The publication generator exists, but the generated table/CSV were not found at `experiments/publication_tables.tex` and `experiments/publication_comparison.csv` in that snapshot. Resolve paths and commit or generate these artifacts before claiming a clean paper build.
- The strict Actions run had no downloadable artifacts; raw logs, numerical CSV, generated tables and the final compiled PDF have not been bundled here.
- Manuscript compilation and final submission readiness are **not certified**.

## Release gate
Before describing the paper as fully validated:
1. Resolve all LaTeX inputs and figure references from a clean checkout.
2. Regenerate and save the publication CSV/LaTeX table from the frozen input CSVs.
3. Archive strict validation stdout/stderr, generated cross-validation CSV, environment and hashes.
4. Reproduce any reported baseline comparison statistics from paired raw rounds and report uncertainty.
5. Compile the exact manuscript in CI, archive the PDF/build logs, and inspect references, tables, figure quality and overflows.
6. Re-run all gates on the exact final commit and associate the final release tag with that commit.

## Verdict
This release candidate is a reader-facing map of the code, model and recorded evidence, paired with a candid manuscript audit. It is **not** a certification that the complete paper is submission-ready. The 9,450-case physical claim remains excluded, predictive superiority is not established, and the exact manuscript build remains an outstanding gate.
