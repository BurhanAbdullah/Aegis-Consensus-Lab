from detector_evidence import EvidenceWeights, build_evidence, build_validator_evidence


def test_evidence_is_bounded():
    thresholds = {"nis": 2.0, "cusum": 4.0, "jacobian": 1.0, "temporal_risk": 0.5}
    detector = {"nis": 20.0, "cusum": 20.0, "jacobian": 20.0, "temporal_risk": 20.0}
    assert build_evidence(detector, thresholds) == 1.0


def test_zero_detector_evidence_is_zero():
    thresholds = {k: 1.0 for k in ("nis", "cusum", "jacobian", "temporal_risk")}
    detector = {k: 0.0 for k in thresholds}
    assert build_evidence(detector, thresholds) == 0.0


def test_weights_are_explicit_and_normalized():
    thresholds = {k: 1.0 for k in ("nis", "cusum", "jacobian", "temporal_risk")}
    detector = {k: 0.0 for k in thresholds}
    detector["nis"] = 1.0
    w = EvidenceWeights(nis=0.7, cusum=0.1, jacobian=0.1, temporal_risk=0.1)
    assert abs(build_evidence(detector, thresholds, w) - 0.7) < 1e-12


def test_validator_mapping_is_deterministic_and_sorted():
    thresholds = {k: 1.0 for k in ("nis", "cusum", "jacobian", "temporal_risk")}
    zero = {k: 0.0 for k in thresholds}
    one = {k: 1.0 for k in thresholds}
    result = build_validator_evidence({"v2": one, "v1": zero}, thresholds)
    assert list(result) == ["v1", "v2"]
    assert result["v1"] == 0.0
    assert result["v2"] == 1.0


def test_invalid_weights_rejected():
    try:
        EvidenceWeights(nis=0.5, cusum=0.5, jacobian=0.5, temporal_risk=0.5)
    except ValueError:
        return
    raise AssertionError("invalid weights were accepted")
