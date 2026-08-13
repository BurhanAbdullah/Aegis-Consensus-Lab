import copy

from tag4_kernel import AegisKernel, Params, ValidatorState


def validators():
    return [
        ValidatorState("v1", [1.0, 1.0, 1.0, 1.0]),
        ValidatorState("v2", [0.8, 0.9, 0.7, 0.9]),
        ValidatorState("v3", [0.6, 0.7, 0.8, 0.7]),
    ]


def test_domain_invariance():
    k = AegisKernel(validators())
    for _ in range(100):
        t = k.step(
            {"v1": 1.0, "v2": 0.4, "v3": 0.0},
            {"v1": 1.0, "v2": 0.2, "v3": 0.0},
        )
        assert 0.5 <= t.quorum_fraction <= 0.99
        assert 0.0 <= t.total_weight
        assert 0.0 <= t.quorum_weight
        for tau in t.tau.values():
            assert 0.0 <= tau <= 1.0
        for r in t.risk.values():
            assert 0.0 <= r <= 1.0


def test_replay_is_deterministic():
    a = AegisKernel(copy.deepcopy(validators()))
    b = AegisKernel(copy.deepcopy(validators()))
    scenarios = [
        ({"v1": .1, "v2": .2, "v3": .3}, {"v1": 0, "v2": .1, "v3": .2}),
        ({"v1": .9, "v2": .8, "v3": .7}, {"v1": .3, "v2": .2, "v3": .1}),
        ({"v1": .2, "v2": .1, "v3": .0}, {"v1": .1, "v2": .1, "v3": .0}),
    ]
    for e, d in scenarios:
        x = a.step(e, d)
        y = b.step(e, d)
        assert x.quorum_fraction == y.quorum_fraction
        assert x.finalized == y.finalized
        assert x.tau == y.tau
        assert x.risk == y.risk


def test_equation_reference_single_validator():
    p = Params(rho=.2, ell=.3)
    k = AegisKernel([ValidatorState("v", [1, 1, 1, 1])], params=p)
    k.step({"v": .5}, {"v": 0})
    expected = 1.0 + .2 * (1 - 1.0) - .3 * .5 * 1.0
    assert abs(k.validators[0].trust[0] - expected) < 1e-12
