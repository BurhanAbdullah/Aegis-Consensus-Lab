"""Deterministic reference equations for the tag4 Transactions rebuild."""
from __future__ import annotations
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


def influence(tau, risk, kappa):
    return project01(tau) * project01(1.0 - kappa * project01(risk))


def quorum_fraction(tau_bar, q0, alpha_q, q_min, q_max):
    return float(np.clip(q0 + alpha_q * (1.0 - tau_bar), q_min, q_max))


def safety_availability_interval(byzantine_weight):
    b = float(byzantine_weight)
    return ((1.0 + b) / 2.0, 1.0 - b)
