import numpy as np

from .detector_evidence import CHANNELS, normalized_scores, temporal_drift
from .unified_state_model import ReducedParams, full_equilibrium, full_interior_jacobian, full_interior_step, spectral_radius, risk_containment


def _detector(v):
    return {k: v for k in CHANNELS}


def _thresholds():
    return {k: 1.0 for k in CHANNELS}


def test_temporal_drift_first_round_is_zero():
    scores = [0.2, 0.4, 0.6, 0.8]
    assert temporal_drift(scores) == 0.0


def test_temporal_drift_zero_for_identical_observations():
    scores = [0.2, 0.4, 0.6, 0.8]
    assert temporal_drift(scores, scores) == 0.0


def test_temporal_drift_max_distance_is_one():
    assert np.isclose(temporal_drift([1, 1, 1, 1], [0, 0, 0, 0]), 1.0)


def test_temporal_drift_is_observable_from_normalized_scores():
    current = normalized_scores(_detector(1.0), _thresholds())
    previous = normalized_scores(_detector(0.0), _thresholds())
    assert np.isclose(temporal_drift([current[k] for k in CHANNELS], [previous[k] for k in CHANNELS]), 1.0)


def test_full_jacobian_matches_finite_difference():
    p = ReducedParams(rho=0.13, ell=0.17, a=0.72)
    e, d = 0.31, 0.08
    x = np.array([0.35, 0.41, 0.52, 0.63, 0.27])
    h = 1e-7
    J_num = np.column_stack([
        (full_interior_step(x + np.eye(5)[j] * h, e, d, p) - full_interior_step(x - np.eye(5)[j] * h, e, d, p)) / (2*h)
        for j in range(5)
    ])
    J_exact = full_interior_jacobian(e, p, dimension=4)
    assert np.allclose(J_num, J_exact, atol=1e-8)


def test_full_equilibrium_is_fixed_point_when_contained():
    p = ReducedParams(c=0.02)
    e, d = 0.2, 0.1
    x = full_equilibrium(e, d, p, dimension=4)
    assert np.allclose(full_interior_step(x, e, d, p), x)
    assert np.all((x > 0) & (x < 1))


def test_full_spectral_radius_matches_closed_form():
    p = ReducedParams(rho=0.1, ell=0.2, a=0.8)
    e = 0.25
    J = full_interior_jacobian(e, p, dimension=4)
    beta = 1 - p.rho - p.ell * e
    assert np.isclose(spectral_radius(J), max(abs(beta), abs(p.a)))


def test_risk_containment_gate_rejects_unbounded_input():
    p = ReducedParams(a=0.8, c=0.3)
    assert not risk_containment(1.0, 1.0, p)
