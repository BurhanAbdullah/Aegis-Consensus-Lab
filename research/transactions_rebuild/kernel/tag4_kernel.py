"""Deterministic AEGIS tag4 reference kernel.

This kernel is intentionally scenario-driven: attack generation and detector
noise are supplied by the caller. The protocol state transition itself has no
internal randomness.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, List
import math


def clip01(x: float) -> float:
    return min(1.0, max(0.0, float(x)))


@dataclass(frozen=True)
class Params:
    rho: float = 0.10
    ell: float = 0.20
    risk_memory: float = 0.80
    risk_gain: float = 0.20
    kappa: float = 0.50
    q0: float = 0.60
    alpha_q: float = 0.20
    q_min: float = 0.50
    q_max: float = 0.99
    g_min: float = 1e-12
    epsilon: float = 1e-12


@dataclass
class ValidatorState:
    validator_id: str
    trust: List[float]
    risk: float = 0.0
    active: bool = True
    byzantine: bool = False

    def tau(self, weights: Iterable[float]) -> float:
        w = list(weights)
        if len(w) != len(self.trust) or not math.isclose(sum(w), 1.0, abs_tol=1e-12):
            raise ValueError("trust weights must match trust dimension and sum to one")
        return clip01(sum(a * b for a, b in zip(w, self.trust)))


@dataclass
class RoundTrace:
    round: int
    evidence: Dict[str, float]
    drift: Dict[str, float]
    trust: Dict[str, List[float]]
    tau: Dict[str, float]
    risk: Dict[str, float]
    influence: Dict[str, float]
    quorum_fraction: float
    total_weight: float
    quorum_weight: float
    prepare_weight: float = 0.0
    commit_weight: float = 0.0
    finalized: bool = False


class AegisKernel:
    """Deterministic protocol kernel matching FINAL_MODEL_SPEC_v2."""

    def __init__(self, validators: List[ValidatorState], weights=(0.40, 0.30, 0.15, 0.15), params=Params()):
        if not validators:
            raise ValueError("at least one validator is required")
        if not math.isclose(sum(weights), 1.0, abs_tol=1e-12):
            raise ValueError("trust aggregation weights must sum to one")
        self.validators = validators
        self.weights = tuple(float(x) for x in weights)
        self.p = params
        self.round = 0

    def step(self, evidence: Dict[str, float], drift: Dict[str, float], prepare: Dict[str, bool] | None = None, commit: Dict[str, bool] | None = None) -> RoundTrace:
        prepare = prepare or {}
        commit = commit or {}
        tau_before = {v.validator_id: v.tau(self.weights) for v in self.validators}

        for v in self.validators:
            e = clip01(evidence.get(v.validator_id, 0.0))
            d = clip01(drift.get(v.validator_id, 0.0))
            v.trust = [
                clip01(t + self.p.rho * (1.0 - t) - self.p.ell * e * t)
                for t in v.trust
            ]
            v.risk = clip01(
                self.p.risk_memory * v.risk
                + (1.0 - self.p.risk_memory) * e
                + self.p.risk_gain * d
            )

        tau = {v.validator_id: v.tau(self.weights) for v in self.validators}
        influence = {
            v.validator_id: tau[v.validator_id] * clip01(1.0 - self.p.kappa * v.risk)
            for v in self.validators
        }
        active = {v.validator_id: g >= self.p.g_min for v, g in [(v, influence[v.validator_id]) for v in self.validators]}
        total = sum(g for vid, g in influence.items() if active[vid])
        tau_bar = (
            sum(influence[vid] * tau[vid] for vid in influence if active[vid]) / max(total, self.p.epsilon)
        )
        q = min(self.p.q_max, max(self.p.q_min, self.p.q0 + self.p.alpha_q * (1.0 - tau_bar)))
        threshold = q * total

        prep_weight = sum(influence[v.validator_id] for v in self.validators if prepare.get(v.validator_id, False) and active[v.validator_id])
        commit_weight = sum(influence[v.validator_id] for v in self.validators if commit.get(v.validator_id, False) and active[v.validator_id])

        self.round += 1
        trace = RoundTrace(
            round=self.round,
            evidence={k: clip01(x) for k, x in evidence.items()},
            drift={k: clip01(x) for k, x in drift.items()},
            trust={v.validator_id: list(v.trust) for v in self.validators},
            tau=tau,
            risk={v.validator_id: v.risk for v in self.validators},
            influence=influence,
            quorum_fraction=q,
            total_weight=total,
            quorum_weight=threshold,
            prepare_weight=prep_weight,
            commit_weight=commit_weight,
            finalized=commit_weight >= threshold and total > self.p.epsilon,
        )
        return trace
