from ..kernel.tag4_kernel import AegisKernel, ValidatorState
from .tag4_end_to_end import ScenarioRound, run_scenario


def test_detector_to_governance_pipeline():
    validators = [
        ValidatorState("v1", [1, 1, 1, 1]),
        ValidatorState("v2", [.9, .9, .9, .9]),
        ValidatorState("v3", [.8, .8, .8, .8]),
    ]
    kernel = AegisKernel(validators)
    s = ScenarioRound(
        nis={"v1": 0.0, "v2": 0.0, "v3": 0.0},
        cusum={"v1": 0.0, "v2": 0.0, "v3": 0.0},
        jacobian={"v1": 0.0, "v2": 0.0, "v3": 0.0},
        residual={"v1": 0.0, "v2": 0.0, "v3": 0.0},
        drift={"v1": 0.0, "v2": 0.0, "v3": 0.0},
        prepare={"v1": True, "v2": True, "v3": True},
        commit={"v1": True, "v2": True, "v3": True},
    )
    traces = run_scenario(kernel, [s])
    assert len(traces) == 1
    t = traces[0]
    assert t.finalized
    assert all(0 <= x <= 1 for x in t.evidence.values())
    assert all(0 <= x <= 1 for x in t.risk.values())
    assert 0.5 <= t.quorum_fraction <= 0.99


def test_attack_evidence_reduces_influence_relative_to_nominal():
    validators = [ValidatorState("v1", [1, 1, 1, 1]), ValidatorState("v2", [1, 1, 1, 1])]
    kernel = AegisKernel(validators)
    normal = ScenarioRound(
        nis={"v1": 0, "v2": 0}, cusum={"v1": 0, "v2": 0},
        jacobian={"v1": 0, "v2": 0}, residual={"v1": 0, "v2": 0},
        drift={"v1": 0, "v2": 0}, prepare={}, commit={}
    )
    attacked = ScenarioRound(
        nis={"v1": 0, "v2": 1}, cusum={"v1": 0, "v2": 1},
        jacobian={"v1": 0, "v2": 1}, residual={"v1": 0, "v2": 1},
        drift={"v1": 0, "v2": 1}, prepare={}, commit={}
    )
    t0 = run_scenario(kernel, [normal])[0]
    t1 = run_scenario(kernel, [attacked])[0]
    assert t1.influence["v2"] < t0.influence["v2"]
