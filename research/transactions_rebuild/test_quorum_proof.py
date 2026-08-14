"""Executable checks for the weighted quorum inequalities."""

import math


def intersection_lower_bound(q):
    return 2.0 * q - 1.0


def test_safety_condition_exceeds_byzantine_weight():
    b = 0.20
    q = 0.61
    assert q > (1 + b) / 2
    assert intersection_lower_bound(q) > b


def test_conservative_availability_condition():
    b = 0.20
    q = 0.75
    assert q <= 1 - b


def test_classical_one_third_boundary():
    b = 1 / 3
    lo = (1 + b) / 2
    hi = 1 - b
    assert math.isclose(lo, hi, rel_tol=0.0, abs_tol=1e-15)
    assert not lo < hi


def test_near_boundary_is_not_rounded_into_safety():
    b = 0.30
    q = (1 + b) / 2
    assert not q > (1 + b) / 2
