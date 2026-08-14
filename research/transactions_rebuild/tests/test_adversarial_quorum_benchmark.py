from research.transactions_rebuild.benchmarks.adversarial_quorum_benchmark import benchmark


def test_adaptive_quorum_blocks_boundary_conflicting_certificate_pair():
    result = benchmark()
    assert result["boundary_conflict_exists"] is True
    assert result["adaptive_conflict_exists"] is False
