"""Component ablation study using identical deterministic attack traces."""
from __future__ import annotations

import csv
import random
from pathlib import Path

from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)
VALIDATORS = ("A", "B", "C", "D")
VARIANTS = {
    "full": Params(),
    "no_adaptive_quorum": Params(alpha_q=0.0),
    "no_predictive_attenuation": Params(kappa=0.0),
    "no_drift_risk": Params(risk_gain=0.0),
    "uniform_trust_aggregation": Params(),
}


def make_kernel(variant: str) -> AegisKernel:
    weights = (0.25, 0.25, 0.25, 0.25) if variant == "uniform_trust_aggregation" else (0.40, 0.30, 0.15, 0.15)
    return AegisKernel([
        ValidatorState("A", [0.90] * 4), ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4), ValidatorState("D", [0.84] * 4),
    ], weights=weights, params=VARIANTS[variant])


def run_case(variant: str, seed: int, location: str = "C", evidence: float = 0.65, drift: float = 0.50, rounds: int = 30) -> dict:
    k = make_kernel(variant)
    rng = random.Random(seed)
    attack_final = 0
    attack_rounds = 0
    overall_final = 0
    margins = []
    for r in range(rounds):
        noise = rng.uniform(-0.01, 0.01)
        e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in VALIDATORS}
        d = {v: 0.0 for v in VALIDATORS}
        attacked = 5 <= r <= 18
        if attacked:
            e[location], d[location] = evidence, drift
            attack_rounds += 1
        trace = k.step(e, d, {v: True for v in VALIDATORS}, {v: True for v in VALIDATORS},
                        height=1, view=r, proposal_id=f"ablation-{variant}-{seed}")
        overall_final += int(trace.finalized)
        margins.append(trace.quorum_margin)
        if attacked:
            attack_final += int(trace.finalized)
    return {
        "variant": variant,
        "seed": seed,
        "attack_location": location,
        "evidence": evidence,
        "drift": drift,
        "attack_finalization_rate": attack_final / attack_rounds,
        "overall_finalization_rate": overall_final / rounds,
        "mean_quorum_margin": sum(margins) / len(margins),
    }


def run_all() -> list[dict]:
    return [run_case(v, s) for v in VARIANTS for s in SEEDS]


def write_csv(rows: list[dict], path: str | Path = "experiments/ablation.csv") -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    rows = run_all(); write_csv(rows); print(f"wrote experiments/ablation.csv ({len(rows)} rows)")
