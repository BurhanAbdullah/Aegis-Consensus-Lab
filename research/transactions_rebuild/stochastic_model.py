"""Stochastic evidence model for the tag4 theory/experiment boundary."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


def clip01(x):
    return np.clip(np.asarray(x, dtype=float), 0.0, 1.0)


@dataclass(frozen=True)
class StochasticParams:
    rho: float = 0.10
    ell: float = 0.20
    risk_memory: float = 0.80
    risk_gain: float = 0.20
    evidence_noise_std: float = 0.0


def trust_step(tau, evidence, p: StochasticParams, rng=None):
    e = clip01(evidence)
    if p.evidence_noise_std:
        if rng is None:
            raise ValueError("rng is required when evidence noise is enabled")
        e = clip01(e + rng.normal(0.0, p.evidence_noise_std, size=np.shape(e)))
    tau = clip01(tau)
    return clip01(tau + p.rho * (1.0 - tau) - p.ell * e * tau), e


def risk_step(risk, evidence, drift, p: StochasticParams):
    return clip01(p.risk_memory * clip01(risk) + (1.0 - p.risk_memory) * clip01(evidence) + p.risk_gain * clip01(drift))


def monte_carlo_mean_trajectory(tau0, evidence, p: StochasticParams, steps, runs, seed):
    """Return mean trust trajectory and 95% Monte Carlo interval."""
    master = np.random.default_rng(seed)
    paths = np.empty((runs, steps + 1), dtype=float)
    paths[:, 0] = tau0
    for r in range(runs):
        rng = np.random.default_rng(int(master.integers(0, 2**63 - 1)))
        tau = float(tau0)
        for k in range(steps):
            tau, _ = trust_step(tau, evidence, p, rng)
            paths[r, k + 1] = float(tau)
    mean = paths.mean(axis=0)
    lo = np.quantile(paths, 0.025, axis=0)
    hi = np.quantile(paths, 0.975, axis=0)
    return mean, lo, hi
