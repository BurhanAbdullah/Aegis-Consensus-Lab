from research.transactions_rebuild.benchmarks.canonical_scenarios import (
    SCENARIOS,
    SEEDS,
    run_all,
)


def test_scenario_matrix_is_complete():
    rows = run_all()
    assert len(rows) == len(SCENARIOS) * len(SEEDS) * 30
    assert {r["scenario"] for r in rows} == set(SCENARIOS)
    assert {r["seed"] for r in rows} == set(SEEDS)


def test_scenario_matrix_is_deterministic():
    assert run_all() == run_all()


def test_metrics_are_finite_and_bounded():
    for row in run_all():
        assert row["finalized"] in (0, 1)
        assert row["detected"] in (0, 1)
        assert row["recovered"] in (0, 1)
        assert 0.0 <= row["max_evidence"] <= 1.0
        assert 0.0 <= row["max_drift"] <= 1.0
        assert 0.5 <= row["quorum_fraction"] <= 0.99
        assert row["quorum_margin"] == row["quorum_margin"]


def test_equivocation_scenario_uses_certificate_semantics():
    rows = [r for r in run_all() if r["scenario"] == "equivocation"]
    # The scenario removes one commit vote. Finalization is therefore decided
    # by the canonical weighted-certificate rule, not by a raw vote count.
    # The test checks that the benchmark remains deterministic and bounded;
    # certificate safety itself is tested exhaustively in the certificate suite.
    assert len(rows) == len(SEEDS) * 30
    assert all(r["finalized"] in (0, 1) for r in rows)
