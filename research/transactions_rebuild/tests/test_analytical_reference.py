import math

from research.transactions_rebuild.analytical_reference import (
    ScalarParameters,
    availability_boundary,
    feasible,
    safety_boundary,
    trust_equilibrium,
    trust_multiplier,
)
from research.transactions_rebuild.kernel.tag4_kernel import AegisKernel, ValidatorState


def test_safety_and_availability_interval_is_nonempty_only_below_one_third_byzantine_weight():
    for b in (0.0, 0.1, 0.2, 0.3):
        assert safety_boundary(b) < availability_boundary(b)
    b = 1.0 / 3.0
    assert math.isclose(safety_boundary(b), availability_boundary(b))
    for b in (0.34, 0.5, 0.8):
        assert safety_boundary(b) > availability_boundary(b)


def test_closed_form_equilibrium_matches_kernel_limit():
    rho, ell, e = 0.10, 0.20, 0.30
    expected = trust_equilibrium(rho, ell, e)
    k = AegisKernel([ValidatorState("A", [0.20] * 4)])
    for _ in range(300):
        k.step({"A": e}, {"A": 0.0}, {"A": True}, {"A": True})
    tau = k.validators[0].tau(k.weights)
    assert math.isclose(tau, expected, rel_tol=1e-9, abs_tol=1e-9)


def test_kernel_local_multiplier_matches_analytical_multiplier():
    rho, ell, e = 0.11, 0.19, 0.22
    beta = trust_multiplier(rho, ell, e)
    k = AegisKernel([ValidatorState("A", [0.51] * 4)])
    k.step({"A": e}, {"A": 0.0}, {"A": True}, {"A": True})
    k.step({"A": e}, {"A": 0.0}, {"A": True}, {"A": True})
    x0 = k.validators[0].trust[0]
    k.step({"A": e}, {"A": 0.0}, {"A": True}, {"A": True})
    x1 = k.validators[0].trust[0]
    assert math.isclose((x1 - expected_equilibrium(rho, ell, e)) / (x0 - expected_equilibrium(rho, ell, e)), beta, rel_tol=1e-8, abs_tol=1e-8)


def expected_equilibrium(rho, ell, e):
    return rho / (rho + ell * e)


def test_reference_parameter_classification_has_both_sides_of_safety_boundary():
    params = ScalarParameters(rho=0.10, ell=0.20, q0=0.55, alpha_q=0.20)
    tau = trust_equilibrium(params.rho, params.ell, 0.40)
    q = params.q0 + params.alpha_q * (1.0 - tau)
    b = 0.20
    assert q > safety_boundary(b)
    assert feasible(q, b)
    b2 = 0.35
    assert not feasible(q, b2)
