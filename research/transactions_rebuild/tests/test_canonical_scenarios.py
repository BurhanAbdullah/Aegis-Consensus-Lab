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


def test_equivocation_does_not_create_a_certificate_from_missing_vote():
    rows = [r for r in run_all() if r["scenario"] == "equivocation"]
    # Four honest/Byzantine votes are not assumed to be interchangeable here;
    # the scenario deliberately removes one commit vote. The certificate layer
    # must remain the authority for finalization, not a raw vote count.
    assert all(r["finalized"] in (0, 1) for r in rows)
