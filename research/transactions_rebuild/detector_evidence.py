"""Deterministic detector-to-evidence mapping for the tag4 rebuild.

The mapping is transparent: detector channels are normalized, weighted, and
clipped into validator-specific evidence E in [0,1]. The canonical temporal
drift D is computed only from consecutive normalized detector observations.
No random state, attack generation, or paper-only calibration is performed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


CHANNELS = ("nis", "cusum", "jacobian", "temporal_risk")


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
    """Map a non-negative detector residual to [0,1]."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    return clip01(max(float(residual), 0.0) / float(threshold))


def normalized_scores(detector: Mapping[str, float], thresholds: Mapping[str, float]) -> dict[str, float]:
    """Return normalized detector scores in the canonical channel order."""
    if set(detector) != set(CHANNELS) or set(thresholds) != set(CHANNELS):
        raise ValueError(f"detector and thresholds must contain exactly {CHANNELS}")
    return {k: residual_to_score(detector[k], thresholds[k]) for k in CHANNELS}


def build_evidence(
    detector: Mapping[str, float],
    thresholds: Mapping[str, float],
    weights: EvidenceWeights = EvidenceWeights(),
) -> float:
    """Construct deterministic normalized evidence from four detector channels."""
    scores = normalized_scores(detector, thresholds)
    return clip01(sum(getattr(weights, k) * scores[k] for k in CHANNELS))


def temporal_drift(current_scores: Sequence[float], previous_scores: Sequence[float] | None = None) -> float:
    """Canonical observable temporal drift D.

    Scores are normalized detector channels in [0,1]. For four channels the
    maximum Euclidean distance is sqrt(4)=2, hence division by 2 normalizes the
    distance to [0,1]. The first round has D=0 unless a prior vector is given.
    """
    current = np.asarray(current_scores, dtype=float)
    if current.shape != (4,) or np.any((current < 0) | (current > 1)):
        raise ValueError("current_scores must be a length-4 vector in [0,1]")
    if previous_scores is None:
        return 0.0
    previous = np.asarray(previous_scores, dtype=float)
    if previous.shape != (4,) or np.any((previous < 0) | (previous > 1)):
        raise ValueError("previous_scores must be a length-4 vector in [0,1]")
    return clip01(np.linalg.norm(current - previous) / 2.0)


def build_evidence_and_drift(
    detector: Mapping[str, float],
    thresholds: Mapping[str, float],
    previous_detector: Mapping[str, float] | None = None,
    weights: EvidenceWeights = EvidenceWeights(),
) -> tuple[dict[str, float], float, float]:
    """Return normalized scores, evidence E, and observable drift D."""
    scores = normalized_scores(detector, thresholds)
    previous_scores = None if previous_detector is None else normalized_scores(previous_detector, thresholds)
    ordered = [scores[k] for k in CHANNELS]
    prev_ordered = None if previous_scores is None else [previous_scores[k] for k in CHANNELS]
    return scores, build_evidence(detector, thresholds, weights), temporal_drift(ordered, prev_ordered)


def build_validator_evidence(
    detector_by_validator: Mapping[str, Mapping[str, float]],
    thresholds: Mapping[str, float},
    weights: EvidenceWeights = EvidenceWeights(),
) -> dict[str, float]:
    """Apply the same documented mapping independently to each validator."""
    return {
        validator: build_evidence(channels, thresholds, weights)
        for validator, channels in sorted(detector_by_validator.items())
    }
