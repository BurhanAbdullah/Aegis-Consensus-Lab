"""Reference implementation of the Transactions-rebuild governance model.

This module is deliberately isolated from the legacy shell consensus engine.
It implements the candidate equations in THEORY_V1.md so that mathematics,
unit tests, and later experiments can be aligned before integration.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


EPS = 1e-12


def clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def weighted_trust(trust: Sequence[float], weights: Sequence[float]) -> float:
    if len(trust) != len(weights) or not trust:
        raise ValueError("trust and weights must have equal non-zero length")
    if any(w < 0 for w in weights):
        raise ValueError("trust weights must be non-negative")
    total = sum(weights)
    if total <= EPS:
        raise ValueError("trust weights must have positive sum")
    return clip01(sum(t * w for t, w in zip(trust, weights)) / total)


def trust_step(t: float, rho: float, loss: float) -> float:
    """t' = clip(t + rho(1-t) - loss*t, 0, 1)."""
    if rho < 0 or loss < 0:
        raise ValueError("rho and loss must be non-negative")
    return clip01(t + rho * (1.0 - t) - loss * t)


def trust_equilibrium(rho: float, loss: float) -> float:
    """Fixed point of the unclipped affine trust recurrence."""
    if rho < 0 or loss < 0:
        raise ValueError("rho and loss must be non-negative")
    if rho + loss <= EPS:
        return 0.0
    return clip01(rho / (rho + loss))


def risk_score(
    aggregate_trust: float,
    volatility: float,
    observation: float,
    degradation: float,
    alpha: float,
    beta: float,
    gamma: float,
    delta: float,
) -> float:
    """Risk score separating low trust from instability/evidence terms."""
    if min(alpha, beta, gamma, delta) < 0:
        raise ValueError("risk coefficients must be non-negative")
    raw = (
        alpha * (1.0 - clip01(aggregate_trust))
        + beta * clip01(volatility)
        + gamma * clip01(observation)
        + delta * clip01(degradation)
    )
    return clip01(raw)


def influence_multiplier(risk: float, threshold: float, kappa: float) -> float:
    """Continuous non-increasing PRC multiplier in [0,1]."""
    if not 0.0 <= threshold <= 1.0 or kappa < 0:
        raise ValueError("invalid PRC parameters")
    risk = clip01(risk)
    if risk <= threshold:
        return 1.0
    span = max(1.0 - threshold, EPS)
    return clip01(1.0 - kappa * (risk - threshold) / span)


def governance_weight(aggregate_trust: float, risk: float, threshold: float, kappa: float) -> float:
    return clip01(aggregate_trust) * influence_multiplier(risk, threshold, kappa)


def adaptive_quorum(
    aggregate_trust: float,
    q0: float,
    alpha_q: float,
    q_min: float,
    q_max: float,
) -> float:
    if not 0.0 <= q_min <= q_max <= 1.0:
        raise ValueError("quorum bounds must satisfy 0 <= q_min <= q_max <= 1")
    if alpha_q < 0:
        raise ValueError("alpha_q must be non-negative")
    q = q0 + alpha_q * (1.0 - clip01(aggregate_trust))
    return max(q_min, min(q_max, q))


@dataclass(frozen=True)
class GovernanceSnapshot:
    trust: float
    risk: float
    influence: float
    quorum: float


def snapshot(
    aggregate_trust: float,
    risk: float,
    *,
    threshold: float,
    kappa: float,
    q0: float,
    alpha_q: float,
    q_min: float,
    q_max: float,
) -> GovernanceSnapshot:
    return GovernanceSnapshot(
        trust=clip01(aggregate_trust),
        risk=clip01(risk),
        influence=governance_weight(aggregate_trust, risk, threshold, kappa),
        quorum=adaptive_quorum(aggregate_trust, q0, alpha_q, q_min, q_max),
    )
