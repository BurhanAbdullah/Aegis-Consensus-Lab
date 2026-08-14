#!/usr/bin/env python3
"""Independent mathematical audit of the recovery-ratio claim.

The audit distinguishes the two recurrences instead of treating Lambda=rho/loss
as a universal theorem. For the affine recurrence, any strictly positive
recovery term creates a positive fixed point; Lambda>=1 is therefore not the
correct criterion. For the multiplicative recurrence, Lambda>=1 is the exact
non-decay condition when loss>0.
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


def affine_prediction(w0, rho, loss):
    return bool(rho > 0.0 or (rho == 0.0 and loss == 0.0 and w0 > 0.0))


def gain_prediction(w0, rho, loss):
    return bool(w0 > 0.0 and rho >= loss)


def audit():
    cases = []
    for rho in np.linspace(0.0, 1.0, 21):
        for loss in np.linspace(0.01, 1.0, 20):
            lam = rho / loss
            for w0 in (0.1, 0.5, 0.9, 1.0):
                affine = simulate_affine(w0, rho, loss)
                gain = simulate_gain(w0, rho, loss)
                for name, x, predicted in (
                    ("affine", affine, affine_prediction(w0, rho, loss)),
                    ("gain", gain, gain_prediction(w0, rho, loss)),
                ):
                    observed = bool(x[-1] > 1e-6)
                    cases.append({
                        "recurrence": name,
                        "rho_recovery": float(rho),
                        "loss": float(loss),
                        "lambda": float(lam),
                        "w0": float(w0),
                        "predicted_positive_asymptotic_mass": predicted,
                        "observed_positive_terminal_mass": observed,
                        "counterexample": bool(predicted != observed),
                    })

    counters = [c for c in cases if c["counterexample"]]
    result = {
        "claim_tested": {
            "affine": "rho>0 (or rho=loss=0 with w0>0) is sufficient for positive asymptotic mass under the bounded parameter regime",
            "multiplicative": "Lambda=rho/loss>=1 is necessary and sufficient for positive asymptotic mass when loss>0 and w0>0",
        },
        "n_cases": len(cases),
        "n_counterexamples": len(counters),
        "counterexamples": counters[:50],
        "interpretation": (
            "Lambda=rho/loss is not a universal theorem for the affine trust recurrence. "
            "It is the exact non-decay criterion for the multiplicative recurrence, while the affine "
            "recurrence has equilibrium rho/(rho+loss) whenever rho>0."
        ),
    }
    (OUT / "theorem_audit.json").write_text(json.dumps(result, indent=2))
    if counters:
        raise AssertionError(f"Corrected recurrence theorem audit found {len(counters)} counterexamples")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    audit()
