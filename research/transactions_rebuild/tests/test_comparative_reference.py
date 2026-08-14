from research.transactions_rebuild.benchmarks.canonical_scenarios import SCENARIOS, SEEDS
from research.transactions_rebuild.benchmarks.comparative_reference import run_compare, summary


def test_comparison_uses_identical_scenarios_and_seeds():
    rows = run_compare()
    assert len(rows) == len(SCENARIOS) * len(SEEDS) * 30
    assert {r["scenario"] for r in rows} == set(SCENARIOS)
    assert {r["seed"] for r in rows} == set(SEEDS)


def test_comparison_metrics_are_bounded():
    for values in summary(run_compare()).values():
        assert 0.0 <= values["aegis_finalization_rate"] <= 1.0
        assert 0.0 <= values["fixed_quorum_finalization_rate"] <= 1.0
        assert values["mean_margin_difference"] == values["mean_margin_difference"]
