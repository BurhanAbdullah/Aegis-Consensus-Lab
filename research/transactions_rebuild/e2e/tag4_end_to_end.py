"""End-to-end deterministic AEGIS experiment harness for tag4.

This harness composes detector evidence, trust/risk dynamics, governance
weights and weighted certificate accounting. It deliberately receives attack
and detector observations from the caller; it does not generate hidden
randomness.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List

from ..detector_evidence import DetectorObservation, EvidenceWeights, evidence_from_observation
from ..kernel.tag4_kernel import AegisKernel, ValidatorState


@dataclass(frozen=True)
class ScenarioRound:
    nis: Dict[str, float]
    cusum: Dict[str, float]
    jacobian: Dict[str, float]
    residual: Dict[str, float]
    drift: Dict[str, float]
    prepare: Dict[str, bool]
    commit: Dict[str, bool]


def run_scenario(kernel: AegisKernel, rounds: Iterable[ScenarioRound], weights: EvidenceWeights | None = None):
    weights = weights or EvidenceWeights()
    traces = []
    for s in rounds:
        evidence = {}
        for vid in s.nis:
            obs = DetectorObservation(
                nis=s.nis.get(vid, 0.0),
                cusum=s.cusum.get(vid, 0.0),
                jacobian=s.jacobian.get(vid, 0.0),
                residual=s.residual.get(vid, 0.0),
            )
            evidence[vid] = evidence_from_observation(obs, weights)
        traces.append(kernel.step(evidence, s.drift, s.prepare, s.commit))
    return traces
