"""Canonical reduced and full interior AEGIS state model.

The analytical state for one validator is x=(T_1,...,T_m,R). Evidence E
and observable drift D are exogenous inputs to this deterministic map. The
projection is inactive on the interior; boundary points are not silently
included in the differentiable theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ReducedParams:
    rho: float = 0.10
    ell: float = 0.20
    a: float = 0.80
    c: float = 0.20
    kappa: float = 0.50
    q0: float = 0.60
    alpha_q: float = 0.20
    q_min: float = 0.50
    q_max: float = 0.99


def interior_step(x, e, d, p: ReducedParams):
    tau, risk = np.asarray(x, dtype=float)
    return np.array([
        tau + p.rho * (1.0 - tau) - p.ell * e * tau,
        p.a * risk + (1.0 - p.a) * e + p.c * d,
    ])


def equilibrium(e, d, p: ReducedParams):
    if not (0.0 <= e <= 1.0 and 0.0 <= d <= 1.0):
        raise ValueError("e and d must lie in [0,1]")
    if not (0.0 <= p.a < 1.0):
        raise ValueError("a must lie in [0,1)")
    denom = p.rho + p.ell * e
    if denom <= 0:
        raise ValueError("trust equilibrium denominator must be positive")
    tau = p.rho / denom
    risk = ((1.0 - p.a) * e + p.c * d) / (1.0 - p.a)
    return np.array([tau, risk])


def risk_containment(e, d, p: ReducedParams) -> bool:
    """Check the condition that keeps the unclipped risk equilibrium in [0,1]."""
    return 0.0 <= e <= 1.0 and 0.0 <= d <= 1.0 and (1.0 - p.a) * e + p.c * d <= (1.0 - p.a) + 1e-12


def jacobian_interior(e, p: ReducedParams):
    return np.array([
        [1.0 - p.rho - p.ell * e, 0.0],
        [0.0, p.a],
    ])


def full_interior_step(x, e, d, p: ReducedParams):
    """One interior step for x=(T_1,...,T_m,R)."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("x must be a one-dimensional vector with at least two states")
    trust = x[:-1]
    risk = x[-1]
    trust_next = trust + p.rho * (1.0 - trust) - p.ell * float(e) * trust
    risk_next = p.a * risk + (1.0 - p.a) * float(e) + p.c * float(d)
    return np.concatenate([trust_next, [risk_next]])


def full_interior_jacobian(e, p: ReducedParams, dimension: int = 4) -> np.ndarray:
    """Exact Jacobian of the canonical m-trust-dimension plus risk map.

    E and D are treated as exogenous observables. Therefore there are no
    hidden detector derivatives in this Jacobian. The result is
    diag(beta I_m, a), beta=1-rho-ell E.
    """
    if dimension < 1:
        raise ValueError("dimension must be >=1")
    beta = 1.0 - p.rho - p.ell * float(e)
    J = np.zeros((dimension + 1, dimension + 1), dtype=float)
    J[:dimension, :dimension] = beta * np.eye(dimension)
    J[-1, -1] = p.a
    return J


def full_equilibrium(e, d, p: ReducedParams, dimension: int = 4):
    """Exact interior equilibrium for the full m+1 state when risk is contained."""
    if not risk_containment(e, d, p):
        raise ValueError("risk containment condition fails; interior equilibrium is not guaranteed in [0,1]")
    x2 = equilibrium(e, d, p)
    return np.concatenate([np.full(dimension, x2[0]), [x2[1]]])


def spectral_radius(J):
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(J, dtype=float)))))


def jury_conditions_2x2(J, tol=1e-12):
    """Return Schur/Jury conditions for a real 2x2 discrete map."""
    J = np.asarray(J, dtype=float)
    if J.shape != (2, 2):
        raise ValueError("J must be 2x2")
    tr = float(np.trace(J)); det = float(np.linalg.det(J))
    return {
        "1-tr+det": 1.0 - tr + det,
        "1+tr+det": 1.0 + tr + det,
        "1-det": 1.0 - det,
        "stable": (1.0 - tr + det > tol and 1.0 + tr + det > tol and 1.0 - det > tol),
    }


def governance_quorum(tau, risk, p: ReducedParams):
    influence = float(np.clip(tau * (1.0 - p.kappa * risk), 0.0, 1.0))
    if influence <= 0.0:
        return 0.0, 0.0, influence
    q = float(np.clip(p.q0 + p.alpha_q * (1.0 - tau), p.q_min, p.q_max))
    return q, q * influence, influence
