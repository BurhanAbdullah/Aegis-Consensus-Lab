"""Unit tests for the isolated Transactions-rebuild governance model."""
from __future__ import annotations

import math

from aegis_governance_model import (
    adaptive_quorum,
    governance_weight,
    influence_multiplier,
    risk_score,
    trust_equilibrium,
    trust_step,
    weighted_trust,
)


def test_trust_is_bounded():
    for t in (-1.0, 0.0, 0.2, 0.9, 1.0, 2.0):
        out = trust_step(t, rho=0.4, loss=0.3)
        assert 0.0 <= out <= 1.0


def test_affine_equilibrium_is_fixed_point():
    t_star = trust_equilibrium(0.2, 0.1)
    assert math.isclose(t_star, 2.0 / 3.0, rel_tol=1e-12)
    assert math.isclose(trust_step(t_star, 0.2, 0.1), t_star, rel_tol=1e-12)


def test_lambda_is_not_required_for_positive_affine_equilibrium():
    # rho/loss < 1, yet the affine recurrence has positive equilibrium.
    t_star = trust_equilibrium(0.1, 0.2)
    assert 0.0 < t_star < 1.0


def test_weighted_trust_is_normalized():
    assert math.isclose(weighted_trust([0.2, 0.8], [1.0, 3.0]), 0.65)


def test_prc_is_non_increasing_in_risk():
    vals = [influence_multiplier(r, threshold=0.25, kappa=0.8) for r in [0.0, 0.25, 0.5, 0.75, 1.0]]
    assert vals == sorted(vals, reverse=True)
    assert all(0.0 <= v <= 1.0 for v in vals)


def test_quorum_increases_as_trust_decreases():
    high = adaptive_quorum(0.9, 0.67, 0.2, 0.67, 0.95)
    low = adaptive_quorum(0.3, 0.67, 0.2, 0.67, 0.95)
    assert low >= high


def test_risk_contains_low_trust_component():
    low_trust = risk_score(0.1, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
    high_trust = risk_score(0.9, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
    assert low_trust > high_trust


def test_governance_weight_is_bounded():
    assert 0.0 <= governance_weight(0.8, 0.9, 0.25, 1.0) <= 1.0
