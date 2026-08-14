from tag4_kernel import AegisKernel, ValidatorState


def _validators():
    return [
        ValidatorState("v1", [1.0, 1.0, 1.0, 1.0]),
        ValidatorState("v2", [0.9, 0.9, 0.9, 0.9]),
        ValidatorState("v3", [0.8, 0.8, 0.8, 0.8]),
    ]


def test_kernel_finalization_comes_from_valid_certificate():
    k = AegisKernel(_validators())
    trace = k.step(
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        commit={"v1": True, "v2": True, "v3": True},
        height=7,
        view=2,
        proposal_id="P-A",
    )
    assert trace.finalized
    assert trace.certificate_weight >= trace.quorum_weight
    assert trace.certificate_voters == ("v1", "v2", "v3")


def test_kernel_does_not_finalize_below_certificate_threshold():
    k = AegisKernel(_validators())
    trace = k.step(
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        {"v1": 0.0, "v2": 0.0, "v3": 0.0},
        commit={"v1": True},
        height=7,
        view=2,
        proposal_id="P-A",
    )
    assert not trace.finalized
    assert trace.certificate_weight == 0.0
    assert trace.certificate_voters == ()
