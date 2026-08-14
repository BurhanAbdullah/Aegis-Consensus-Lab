"""Adversarial certificate tests derived from the quorum theorem."""
from __future__ import annotations

from transactions_rebuild.kernel.certificates import (
    Certificate,
    Vote,
    certificate,
    conflicting_certificates,
    feasible_interval,
    safety_condition,
)


def test_exact_intersection_boundary_is_unsafe():
    b = 0.30
    q = (1.0 + b) / 2.0
    assert not safety_condition(q, b)


def test_just_above_safety_boundary_is_safe():
    b = 0.30
    q = (1.0 + b) / 2.0 + 1e-9
    assert safety_condition(q, b)


def test_byzantine_weight_cannot_create_two_conflicting_safe_certificates():
    # Two q-quorums with total normalized weight 1 have intersection >= 2q-1.
    # If 2q-1>b, Byzantine weight alone cannot occupy the intersection.
    b = 0.25
    q = 0.63
    assert 2.0 * q - 1.0 > b
    assert safety_condition(q, b)


def test_boundary_b_one_third_has_no_strict_feasible_interval():
    lower, upper = feasible_interval(1.0 / 3.0)
    assert lower >= upper


def test_below_one_third_has_nonempty_sufficient_interval():
    lower, upper = feasible_interval(0.30)
    assert lower < upper


def test_certificate_requires_context_binding():
    cert_a = Certificate(height=7, view=2, phase="prepare", proposal_id="A", weight=0.8, voters=("v1", "v2"))
    cert_b = Certificate(height=7, view=2, phase="prepare", proposal_id="B", weight=0.8, voters=("v1", "v2"))
    assert conflicting_certificates(cert_a, cert_b)


def test_duplicate_voter_cannot_be_counted_twice():
    votes = [
        Vote("v1", 1, 0, "commit", "X", 0.5),
        Vote("v1", 1, 0, "commit", "X", 0.5),
    ]
    assert certificate(votes, 0.5) is None
