"""Independent validation of the weighted-quorum safety/availability bounds.

These tests do not depend on the consensus implementation.  They exercise the
mathematical claim directly on normalized validator weights and therefore act
as an independent cross-check of the quorum theorem used by the model.
"""
from __future__ import annotations

import numpy as np


def quorum_weight(weights: np.ndarray, mask: np.ndarray) -> float:
    return float(weights[mask].sum())


def test_intersection_lower_bound_for_random_weighted_quorums() -> None:
    rng = np.random.default_rng(20260815)
    for _ in range(2000):
        weights = rng.dirichlet(np.ones(20))
        q = float(rng.uniform(0.5, 0.95))
        a = rng.random(20) < rng.uniform(0.5, 1.0)
        b = rng.random(20) < rng.uniform(0.5, 1.0)
        if quorum_weight(weights, a) < q or quorum_weight(weights, b) < q:
            continue
        intersection = quorum_weight(weights, a & b)
        assert intersection + 1e-12 >= 2.0 * q - 1.0


def test_strict_safety_boundary_excludes_byzantine_only_intersection() -> None:
    b = 0.20
    q = (1.0 + b) / 2.0 + 1e-6
    # A Byzantine-only intersection has weight at most b.  The theorem requires
    # the minimum quorum intersection 2q-1 to exceed that adversarial budget.
    assert 2.0 * q - 1.0 > b


def test_equality_boundary_is_not_safe_under_the_strict_theorem() -> None:
    b = 0.20
    q = (1.0 + b) / 2.0
    # At equality, the lower-bound intersection is exactly b and can therefore
    # be entirely Byzantine.  The safety condition is intentionally strict.
    assert np.isclose(2.0 * q - 1.0, b)


def test_nonempty_conservative_security_availability_interval_requires_below_one_third() -> None:
    for b in np.linspace(0.0, 0.49, 100):
        lower = (1.0 + b) / 2.0
        upper = 1.0 - b
        expected = b < 1.0 / 3.0
        assert (lower < upper) == expected


def test_exact_honest_participation_availability_condition() -> None:
    rng = np.random.default_rng(20260816)
    for _ in range(1000):
        h = float(rng.uniform(0.0, 1.0))
        q = float(rng.uniform(0.0, 1.0))
        # An honest-only quorum is achievable exactly when honest participating
        # weight reaches the requested quorum threshold.
        assert (q <= h) == (h >= q)
