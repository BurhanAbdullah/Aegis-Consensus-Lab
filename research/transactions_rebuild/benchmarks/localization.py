"""Attack-localization sweep across validator identity and attack magnitude."""
from __future__ import annotations

import csv
import random
from pathlib import Path

from ..kernel.tag4_kernel import AegisKernel, ValidatorState

SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)
VALIDATORS = ("A", "B", "C", "D")
MAGNITUDES = (0.20, 0.40, 0.60, 0.80, 0.95)
DRIFTS = (0.00, 0.10, 0.30, 0.60)


def make_kernel() -> AegisKernel:
    return AegisKernel([
        ValidatorState("A", [0.90] * 4), ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4), ValidatorState("D", [0.84] * 4),
    ])


def run_case(location: str, magnitude: float, drift: float, seed: int, rounds: int = 30) -> dict:
    k = make_kernel(); rng = random.Random(seed)
    attack_final = 0; detected_like = 0; attack_rounds = 0
    min_tau = 1.0; min_influence = 1.0
    for r in range(rounds):
        noise = rng.uniform(-0.01, 0.01)
        e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in VALIDATORS}
        d = {v: 0.0 for v in VALIDATORS}
        attacked = 5 <= r <= 18
        if attacked:
            e[location], d[location] = magnitude, drift
            attack_rounds += 1
        trace = k.step(e, d, {v: True for v in VALIDATORS}, {v: True for v in VALIDATORS},
                        height=1, view=r, proposal_id=f"loc-{location}-{magnitude}-{drift}-{seed}")
        min_tau = min(min_tau, trace.tau[location])
        min_influence = min(min_influence, trace.influence[location])
        if attacked:
            attack_final += int(trace.finalized)
            detected_like += int(trace.risk[location] > 0.10)
    return {
        "location": location,
        "magnitude": magnitude,
        "drift": drift,
        "seed": seed,
        "attack_finalization_rate": attack_final / attack_rounds,
        "risk_activation_rate": detected_like / attack_rounds,
        "min_tau": min_tau,
        "min_influence": min_influence,
    }


def run_all() -> list[dict]:
    return [run_case(v, m, d, s) for v in VALIDATORS for m in MAGNITUDES for d in DRIFTS for s in SEEDS]


def write_csv(rows: list[dict], path: str | Path = "experiments/localization.csv") -> None:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    rows = run_all(); write_csv(rows); print(f"wrote experiments/localization.csv ({len(rows)} rows)")
