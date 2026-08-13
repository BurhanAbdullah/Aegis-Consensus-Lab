"""Deterministic detector-to-evidence mapping for the tag4 rebuild.

The mapping is intentionally transparent: detector channels are normalized,
weighted, and clipped into validator-specific evidence e in [0, 1].
No random state, attack generation, or paper-only calibration is performed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np


@dataclass(frozen=True)
class EvidenceWeights:
    nis: float = 0.25
    cusum: float = 0.25
    jacobian: float = 0.25
    temporal_risk: float = 0.25

    def __post_init__(self) -> None:
        values = np.asarray([self.nis, self.cusum, self.jacobian, self.temporal_risk], dtype=float)
        if np.any(values < 0) or not np.isclose(values.sum(), 1.0):
            raise ValueError("Evidence weights must be non-negative and sum to one.")


def clip01(x: float) -> float:
    return float(np.clip(float(x), 0.0, 1.0))


def residual_to_score(residual: float, threshold: float) -> float:
    """Map a non-negative detector residual to [0,1].

    Zero residual maps to zero evidence; the configured threshold maps to one.
    Values above threshold saturate. Thresholds must be positive and represent
    detector-level quantities, not manuscript results.
    """
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    return clip01(max(float(residual), 0.0) / float(threshold))


def build_evidence(
    detector: Mapping[str, float],
    thresholds: Mapping[str, float],
    weights: EvidenceWeights = EvidenceWeights(),
) -> float:
    """Construct deterministic normalized evidence from four detector channels.

    Required detector keys: nis, cusum, jacobian, temporal_risk.
    Required threshold keys: same names. All values are interpreted as
    non-negative detector scores; the output is a scalar e in [0,1].
    """
    keys = ("nis", "cusum", "jacobian", "temporal_risk")
    if set(detector) != set(keys) or set(thresholds) != set(keys):
        raise ValueError(f"detector and thresholds must contain exactly {keys}")
    scores = {k: residual_to_score(detector[k], thresholds[k]) for k in keys}
    return clip01(
        weights.nis * scores["nis"]
        + weights.cusum * scores["cusum"]
        + weights.jacobian * scores["jacobian"]
        + weights.temporal_risk * scores["temporal_risk"]
    )


def build_validator_evidence(
    detector_by_validator: Mapping[str, Mapping[str, float]],
    thresholds: Mapping[str, float],
    weights: EvidenceWeights = EvidenceWeights(),
) -> dict[str, float]:
    """Apply the same documented mapping independently to each validator."""
    return {
        validator: build_evidence(channels, thresholds, weights)
        for validator, channels in sorted(detector_by_validator.items())
    }
