"""Independent oracle tests for production-kernel equivalence."""
import copy
import numpy as np

from kernel.tag4_kernel import AegisKernel, Params, ValidatorState
from reference_model import ReferenceState, reference_step


def _validators():
    return [
        ValidatorState("v1", [1.0, 0.8, 0.6, 0.4], risk=0.1),
        ValidatorState("v2", [0.9, 0.7, 0.5, 0.3], risk=0.2),
        ValidatorState("v3", [0.8, 0.6, 0.4, 0.2], risk=0.3),
    ]


def _assert_close(a, b, tol=1e-12):
    np.testing.assert_allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), rtol=0.0, atol=tol)


def test_reference_matches_kernel_across_deterministic_trace():
    params = Params(rho=0.13, ell=0.27, risk_memory=0.73, risk_gain=0.19, kappa=0.42,
                    q0=0.58, alpha_q=0.24, q_min=0.50, q_max=0.97)
    weights = (0.40, 0.30, 0.15, 0.15)
    kernel = AegisKernel(copy.deepcopy(_validators()), weights=weights, params=params)
    ref = ReferenceState(
        trust=tuple(tuple(v.trust) for v in _validators()),
        risk=tuple(v.risk for v in _validators()),
    )
    scenarios = [
        ({"v1": 0.0, "v2": 0.2, "v3": 0.9}, {"v1": 0.1, "v2": 0.0, "v3": 0.4}),
        ({"v1": 1.0, "v2": 0.7, "v3": 0.1}, {"v1": 0.8, "v2": 0.2, "v3": 0.0}),
        ({"v1": 0.35, "v2": 0.55, "v3": 0.75}, {"v1": 0.3, "v2": 0.5, "v3": 0.7}),
        ({"v1": 0.95, "v2": 0.05, "v3": 0.45}, {"v1": 0.0, "v2": 1.0, "v3": 0.5}),
    ]
    for evidence, drift in scenarios:
        tr = kernel.step(evidence, drift)
        out = reference_step(ref, [evidence[x] for x in ("v1", "v2", "v3")],
                             [drift[x] for x in ("v1", "v2", "v3")], weights, params)
        ref = out["state"]
        _assert_close(tr.tau.values(), out["tau"])
        _assert_close(tr.risk.values(), out["risk"])
        _assert_close([tr.influence[x] for x in ("v1", "v2", "v3")], out["influence"])
        assert abs(tr.quorum_fraction - out["q"]) <= 1e-12
        assert abs(tr.total_weight - out["total_weight"]) <= 1e-12
        assert abs(tr.quorum_weight - out["quorum_weight"]) <= 1e-12


def test_reference_and_kernel_agree_at_clipping_extremes():
    params = Params(rho=0.2, ell=0.9, risk_memory=0.8, risk_gain=0.7, kappa=1.0)
    weights = (0.4, 0.3, 0.15, 0.15)
    initial = [ValidatorState("v1", [0.0, 1.0, 0.5, 0.2]), ValidatorState("v2", [1.0, 0.0, 0.2, 0.8])]
    kernel = AegisKernel(copy.deepcopy(initial), weights=weights, params=params)
    ref = ReferenceState(tuple(tuple(v.trust) for v in initial), tuple(v.risk for v in initial))
    out = reference_step(ref, [1.0, 0.0], [1.0, 0.0], weights, params)
    tr = kernel.step({"v1": 1.0, "v2": 0.0}, {"v1": 1.0, "v2": 0.0})
    _assert_close([x for row in tr.trust.values() for x in row], out["trust"].ravel())
    _assert_close(tr.risk.values(), out["risk"])
    _assert_close(tr.tau.values(), out["tau"])
    assert abs(tr.quorum_fraction - out["q"]) <= 1e-12
