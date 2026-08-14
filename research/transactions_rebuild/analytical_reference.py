"""Executable analytical reference for the canonical scalar model.

The functions here implement the closed-form stationary equilibrium and the
security/availability/stability inequalities stated in the canonical model.
They are deliberately separate from the protocol kernel so analytical
classification can be cross-validated against independent execution.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScalarParameters:
    rho: float = 0.10
    ell: float = 0.20
    q0: float = 0.60
    alpha_q: float = 0.20
    q_min: float = 0.50
    q_max: float = 0.99
    a: float = 0.80


def trust_equilibrium(rho: float, ell: float, evidence: float) -> float:
    denom = rho + ell * evidence
    if denom <= 0:
        raise ValueError("rho + ell*evidence must be positive")
    return rho / denom


def trust_multiplier(rho: float, ell: float, evidence: float) -> float:
    return 1.0 - rho - ell * evidence


def quorum_unclipped(q0: float, alpha_q: float, tau_star: float) -> float:
    return q0 + alpha_q * (1.0 - tau_star)


def quorum(q0: float, alpha_q: float, tau_star: float, q_min: float = 0.50, q_max: float = 0.99) -> float:
    return min(q_max, max(q_min, quorum_unclipped(q0, alpha_q, tau_star)))


def safety_boundary(byzantine_weight: float) -> float:
    return (1.0 + float(byzantine_weight)) / 2.0


def availability_boundary(byzantine_weight: float) -> float:
    return 1.0 - float(byzantine_weight)


def feasible(q: float, byzantine_weight: float) -> bool:
    return safety_boundary(byzantine_weight) < q <= availability_boundary(byzantine_weight)


def stable_scalar(rho: float, ell: float, evidence: float) -> bool:
    return abs(trust_multiplier(rho, ell, evidence)) < 1.0


def feasible_parameter_set(params: ScalarParameters, evidence: float, byzantine_weight: float) -> dict[str, float | bool]:
    tau = trust_equilibrium(params.rho, params.ell, evidence)
    q = quorum(params.q0, params.alpha_q, tau, params.q_min, params.q_max)
    return {
        "tau_star": tau,
        "q_star": q,
        "stable": stable_scalar(params.rho, params.ell, evidence),
        "safe_available": feasible(q, byzantine_weight),
        "safety_boundary": safety_boundary(byzantine_weight),
        "availability_boundary": availability_boundary(byzantine_weight),
    }
