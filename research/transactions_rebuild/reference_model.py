"""Independent equation-first oracle for the tag4 Transactions rebuild.

This module is deliberately independent of AegisKernel. It implements the
state equations directly from FINAL_MODEL_SPEC_v2 and is used for
reference-versus-production equivalence tests.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Sequence, Tuple
import numpy as np


def project01(x):
    return np.clip(np.asarray(x, dtype=float), 0.0, 1.0)


def trust_step(tau, rho, ell, evidence):
    tau = np.asarray(tau, dtype=float)
    return project01(tau + rho * (1.0 - tau) - ell * evidence * tau)


def trust_equilibrium(rho, ell, evidence):
    denom = rho + ell * evidence
    if denom == 0:
        return 1.0
    return float(rho / denom)


def risk_step(risk, evidence, drift, a, c):
    return float(project01(a * risk + (1.0 - a) * evidence + c * drift))


def influence(tau, risk, kappa):
    return project01(tau) * project01(1.0 - kappa * project01(risk))


def quorum_fraction(tau_bar, q0, alpha_q, q_min, q_max):
    return float(np.clip(q0 + alpha_q * (1.0 - tau_bar), q_min, q_max))


def governance_state(tau, risk, q0, alpha_q, q_min, q_max, kappa, epsilon=1e-12):
    tau = np.asarray(tau, dtype=float)
    risk = np.asarray(risk, dtype=float)
    g = influence(tau, risk, kappa)
    active = g >= 1e-12
    total = float(np.sum(g[active]))
    tau_bar = float(np.sum(g[active] * tau[active]) / max(total, epsilon))
    q = quorum_fraction(tau_bar, q0, alpha_q, q_min, q_max)
    return g, tau_bar, q, total, q * total


def safety_availability_interval(byzantine_weight):
    b = float(byzantine_weight)
    return ((1.0 + b) / 2.0, 1.0 - b)


@dataclass(frozen=True)
class ReferenceState:
    trust: Tuple[Tuple[float, ...], ...]
    risk: Tuple[float, ...]
    round: int = 0


def reference_step(state: ReferenceState, evidence: Sequence[float], drift: Sequence[float], weights: Sequence[float], params):
    """Independent multi-validator state transition and governance oracle."""
    W = np.asarray(weights, dtype=float)
    E = np.asarray(evidence, dtype=float)
    D = np.asarray(drift, dtype=float)
    trust = np.asarray(state.trust, dtype=float)
    risk = np.asarray(state.risk, dtype=float)
    if trust.ndim != 2 or len(E) != len(trust) or len(D) != len(trust):
        raise ValueError("dimension mismatch")
    new_trust = np.vstack([trust_step(t, params.rho, params.ell, e) for t, e in zip(trust, E)])
    new_risk = np.asarray([risk_step(r, e, d, params.risk_memory, params.risk_gain) for r, e, d in zip(risk, E, D)])
    tau = np.asarray([float(np.dot(W, t)) for t in new_trust])
    g, tau_bar, q, total, threshold = governance_state(
        tau, new_risk, params.q0, params.alpha_q, params.q_min, params.q_max, params.kappa, params.epsilon
    )
    return {
        "state": ReferenceState(tuple(map(tuple, new_trust)), tuple(new_risk), state.round + 1),
        "trust": new_trust,
        "tau": tau,
        "risk": new_risk,
        "influence": g,
        "tau_bar": tau_bar,
        "q": q,
        "total_weight": total,
        "quorum_weight": threshold,
    }
