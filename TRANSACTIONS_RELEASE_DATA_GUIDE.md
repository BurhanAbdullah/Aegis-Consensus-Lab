# Transactions Release Data Guide

Validated Transactions implementation/research release lineage:

- Source: `tag4`
- Validated implementation commit: `bdbfacbf548f0b46d0a62e2b0cc7b5b2c3c38aa1`
- Release branch: `tag4-transactions-release-candidate-v2`

## Paper data and figures

### Frozen round-level traces
- `archive/final_run/experiments/results.csv`
- `archive/final_run/experiments/results_predictive.csv`

### Frozen phase-space / comparison data
- `archive/final_run/experiments/phase_space.csv`
- `archive/final_run/experiments/phase_space_baseline.csv`
- `archive/final_run/experiments/phase_space_predictive.csv`
- `archive/final_run/experiments/topology_deformation_summary.csv`

### Figures already included in the release lineage
- `archive/final_run/experiments/baseline_heatmap.png`
- `archive/final_run/experiments/predictive_heatmap.png`
- `archive/final_run/experiments/difference_heatmap.png`
- `archive/final_run/experiments/phase_space.png`
- `archive/final_run/experiments/phase_space_publication.png`

### Reproducible summary tables
- `experiments/publication_comparison.csv`
- `experiments/publication_tables.tex`

The publication-table generator is fail-closed: it validates the required schema, exactly 200 rounds, numeric fields, round IDs 1..200, and paired round identity before writing outputs.

### Mathematical audit outputs
- `experiments/strict_cross_validation.csv`
- `research/transactions_rebuild/benchmarks/strict_cross_validation.py`
- `research/transactions_rebuild/tests/test_strict_mathematical_validation.py`
- `research/transactions_rebuild/tests/test_weighted_quorum_validation.py`

### Canonical theory/model
- `research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md`
- `research/transactions_rebuild/COUPLED_JACOBIAN_v1.md`
- `research/transactions_rebuild/PROOF_OBLIGATIONS.md`
- `research/transactions_rebuild/ADVERSARIAL_VALIDATION_v1.md`

## Validation provenance

The exact Transactions implementation commit passed both validation workflows:

1. `tag4-transactions-strict` run #20
2. `tag4-validation` run #109

The Transactions strict workflow included complete tests, independent mathematical cross-validation, repeated deterministic cross-validation, frozen-artifact comparison generation, artifact verification, and the implementation-only Transactions gate.

## Claims boundary

The historical 9,450-case physical-system claim is intentionally excluded from the validated release because the raw case-level trace bundle is not present. Do not use that claim in the paper or figures unless the raw evidence is later added and independently validated.
