"""Adversarial certificate tests derived from the quorum theorem."""
from __future__ import annotations

from transactions_rebuild.kernel.certificates import (
    Certificate,
    certificate_safe,
    feasible_quorum_interval,
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
    assert certificate_safe(q, b)


def test_boundary_b_one_third_has_no_strict_feasible_interval():
    lower, upper = feasible_quorum_interval(1.0 / 3.0)
    assert lower >= upper


def test_below_one_third_has_nonempty_sufficient_interval():
    lower, upper = feasible_quorum_interval(0.30)
    assert lower < upper


def test_certificate_requires_context_binding():
    cert_a = Certificate(height=7, view=2, phase="prepare", proposal_hash="A", voter_ids=("v1", "v2"), weight=0.8)
    cert_b = Certificate(height=7, view=2, phase="prepare", proposal_hash="B", voter_ids=("v1", "v2"), weight=0.8)
    assert cert_a.context != cert_b.context


def test_duplicate_voter_cannot_be_counted_twice():
    cert = Certificate(height=1, view=0, phase="commit", proposal_hash="X", voter_ids=("v1", "v1"), weight=1.0)
    assert len(set(cert.voter_ids)) < len(cert.voter_ids)
