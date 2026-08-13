from certificates import (
    Vote, certificate, conflicting_certificates,
    weighted_intersection_lower_bound, safety_condition,
    availability_condition, feasible_interval,
)


def votes(proposal, weights=(0.25, 0.25, 0.25, 0.25)):
    return [
        Vote(f"v{i}", 1, 0, "commit", proposal, w)
        for i, w in enumerate(weights)
    ]


def test_certificate_requires_quorum():
    c = certificate(votes("A")[:2], 0.75)
    assert c is None
    c = certificate(votes("A")[:3], 0.75)
    assert c is not None
    assert abs(c.weight - 0.75) < 1e-12


def test_duplicate_validator_is_rejected():
    v = votes("A")
    bad = [v[0], v[0], v[1], v[2]]
    assert certificate(bad, 0.5) is None


def test_context_mismatch_is_rejected():
    v = votes("A")
    bad = [v[0], Vote("v1", 2, 0, "commit", "A", 0.25), v[2]]
    assert certificate(bad, 0.5) is None


def test_conflicting_certificates_are_detected():
    a = certificate(votes("A")[:3], 0.5)
    b = certificate(votes("B")[:3], 0.5)
    assert a is not None and b is not None
    assert conflicting_certificates(a, b)


def test_intersection_bound():
    assert abs(weighted_intersection_lower_bound(2/3) - 1/3) < 1e-12


def test_safety_condition():
    assert safety_condition(0.7, 0.3)
    assert not safety_condition(0.65, 0.3)


def test_availability_condition():
    assert availability_condition(0.7, 0.7)
    assert not availability_condition(0.71, 0.7)


def test_feasible_interval_requires_below_one_third():
    lo, hi = feasible_interval(0.2)
    assert lo < hi
    lo, hi = feasible_interval(1/3)
    assert abs(lo - hi) < 1e-12
