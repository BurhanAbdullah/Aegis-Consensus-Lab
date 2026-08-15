# Transactions Release Provenance Manifest v1

This manifest freezes the provenance of the Transactions implementation/data/figure release on the `tag4` lineage. It is an audit index, not a substitute for raw evidence.

## Frozen lineage

- Historical source boundary: `tag4`
- Transactions hardening successor: `tag4-transactions-10of10-v13`
- Successor under finalization: `tag4-transactions-10of10-v14`
- Canonical validated implementation commit: `bdbfacbf548f0b46d0a62e2b0cc7b5b2c3c38aa1`
- Validation workflow: `tag4-transactions-strict` run #20 — success
- Tag4 validation workflow: `tag4-validation` run #109 — success

## Canonical model / mathematics

| Artifact | Role |
|---|---|
| `research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md` | Authoritative state, detector, governance, certificate and safety model |
| `research/transactions_rebuild/COUPLED_JACOBIAN_v1.md` | Coupled Jacobian definition |
| `research/transactions_rebuild/PROOF_OBLIGATIONS.md` | Theorem/proof obligations |
| `research/transactions_rebuild/ADVERSARIAL_VALIDATION_v1.md` | Adversarial validation scope |
| `research/transactions_rebuild/benchmarks/strict_cross_validation.py` | Independent mathematical cross-validation |
| `research/transactions_rebuild/tests/test_strict_mathematical_validation.py` | Mathematical validation tests |
| `research/transactions_rebuild/tests/test_weighted_quorum_validation.py` | Independent weighted-quorum validation |

## Frozen numerical inputs

| Artifact | Role | Git blob SHA |
|---|---|---|
| `archive/final_run/experiments/results.csv` | Frozen 200-round reference trace | `21399bd0ccf0d883e22743a390afc10ecc47083f` |
| `archive/final_run/experiments/results_predictive.csv` | Frozen 200-round predictive trace | `e930530eb4fd11c5a64b002d67922f27a2eb99c3` |
| `archive/final_run/experiments/phase_space.csv` | Phase-space source data | `162900105c206cb779cd3c180902630be1063cc7` |
| `archive/final_run/experiments/phase_space_baseline.csv` | Baseline phase-space data | `9ab1934ed3aa10a03f54741854e490ec8ea84d96` |
| `archive/final_run/experiments/phase_space_predictive.csv` | Predictive phase-space data | `773305fb62a4570020fd680377713537adfb4182` |
| `archive/final_run/experiments/topology_deformation_summary.csv` | Topology deformation summary | `9f3f8e9026e0a77d9fc18794a0c6dd5329192272` |

## Publication figures

| Artifact | Format | Git blob SHA |
|---|---|---|
| `archive/final_run/figures/baseline_heatmap_publication.pdf` | PDF | `20e614e2ee89631564d867a1e089beacfb5e967d` |
| `archive/final_run/figures/baseline_heatmap_publication.png` | PNG | `cb41b919fc0f150254e48943131aefa23fa67482` |
| `archive/final_run/figures/predictive_heatmap_publication.pdf` | PDF | `02b3bbc386606282dab56477b6a42158ac38daff` |
| `archive/final_run/figures/predictive_heatmap_publication.png` | PNG | `b9134b17b3837a70ed77a98675ce77f6a2a11190` |
| `archive/final_run/figures/difference_heatmap_publication.pdf` | PDF | `b0c5ea31703a91769c41245677155f407b11a18f` |
| `archive/final_run/figures/difference_heatmap_publication.png` | PNG | `0c694cf070906c2ea7a1771446c9bba7cd58a018` |
| `archive/final_run/figures/comparative_governance_landscapes_publication.pdf` | PDF | `d59a3a9be9d7176b204c9fecf3c1871854a99b30` |
| `archive/final_run/figures/comparative_governance_landscapes_publication.png` | PNG | `d9395e90bd4eab8078c3241f269bde1e428ced12` |
| `archive/final_run/figures/phase_space_publication.png` | PNG | `8f260b38c9985d2f0bed13405fe863faf0899e46` |
| `archive/final_run/figures/regime_classification_map.pdf` | PDF | `dc7baa3f243b1da4861824cd29556efa3a76808d` |

## Derived publication artifacts

The following are generated deterministically from the frozen 200-round traces and must never be hand-edited:

- `experiments/publication_comparison.csv`
- `experiments/publication_tables.tex`

Generator:
`research/transactions_rebuild/benchmarks/generate_publication_tables.py`

The generator fail-closes on missing inputs, schema errors, non-numeric fields, incorrect round coverage, or mismatched reference/predictive round IDs.

## Validation record

The strict validation run completed successfully with:

- 77 Transactions tests passed;
- 1,000 independent mathematical cross-validation cases;
- maximum equilibrium residual `1.1102230246251565e-16`;
- maximum finite-difference Jacobian relative error `9.648334450896133e-11`;
- zero stability-classification mismatches;
- deterministic repeated cross-validation byte-identical to the first run;
- publication comparison artifacts generated successfully.

## Claim boundary

The historical 9,450-case physical-system validation claim is **not** part of this release. The raw case-level evidence is absent and therefore no figure/table in this release may be presented as an independently reproduced 9,450-case physical validation.

The mathematical theorems are conditional on their stated assumptions. In particular:

1. The canonical Jacobian theorem concerns interior dynamics with exogenous detector inputs.
2. Endogenous detector dynamics require the corresponding augmented state/Jacobian and are not implied by the exogenous-input result.
3. The scalar quorum expression is a homogeneous reference boundary, not the general heterogeneous governance boundary.
4. Deterministic recurrence tests do not establish stochastic convergence.
5. Protocol comparisons must be assumption-equivalent; no PBFT/HotStuff equivalence is claimed without equivalent implementations and assumptions.

## Submission-control status

**Implementation/data/figure provenance: PASS.**

**Manuscript compilation: NOT CERTIFIED BY THIS REPOSITORY.** The repository contains the canonical model/audit and release artifacts but no authoritative manuscript `.tex` source. Therefore this manifest deliberately does not claim final manuscript compilation or submission readiness.
