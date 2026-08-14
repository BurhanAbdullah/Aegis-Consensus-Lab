from research.transactions_rebuild.benchmarks.analytical_boundary_sweep import max_errors, run_sweep


def test_analytical_boundary_sweep_has_full_grid_and_zero_mismatch_away_from_boundary():
    rows = run_sweep()
    assert len(rows) == 21 * 7 * 13
    tau_error, q_error, classification_mismatches, near_boundary = max_errors(rows)
    assert tau_error < 1e-10
    assert q_error < 1e-10
    assert classification_mismatches == 0
    assert near_boundary >= 0
