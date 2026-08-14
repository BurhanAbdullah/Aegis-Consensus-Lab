from research.transactions_rebuild.benchmarks.comparative_grid import (
    ATTACK_SETS, DRIFT_LEVELS, EVIDENCE_LEVELS, SEEDS,
)
from research.transactions_rebuild.benchmarks.ablation import VARIANTS
from research.transactions_rebuild.benchmarks.localization import MAGNITUDES, DRIFTS, VALIDATORS


def test_comparative_grid_cardinality():
    assert len(ATTACK_SETS) == 14
    assert len(ATTACK_SETS) * len(DRIFT_LEVELS) * len(EVIDENCE_LEVELS) * len(SEEDS) == 14 * 5 * 6 * 10


def test_ablation_cardinality():
    assert len(VARIANTS) == 5


def test_localization_cardinality():
    assert len(VALIDATORS) * len(MAGNITUDES) * len(DRIFTS) * len(SEEDS) == 4 * 5 * 4 * 10


def test_experiment_ranges():
    assert all(0.0 <= x <= 1.0 for x in EVIDENCE_LEVELS)
    assert all(0.0 <= x <= 1.0 for x in DRIFT_LEVELS)
    assert all(0.0 <= x <= 1.0 for x in MAGNITUDES)
    assert all(0.0 <= x <= 1.0 for x in DRIFTS)
