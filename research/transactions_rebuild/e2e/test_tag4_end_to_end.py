from ..kernel.tag4_kernel import AegisKernel, ValidatorState
from .tag4_end_to_end import ScenarioRound, run_scenario


THRESHOLDS = {"nis": 1.0, "cusum": 1.0, "jacobian": 1.0, "temporal_risk": 1.0}


def scenario_for(values, drift, prepare=None, commit=None):
    return ScenarioRound(
        detector={
            vid: {"nis": x, "cusum": x, "jacobian": x, "temporal_risk": x}
            for vid, x in values.items()
        },
        thresholds=THRESHOLDS,
        drift=drift,
        prepare=prepare or {},
        commit=commit or {},
    )


def test_detector_to_governance_pipeline():
    validators = [
        ValidatorState("v1", [1, 1, 1, 1]),
        ValidatorState("v2", [.9, .9, .9, .9]),
        ValidatorState("v3", [.8, .8, .8, .8]),
    ]
    kernel = AegisKernel(validators)
    s = scenario_for(
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        {"v1": True, "v2": True, "v3": True},
        {"v1": True, "v2": True, "v3": True},
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
    normal = scenario_for({"v1": 0.0, "v2": 0.0}, {"v1": 0.0, "v2": 0.0})
    attacked = scenario_for({"v1": 0.0, "v2": 1.0}, {"v1": 0.0, "v2": 1.0})
    t0 = run_scenario(kernel, [normal])[0]
    t1 = run_scenario(kernel, [attacked])[0]
    assert t1.influence["v2"] < t0.influence["v2"]
