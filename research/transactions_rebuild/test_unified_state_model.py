import numpy as np
from .unified_state_model import ReducedParams, equilibrium, interior_step, jacobian_interior, spectral_radius, jury_conditions_2x2, governance_quorum


def test_equilibrium_is_fixed_point_for_interior_case():
    p = ReducedParams(c=0.02)
    e, d = 0.2, 0.1
    x = equilibrium(e, d, p)
    assert np.allclose(interior_step(x, e, d, p), x)
    assert 0 < x[0] < 1 and 0 < x[1] < 1


def test_jacobian_matches_finite_difference():
    p = ReducedParams()
    e = 0.25
    x = np.array([0.7, 0.3])
    h = 1e-7
    J_num = np.column_stack([(interior_step(x + np.eye(2)[j] * h, e, 0.1, p) - interior_step(x - np.eye(2)[j] * h, e, 0.1, p)) / (2*h) for j in range(2)])
    assert np.allclose(J_num, jacobian_interior(e, p), atol=1e-8)


def test_jury_and_spectral_radius_agree():
    J = jacobian_interior(0.2, ReducedParams())
    assert jury_conditions_2x2(J)["stable"]
    assert spectral_radius(J) < 1


def test_quorum_is_bounded():
    p = ReducedParams()
    q, threshold, influence = governance_quorum(0.8, 0.1, p)
    assert p.q_min <= q <= p.q_max
    assert 0 <= influence <= 1
    assert threshold == q * influence
