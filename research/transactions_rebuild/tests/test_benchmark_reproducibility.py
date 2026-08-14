from research.transactions_rebuild.benchmarks.canonical_scenarios import SCENARIOS, SEEDS, run_all
from research.transactions_rebuild.benchmarks.comparative_reference import run_compare, summary


def test_canonical_benchmark_matrix_and_repeatability():
    first = run_all()
    second = run_all()
    assert len(first) == len(SCENARIOS) * len(SEEDS) * 30
    assert first == second
    assert {r["scenario"] for r in first} == set(SCENARIOS)
    assert {r["seed"] for r in first} == set(SEEDS)


def test_fixed_quorum_reference_uses_same_matrix():
    rows = run_compare()
    assert len(rows) == len(SCENARIOS) * len(SEEDS) * 30
    result = summary(rows)
    assert set(result) == set(SCENARIOS)
    for values in result.values():
        assert values["seed_count"] == len(SEEDS)
        assert 0.0 <= values["aegis_mean"] <= 1.0
        assert 0.0 <= values["fixed_quorum_mean"] <= 1.0
        assert values["aegis_ci95_low"] <= values["aegis_mean"] <= values["aegis_ci95_high"]
        assert values["fixed_quorum_ci95_low"] <= values["fixed_quorum_mean"] <= values["fixed_quorum_ci95_high"]
