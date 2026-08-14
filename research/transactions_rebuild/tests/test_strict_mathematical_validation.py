"""Independent mathematical cross-validation for the tag4 Transactions model."""
from __future__ import annotations

import numpy as np
import pytest

from research.transactions_rebuild.unified_state_model import (
    ReducedParams,
    equilibrium,
    full_equilibrium,
    full_interior_jacobian,
    full_interior_step,
    jury_conditions_2x2,
    spectral_radius,
    risk_containment,
)


def reference_trust_equilibrium(rho, ell, e):
    return rho / (rho + ell * e)


def reference_risk_equilibrium(a, c, e, d):
    return e + c * d / (1.0 - a)


def numerical_jacobian(fun, x, h=1e-6):
    x = np.asarray(x, dtype=float)
    J = np.zeros((np.asarray(fun(x)).size, x.size))
    for j in range(x.size):
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        J[:, j] = (fun(xp) - fun(xm)) / (2.0 * h)
    return J


def test_closed_form_equilibrium_identity():
    rng = np.random.default_rng(20260814)
    for _ in range(250):
        p = ReducedParams(rho=rng.uniform(0.02, 0.25), ell=rng.uniform(0.05, 0.35),
                          a=rng.uniform(0.20, 0.90), c=rng.uniform(0.02, 0.15))
        e, d = rng.uniform(0.0, 0.8), rng.uniform(0.0, 0.8)
        if not risk_containment(e, d, p):
            continue
        x = equilibrium(e, d, p)
        assert np.isclose(x[0], reference_trust_equilibrium(p.rho, p.ell, e), rtol=1e-12, atol=1e-12)
        assert np.isclose(x[1], reference_risk_equilibrium(p.a, p.c, e, d), rtol=1e-12, atol=1e-12)
        mapped = np.array([x[0] + p.rho*(1-x[0]) - p.ell*e*x[0],
                           p.a*x[1] + (1-p.a)*e + p.c*d])
        assert np.max(np.abs(mapped-x)) < 1e-11


def test_full_jacobian_matches_finite_difference():
    rng = np.random.default_rng(42)
    for _ in range(100):
        p = ReducedParams(rho=rng.uniform(.03,.2), ell=rng.uniform(.05,.3), a=rng.uniform(.2,.9), c=.08)
        e, d = rng.uniform(.05,.75), rng.uniform(.0,.5)
        x = np.r_[rng.uniform(.2,.8,4), rng.uniform(.1,.7)]
        J_exact = full_interior_jacobian(e, p, dimension=4)
        J_fd = numerical_jacobian(lambda z: full_interior_step(z, e, d, p), x)
        err = np.linalg.norm(J_exact-J_fd, ord='fro') / max(1.0, np.linalg.norm(J_exact, ord='fro'))
        assert err < 5e-8


def test_full_jacobian_spectral_radius_matches_eigenvalues():
    rng = np.random.default_rng(7)
    for _ in range(100):
        p = ReducedParams(rho=rng.uniform(.01,.25), ell=rng.uniform(.01,.4), a=rng.uniform(.01,.95))
        e = rng.uniform(0,1)
        J = full_interior_jacobian(e, p, dimension=6)
        beta = 1-p.rho-p.ell*e
        assert np.isclose(spectral_radius(J), max(abs(beta), abs(p.a)), rtol=1e-13, atol=1e-13)


def test_jury_matches_direct_schur_stability():
    rng = np.random.default_rng(8)
    for _ in range(500):
        J = rng.normal(0, .4, size=(2,2))
        direct = spectral_radius(J) < 1.0
        jury = jury_conditions_2x2(J)['stable']
        assert direct == jury


def test_risk_containment_boundary_is_strictly_respected():
    p = ReducedParams(a=.8, c=.2)
    # Equality: (1-a)E+cD = 1-a.
    assert risk_containment(0.8, 0.0, p)
    # Strict excess: .2*.8 + .2*.3 = .22 > .20.
    assert not risk_containment(0.8, 0.3, p)


def test_model_equivalence_full_equilibrium_residual():
    p = ReducedParams()
    x = full_equilibrium(.25, .10, p, dimension=4)
    nxt = full_interior_step(x, .25, .10, p)
    assert np.max(np.abs(nxt-x)) < 1e-12


def test_uncontained_equilibrium_is_rejected():
    p = ReducedParams(a=.95, c=.5)
    with pytest.raises(ValueError):
        full_equilibrium(.9, .9, p, dimension=4)
