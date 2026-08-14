import math
import numpy as np
import pytest

from research.transactions_rebuild.detector_evidence import temporal_drift
from research.transactions_rebuild.kernel.certificates import (
    Vote,
    certificate,
    safety_condition,
    weighted_intersection_lower_bound,
)
from research.transactions_rebuild.kernel.tag4_kernel import AegisKernel, Params, ValidatorState


def test_temporal_drift_matches_canonical_normalization():
    a = [0.0, 0.0, 0.0, 0.0]
    b = [1.0, 1.0, 1.0, 1.0]
    assert temporal_drift(a) == 0.0
    assert math.isclose(temporal_drift(b, a), 1.0)
    c = [1.0, 0.0, 0.0, 0.0]
    assert math.isclose(temporal_drift(c, a), 0.5)


def test_scalar_trust_equilibrium_matches_iteration():
    rho, ell, e = 0.10, 0.20, 0.30
    beta = 1.0 - rho - ell * e
    tau_star = rho / (rho + ell * e)
    x = 0.17
    for _ in range(200):
        x = x + rho * (1.0 - x) - ell * e * x
    assert math.isclose(x, tau_star, rel_tol=1e-10, abs_tol=1e-10)
    assert abs(beta) < 1.0


def test_interior_jacobian_matches_finite_difference():
    rho, ell, e = 0.13, 0.27, 0.21
    a = 0.73
    beta = 1.0 - rho - ell * e

    def f(x):
        t1, t2, r = x
        return np.array([
            t1 + rho * (1 - t1) - ell * e * t1,
            t2 + rho * (1 - t2) - ell * e * t2,
            a * r + (1 - a) * e,
        ])

    x = np.array([0.61, 0.42, 0.37])
    h = 1e-6
    J_fd = np.column_stack([(f(x + h * np.eye(3)[j]) - f(x - h * np.eye(3)[j])) / (2 * h) for j in range(3)])
    J_expected = np.diag([beta, beta, a])
    assert np.allclose(J_fd, J_expected, atol=1e-8)
    assert math.isclose(max(abs(np.linalg.eigvals(J_expected))), max(abs(beta), abs(a)))


def test_jury_conditions_agree_with_eigenvalue_stability():
    rng = np.random.default_rng(12345)
    for _ in range(500):
        J = rng.uniform(-0.8, 0.8, size=(2, 2))
        tr = float(np.trace(J))
        det = float(np.linalg.det(J))
        jury = (1 - tr + det > 0) and (1 + tr + det > 0) and (1 - det > 0)
        spectral = max(abs(np.linalg.eigvals(J))) < 1.0
        assert jury == spectral


def test_quorum_intersection_boundary_is_strict():
    b = 0.20
    boundary = (1 + b) / 2
    assert math.isclose(weighted_intersection_lower_bound(boundary), b)
    assert not safety_condition(boundary, b)
    assert safety_condition(boundary + 1e-6, b)
    assert not safety_condition(boundary - 1e-6, b)


def test_certificate_rejects_duplicate_and_cross_context_votes():
    votes = [
        Vote("A", 1, 1, "commit", "p", 0.4),
        Vote("A", 1, 1, "commit", "p", 0.4),
    ]
    assert certificate(votes, 0.5) is None

    cross_context = [
        Vote("A", 1, 1, "commit", "p", 0.4),
        Vote("B", 1, 2, "commit", "p", 0.4),
    ]
    assert certificate(cross_context, 0.5) is None


def test_kernel_matches_closed_form_one_step_interior():
    p = Params(rho=0.10, ell=0.20, risk_memory=0.80, risk_gain=0.05)
    v = ValidatorState("A", [0.60, 0.60, 0.60, 0.60], risk=0.20)
    k = AegisKernel([v], params=p)
    e, d = {"A": 0.10}, {"A": 0.05}
    trace = k.step(e, d, {"A": True}, {"A": True})
    expected_t = 0.60 + p.rho * (1 - 0.60) - p.ell * 0.10 * 0.60
    expected_r = p.risk_memory * 0.20 + (1 - p.risk_memory) * 0.10 + p.risk_gain * 0.05
    assert math.isclose(trace.trust["A"][0], expected_t)
    assert math.isclose(trace.risk["A"], expected_r)
    assert math.isclose(trace.tau["A"], expected_t)


def test_projection_invariance_is_explicit():
    p = Params(rho=0.10, ell=2.0, risk_memory=0.80, risk_gain=1.0)
    v = ValidatorState("A", [0.0, 1.0, 0.5, 0.5], risk=1.0)
    k = AegisKernel([v], params=p)
    trace = k.step({"A": 1.0}, {"A": 1.0}, {"A": True}, {"A": True})
    assert all(0.0 <= x <= 1.0 for x in trace.trust["A"])
    assert 0.0 <= trace.risk["A"] <= 1.0


def test_risk_containment_condition_is_distinguished_from_projection():
    a, c = 0.8, 0.05
    E, D = 0.8, 0.2
    assert (1 - a) * E + c * D <= 1 - a
    E2, D2 = 1.0, 1.0
    assert (1 - a) * E2 + c * D2 > 1 - a
