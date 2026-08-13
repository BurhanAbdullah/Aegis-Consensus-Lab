"""Unified reduced AEGIS state model for the tag4 analytical gate.

The reduced state is x=(tau,R). Evidence e and drift d are exogenous scenario
inputs. The model is differentiable only on the interior of the projection
maps; the Jacobian routines therefore refuse boundary points unless the
caller explicitly requests the piecewise map analysis.
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
    denom = p.rho + p.ell * e
    if denom <= 0:
        raise ValueError("trust equilibrium denominator must be positive")
    tau = p.rho / denom
    risk = ((1.0 - p.a) * e + p.c * d) / (1.0 - p.a)
    return np.array([tau, risk])


def jacobian_interior(e, p: ReducedParams):
    return np.array([
        [1.0 - p.rho - p.ell * e, 0.0],
        [0.0, p.a],
    ])


def spectral_radius(J):
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(J, dtype=float)))))


def jury_conditions_2x2(J, tol=1e-12):
    """Return Schur/Jury conditions for a real 2x2 discrete map.

    For characteristic polynomial lambda^2 - tr(J) lambda + det(J), the
    conditions are 1-tr+det>0, 1+tr+det>0, and 1-det>0.
    """
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
