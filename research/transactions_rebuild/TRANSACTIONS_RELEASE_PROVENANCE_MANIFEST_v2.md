# Transactions Release Provenance Manifest v2

This manifest freezes the provenance of the IEEE Transactions implementation/data/figure release candidate. It is an audit index, not a substitute for raw evidence.

## Frozen lineage

- Frozen base: `tag4`
- Frozen base commit: `4754590eec6f7fc3a3e9af47627af1f82afa0f14`
- Release candidate branch: `tag4-transactions-release-v1`
- No manuscript is required for the implementation release gate.

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

The release must preserve the existing frozen artifacts byte-for-byte. Their Git blob hashes are checked by `verify_release_provenance_v2.py`.

| Artifact | Git blob SHA |
|---|---|
| `archive/final_run/experiments/results.csv` | `21399bd0ccf0d883e22743a390afc10ecc47083f` |
| `archive/final_run/experiments/results_predictive.csv` | `e930530eb4fd11c5a64b002d67922f27a2eb99c3` |
| `archive/final_run/experiments/phase_space.csv` | `162900105c206cb779cd3c180902630be1063cc7` |
| `archive/final_run/experiments/phase_space_baseline.csv` | `9ab1934ed3aa10a03f54741854e490ec8ea84d96` |
| `archive/final_run/experiments/phase_space_predictive.csv` | `773305fb62a4570020fd680377713537adfb4182` |
| `archive/final_run/experiments/topology_deformation_summary.csv` | `9f3f8e9026e0a77d9fc18794a0c6dd5329192272` |

## Publication figures

The release preserves the existing publication-ready figures and their blob hashes:

| Artifact | Git blob SHA |
|---|---|
| `archive/final_run/figures/baseline_heatmap_publication.pdf` | `20e614e2ee89631564d867a1e089beacfb5e967d` |
| `archive/final_run/figures/baseline_heatmap_publication.png` | `cb41b919fc0f150254e48943131aefa23fa67482` |
| `archive/final_run/figures/predictive_heatmap_publication.pdf` | `02b3bbc386606282dab56477b6a42158ac38daff` |
| `archive/final_run/figures/predictive_heatmap_publication.png` | `b9134b17b3837a70ed77a98675ce77f6a2a11190` |
| `archive/final_run/figures/difference_heatmap_publication.pdf` | `b0c5ea31703a91769c41245677155f407b11a18f` |
| `archive/final_run/figures/difference_heatmap_publication.png` | `0c694cf070906c2ea7a1771446c9bba7cd58a018` |
| `archive/final_run/figures/comparative_governance_landscapes_publication.pdf` | `d59a3a9be9d7176b204c9fecf3c1871854a99b30` |
| `archive/final_run/figures/comparative_governance_landscapes_publication.png` | `d9395e90bd4eab8078c3241f269bde1e428ced12` |
| `archive/final_run/figures/phase_space_publication.png` | `8f260b38c9985d2f0bed13405fe863faf0899e46` |
| `archive/final_run/figures/regime_classification_map.pdf` | `dc7baa3f243b1da4861824cd29556efa3a76808d` |

## Derived publication artifacts

`experiments/publication_comparison.csv` and `experiments/publication_tables.tex` are generated deterministically from the frozen traces and are never hand-edited. The CI generator fail-closes on missing inputs, schema errors, non-numeric fields, incorrect round coverage, or mismatched round IDs.

## Validation requirements

A release candidate is valid only if the strict workflow passes all of:

1. complete Transactions pytest suite;
2. independent mathematical cross-validation;
3. byte-identical repeated cross-validation;
4. deterministic publication artifact generation;
5. frozen data/figure provenance verification;
6. implementation-only Transactions gate;
7. exact-head recording.

## Claim boundaries

- The historical 9,450-case physical-system claim is excluded because raw case-level evidence is absent.
- The Jacobian theorem is conditional on interior dynamics with exogenous detector inputs; endogenous detector dynamics require an augmented state/Jacobian.
- The scalar quorum expression is a homogeneous reference boundary, not a general heterogeneous governance theorem.
- Deterministic recurrence tests do not establish stochastic convergence.
- No PBFT/HotStuff equivalence or superiority claim is made without assumption-equivalent implementations.
- The implementation release does not certify manuscript compilation or paper submission readiness.

## Release decision

**PASS only after the exact release-candidate head completes the strict workflow successfully and provenance hashes remain unchanged.**
