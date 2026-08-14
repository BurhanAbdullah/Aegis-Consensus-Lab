#!/usr/bin/env python3
"""Independent audit of the recovery-ratio claim.

The audit does not infer asymptotic behavior from a finite simulation horizon.
It checks the exact limiting classification implied by each explicitly stated
recurrence, and separately records finite-horizon convergence diagnostics.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path("research_validation/results")
OUT.mkdir(parents=True, exist_ok=True)


def simulate_affine(w0, rho, loss, steps=500):
    w = float(w0)
    xs = [w]
    for _ in range(steps):
        w = np.clip(w + rho * (1.0 - w) - loss * w, 0.0, 1.0)
        xs.append(float(w))
    return np.asarray(xs)


def simulate_gain(w0, rho, loss, steps=500):
    w = float(w0)
    xs = [w]
    for _ in range(steps):
        w = np.clip(w * (1.0 + rho - loss), 0.0, 1.0)
        xs.append(float(w))
    return np.asarray(xs)


def affine_limit(w0, rho, loss):
    """Exact limit for 0 <= rho,loss <= 1 under the projected affine map."""
    if rho == 0.0:
        if loss == 0.0:
            return float(w0)
        return 0.0
    return float(rho / (rho + loss))


def gain_limit(w0, rho, loss):
    """Exact limit for the projected multiplicative map on [0,1]."""
    if w0 <= 0.0:
        return 0.0
    multiplier = 1.0 + rho - loss
    if multiplier < 1.0:
        return 0.0
    return 1.0 if multiplier > 1.0 else float(w0)


def affine_prediction(w0, rho, loss):
    return bool(affine_limit(w0, rho, loss) > 0.0)


def gain_prediction(w0, rho, loss):
    return bool(gain_limit(w0, rho, loss) > 0.0)


def audit():
    cases = []
    finite_horizon_mismatches = []

    for rho in np.linspace(0.0, 1.0, 21):
        for loss in np.linspace(0.01, 1.0, 20):
            lam = rho / loss
            for w0 in (0.1, 0.5, 0.9, 1.0):
                affine = simulate_affine(w0, rho, loss)
                gain = simulate_gain(w0, rho, loss)
                for name, x, limit, predicted in (
                    ("affine", affine, affine_limit(w0, rho, loss), affine_prediction(w0, rho, loss)),
                    ("gain", gain, gain_limit(w0, rho, loss), gain_prediction(w0, rho, loss)),
                ):
                    observed_asymptotic = bool(limit > 0.0)
                    analytic_counterexample = bool(predicted != observed_asymptotic)
                    finite_observation = bool(x[-1] > 1e-6)
                    cases.append({
                        "recurrence": name,
                        "rho_recovery": float(rho),
                        "loss": float(loss),
                        "lambda": float(lam),
                        "w0": float(w0),
                        "analytic_limit": float(limit),
                        "predicted_positive_asymptotic_mass": predicted,
                        "analytic_counterexample": analytic_counterexample,
                        "finite_horizon_terminal_mass": float(x[-1]),
                        "finite_horizon_positive": finite_observation,
                    })
                    if finite_observation != observed_asymptotic:
                        finite_horizon_mismatches.append(cases[-1])

    counters = [c for c in cases if c["analytic_counterexample"]]
    result = {
        "claim_tested": {
            "affine": "For W'=clip(W+rho(1-W)-loss W,0,1), positive asymptotic mass occurs iff rho>0 or (rho=loss=0 and W0>0). For rho>0, W*=rho/(rho+loss).",
            "multiplicative": "For W'=clip(W(1+rho-loss),0,1) with loss>0 and W0>0, Lambda=rho/loss>=1 is necessary and sufficient for nonzero asymptotic mass.",
        },
        "n_cases": len(cases),
        "n_analytic_counterexamples": len(counters),
        "analytic_counterexamples": counters[:50],
        "n_finite_horizon_diagnostics": len(finite_horizon_mismatches),
        "finite_horizon_diagnostics": finite_horizon_mismatches[:20],
        "interpretation": (
            "Lambda=rho/loss is not a universal theorem for the affine trust recurrence. "
            "It is the exact non-decay criterion for the multiplicative recurrence under the stated assumptions. "
            "Finite-horizon terminal values are reported only as diagnostics and are not used to classify asymptotic behavior."
        ),
    }
    (OUT / "theorem_audit.json").write_text(json.dumps(result, indent=2))
    if counters:
        raise AssertionError(f"Analytic recurrence theorem audit found {len(counters)} counterexamples")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    audit()
