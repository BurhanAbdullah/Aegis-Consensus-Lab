"""Fail-closed verification of the Transactions release provenance manifest."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPECTED = {
    "archive/final_run/experiments/results.csv": "21399bd0ccf0d883e22743a390afc10ecc47083f",
    "archive/final_run/experiments/results_predictive.csv": "e930530eb4fd11c5a64b002d67922f27a2eb99c3",
    "archive/final_run/experiments/phase_space.csv": "162900105c206cb779cd3c180902630be1063cc7",
    "archive/final_run/experiments/phase_space_baseline.csv": "9ab1934ed3aa10a03f54741854e490ec8ea84d96",
    "archive/final_run/experiments/phase_space_predictive.csv": "773305fb62a4570020fd680377713537adfb4182",
    "archive/final_run/experiments/topology_deformation_summary.csv": "9f3f8e9026e0a77d9fc18794a0c6dd5329192272",
    "archive/final_run/figures/baseline_heatmap_publication.pdf": "20e614e2ee89631564d867a1e089beacfb5e967d",
    "archive/final_run/figures/baseline_heatmap_publication.png": "cb41b919fc0f150254e48943131aefa23fa67482",
    "archive/final_run/figures/predictive_heatmap_publication.pdf": "02b3bbc386606282dab56477b6a42158ac38daff",
    "archive/final_run/figures/predictive_heatmap_publication.png": "b9134b17b3837a70ed77a98675ce77f6a2a11190",
    "archive/final_run/figures/difference_heatmap_publication.pdf": "b0c5ea31703a91769c41245677155f407b11a18f",
    "archive/final_run/figures/difference_heatmap_publication.png": "0c694cf070906c2ea7a1771446c9bba7cd58a018",
    "archive/final_run/figures/comparative_governance_landscapes_publication.pdf": "d59a3a9be9d7176b204c9fecf3c1871854a99b30",
    "archive/final_run/figures/comparative_governance_landscapes_publication.png": "d9395e90bd4eab8078c3241f269bde1e428ced12",
    "archive/final_run/figures/phase_space_publication.png": "8f260b38c9985d2f0bed13405fe863faf0899e46",
    "archive/final_run/figures/regime_classification_map.pdf": "dc7baa3f243b1da4861824cd29556efa3a76808d",
}

REQUIRED_TEXT = [
    "research/transactions_rebuild/FINAL_MODEL_SPEC_v2.md",
    "research/transactions_rebuild/COUPLED_JACOBIAN_v1.md",
    "research/transactions_rebuild/PROOF_OBLIGATIONS.md",
    "research/transactions_rebuild/ADVERSARIAL_VALIDATION_v1.md",
    "research/transactions_rebuild/benchmarks/generate_publication_tables.py",
    "research/transactions_rebuild/MANUSCRIPT_MODEL_AUDIT_v1.md",
]


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def main() -> None:
    manifest = ROOT / "research/transactions_rebuild/TRANSACTIONS_RELEASE_PROVENANCE_MANIFEST_v1.md"
    if not manifest.is_file() or manifest.stat().st_size == 0:
        raise SystemExit("missing or empty release provenance manifest")

    for rel in REQUIRED_TEXT:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing required release-control artifact: {rel}")

    for rel, expected in EXPECTED.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"missing frozen release artifact: {rel}")
        actual = git_blob_sha(path)
        if actual != expected:
            raise SystemExit(f"provenance mismatch for {rel}: expected {expected}, got {actual}")

    print(f"verified {len(EXPECTED)} frozen data/figure artifacts and {len(REQUIRED_TEXT)} release-control artifacts")


if __name__ == "__main__":
    main()
