from reference_model import (
    project01, trust_step, trust_equilibrium, influence,
    quorum_fraction, safety_availability_interval,
)
import numpy as np


def test_projection_invariant():
    x = project01(np.array([-2.0, 0.2, 3.0]))
    assert np.all((x >= 0) & (x <= 1))


def test_equilibrium_reference():
    rho, ell, e = 0.2, 0.3, 0.5
    tau_star = trust_equilibrium(rho, ell, e)
    tau = 0.1
    for _ in range(2000):
        tau = float(trust_step(tau, rho, ell, e))
    assert abs(tau - tau_star) < 1e-8


def test_zero_loss_equilibrium():
    assert trust_equilibrium(0.2, 0.0, 0.8) == 1.0


def test_influence_bounds():
    g = influence(np.array([0.0, 0.5, 1.0]), np.array([0.0, 0.2, 1.0]), 0.8)
    assert np.all((g >= 0) & (g <= 1))


def test_quorum_clipping():
    q = quorum_fraction(0.2, 0.5, 0.8, 0.5, 0.9)
    assert 0.5 <= q <= 0.9


def test_quorum_interval_empty_at_one_third():
    lo, hi = safety_availability_interval(1/3)
    assert abs(lo - hi) < 1e-12


def test_quorum_interval_nonempty_below_one_third():
    lo, hi = safety_availability_interval(0.2)
    assert lo < hi
