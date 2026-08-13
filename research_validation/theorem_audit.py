#!/usr/bin/env python3
"""Independent mathematical audit of the proposed Recovery Elasticity Ratio.

This deliberately does not assume the proposed Lambda>=1 theorem. It tests
whether the claim follows from explicit recurrences and searches for
counterexamples. Results are written as machine-readable JSON.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

OUT = Path("research_validation/results")
OUT.mkdir(parents=True, exist_ok=True)


def simulate_affine(w0, rho, loss, steps=500):
    """Bounded recurrence: W' = clip(W + rho(1-W) - loss*W)."""
    w = float(w0)
    xs = [w]
    for _ in range(steps):
        w = np.clip(w + rho * (1.0 - w) - loss * w, 0.0, 1.0)
        xs.append(float(w))
    return np.asarray(xs)


def simulate_gain(w0, rho, loss, steps=500):
    """Multiplicative recurrence: W' = clip(W*(1+rho-loss))."""
    w = float(w0)
    xs = [w]
    for _ in range(steps):
        w = np.clip(w * (1.0 + rho - loss), 0.0, 1.0)
        xs.append(float(w))
    return np.asarray(xs)


def audit():
    # The reported Lambda expression is rho / loss.
    cases = []
    for rho in np.linspace(0.0, 1.0, 21):
        for loss in np.linspace(0.01, 1.0, 20):
            lam = rho / loss
            for w0 in (0.1, 0.5, 0.9, 1.0):
                a = simulate_affine(w0, rho, loss)
                g = simulate_gain(w0, rho, loss)
                for name, x in (("affine", a), ("gain", g)):
                    positive = bool(x[-1] > 1e-6)
                    predicted = bool(lam >= 1.0)
                    cases.append({
                        "recurrence": name,
                        "rho_recovery": float(rho),
                        "loss": float(loss),
                        "lambda": float(lam),
                        "w0": float(w0),
                        "predicted_nondecay": predicted,
                        "observed_positive_terminal_mass": positive,
                        "counterexample": bool(predicted != positive),
                    })

    counters = [c for c in cases if c["counterexample"]]
    result = {
        "claim_tested": "Lambda = rho_recovery / loss >= 1 is necessary and sufficient for positive asymptotic trust mass",
        "explicit_recurrences_tested": [
            "W' = clip(W + rho*(1-W) - loss*W, 0, 1)",
            "W' = clip(W*(1+rho-loss), 0, 1)",
        ],
        "n_cases": len(cases),
        "n_counterexamples": len(counters),
        "counterexamples": counters[:50],
        "interpretation": (
            "The Lambda condition cannot be accepted as a universal theorem from the ratio alone. "
            "Its validity is recurrence-specific and requires the exact implemented state equation and assumptions."
        ),
    }
    (OUT / "theorem_audit.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    audit()
