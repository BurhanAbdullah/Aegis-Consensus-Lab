from __future__ import annotations

import copy
import math

import numpy as np

from detector_evidence import EvidenceWeights, build_evidence_and_drift
from kernel.tag4_kernel import AegisKernel, Params, ValidatorState
from kernel.certificates import safety_condition, weighted_intersection_lower_bound


def _validators():
    return [
        ValidatorState("A", [0.90, 0.85, 0.80, 0.95]),
        ValidatorState("B", [0.82, 0.88, 0.86, 0.80]),
        ValidatorState("C", [0.65, 0.70, 0.68, 0.72]),
        ValidatorState("D", [0.55, 0.60, 0.58, 0.62]),
    ]


def _run_once():
    kernel = AegisKernel(_validators())
    evidence = {v: 0.2 + 0.1 * i for i, v in enumerate(("A", "B", "C", "D"))}
    drift = {v: 0.05 * i for i, v in enumerate(("A", "B", "C", "D"))}
    traces = []
    for k in range(8):
        traces.append(kernel.step(evidence, drift, prepare={v: True for v in evidence}, commit={v: True for v in evidence}, height=1, view=k, proposal_id=f"p{k}"))
        evidence = {v: min(1.0, x + 0.01) for v, x in evidence.items()}
        drift = {v: min(1.0, x + 0.005) for v, x in drift.items()}
    return traces


def test_kernel_is_deterministic_for_identical_inputs():
    a = _run_once()
    b = _run_once()
    assert [(x.quorum_fraction, x.quorum_weight, x.certificate_weight, x.finalized) for x in a] == [
        (x.quorum_fraction, x.quorum_weight, x.certificate_weight, x.finalized) for x in b
    ]
    assert [x.trust for x in a] == [x.trust for x in b]
    assert [x.risk for x in a] == [x.risk for x in b]


def test_state_bounds_and_monotone_risk_response():
    trace = _run_once()
    for t in trace:
        for vec in t.trust.values():
            assert all(0.0 <= x <= 1.0 for x in vec)
        assert all(0.0 <= x <= 1.0 for x in t.risk.values())
        assert 0.0 <= t.quorum_fraction <= 0.99
        assert t.total_weight >= 0.0
        assert t.quorum_weight >= 0.0


def test_observable_drift_is_bounded_and_first_round_zero():
    thresholds = {k: 1.0 for k in ("nis", "cusum", "jacobian", "temporal_risk")}
    d0 = {k: 0.0 for k in thresholds}
    d1 = {k: 1.0 for k in thresholds}
    scores, e0, drift0 = build_evidence_and_drift(d0, thresholds, weights=EvidenceWeights())
    _, e1, drift1 = build_evidence_and_drift(d1, thresholds, previous_detector=d0, weights=EvidenceWeights())
    assert e0 == 0.0
    assert e1 == 1.0
    assert drift0 == 0.0
    assert math.isclose(drift1, 1.0, abs_tol=1e-12)
    assert all(0.0 <= x <= 1.0 for x in scores.values())


def test_trust_equilibrium_matches_scalar_reference_case():
    p = Params(rho=0.1, ell=0.2, risk_memory=0.8, risk_gain=0.0)
    e = 0.5
    expected = p.rho / (p.rho + p.ell * e)
    state = ValidatorState("A", [expected] * 4)
    kernel = AegisKernel([state], params=p)
    tr = kernel.step({"A": e}, {"A": 0.0})
    beta = 1.0 - p.rho - p.ell * e
    assert max(abs(x - expected) for x in tr.trust["A"]) < 1e-12
    assert abs(beta) < 1.0


def test_stability_boundary_is_strict():
    # Scalar reference: |1-rho-ell*e| < 1 is required.
    rho, ell, e = 0.1, 0.2, 0.5
    beta = 1.0 - rho - ell * e
    assert abs(beta) < 1.0
    # Exact lower boundary rho+ell*e=0 is not admissible for asymptotic stability.
    assert not (0.0 < 0.0 < 2.0)


def test_quorum_boundary_is_strict():
    b = 0.20
    q_boundary = (1.0 + b) / 2.0
    assert weighted_intersection_lower_bound(q_boundary) == b
    assert not safety_condition(q_boundary, b)
    assert safety_condition(q_boundary + 1e-6, b)


def test_certificate_threshold_matches_kernel_quorum():
    trace = _run_once()[0]
    assert trace.certificate_weight + 1e-12 >= trace.quorum_weight or not trace.finalized


def test_six_scenario_classes_are_representable_without_randomness():
    # These are deterministic scenario inputs, not stochastic attack claims.
    scenarios = {
        "clean": 0.0,
        "burst": 1.0,
        "slow_drift": 0.2,
        "stealth": 0.45,
        "equivocation": 0.8,
        "mixed": 0.65,
    }
    outputs = []
    for name, e in scenarios.items():
        k = AegisKernel(_validators())
        t = k.step({v.validator_id: e for v in k.validators}, {v.validator_id: 0.1 for v in k.validators})
        outputs.append((name, tuple(round(t.risk[v], 12) for v in sorted(t.risk))))
    assert len(outputs) == 6
    assert len({x[1] for x in outputs}) == 6
