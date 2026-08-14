"""Equation-to-production alignment tests for the tag4 scientific gate."""
from __future__ import annotations

import math

from kernel.tag4_kernel import AegisKernel, Params, ValidatorState
from reference_model import ReferenceState, reference_step


def test_reference_and_kernel_match_with_nondefault_active_threshold():
    params = Params(g_min=0.05)
    validators = [
        ValidatorState("A", [0.9, 0.8, 0.7, 0.6]),
        ValidatorState("B", [0.6, 0.7, 0.8, 0.9]),
        ValidatorState("C", [0.1, 0.2, 0.3, 0.4]),
    ]
    weights = (0.4, 0.3, 0.2, 0.1)
    evidence = {"A": 0.1, "B": 0.4, "C": 0.9}
    drift = {"A": 0.0, "B": 0.2, "C": 0.7}

    kernel = AegisKernel(validators, weights=weights, params=params)
    trace = kernel.step(evidence, drift)

    state = ReferenceState(
        trust=((0.9, 0.8, 0.7, 0.6), (0.6, 0.7, 0.8, 0.9), (0.1, 0.2, 0.3, 0.4)),
        risk=(0.0, 0.0, 0.0),
    )
    ref = reference_step(
        state,
        evidence=(0.1, 0.4, 0.9),
        drift=(0.0, 0.2, 0.7),
        weights=weights,
        params=params,
    )

    for vid in ("A", "B", "C"):
        assert all(math.isclose(a, b, rel_tol=0.0, abs_tol=1e-12)
                   for a, b in zip(trace.trust[vid], ref["trust"][{"A": 0, "B": 1, "C": 2}[vid]]))
        assert math.isclose(trace.tau[vid], ref["tau"][{"A": 0, "B": 1, "C": 2}[vid]], abs_tol=1e-12)
        assert math.isclose(trace.risk[vid], ref["risk"][{"A": 0, "B": 1, "C": 2}[vid]], abs_tol=1e-12)
        assert math.isclose(trace.influence[vid], ref["influence"][{"A": 0, "B": 1, "C": 2}[vid]], abs_tol=1e-12)

    assert math.isclose(trace.quorum_fraction, ref["q"], abs_tol=1e-12)
    assert math.isclose(trace.total_weight, ref["total_weight"], abs_tol=1e-12)
    assert math.isclose(trace.quorum_weight, ref["quorum_weight"], abs_tol=1e-12)
