"""End-to-end deterministic AEGIS experiment harness for tag4."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable

from ..detector_evidence import EvidenceWeights, build_evidence
from ..kernel.tag4_kernel import AegisKernel


@dataclass(frozen=True)
class ScenarioRound:
    detector: Dict[str, Dict[str, float]]
    thresholds: Dict[str, float]
    drift: Dict[str, float]
    prepare: Dict[str, bool]
    commit: Dict[str, bool]


def run_scenario(kernel: AegisKernel, rounds: Iterable[ScenarioRound], weights: EvidenceWeights | None = None):
    weights = weights or EvidenceWeights()
    traces = []
    for scenario in rounds:
        evidence = {
            vid: build_evidence(channels, scenario.thresholds, weights)
            for vid, channels in sorted(scenario.detector.items())
        }
        traces.append(kernel.step(evidence, scenario.drift, scenario.prepare, scenario.commit))
    return traces
