"""Pre-registered comparative stress grid for AEGIS versus fixed quorum.

The grid is not tuned to a single attack. It sweeps attack location, evidence
magnitude, drift magnitude, and seed while using identical traces for both
policies. Results are written as machine-readable CSV artifacts.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean

from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)
VALIDATORS = ("A", "B", "C", "D")
EVIDENCE_LEVELS = (0.20, 0.35, 0.50, 0.65, 0.80, 0.95)
DRIFT_LEVELS = (0.00, 0.10, 0.25, 0.50, 0.75)
ATTACK_LOCATIONS = VALIDATORS
FIXED_Q = 0.67
ROUNDS = 30
ATTACK_START = 5
ATTACK_END = 18


def make_kernel(params: Params | None = None) -> AegisKernel:
    return AegisKernel([
        ValidatorState("A", [0.90] * 4),
        ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4),
        ValidatorState("D", [0.84] * 4),
    ], params=params or Params())


def run_trace(location: str, evidence_level: float, drift_level: float, seed: int, params: Params | None = None):
    k = make_kernel(params)
    rng = random.Random(seed)
    aegis_attack_final = fixed_attack_final = 0
    aegis_all_final = fixed_all_final = 0
    margins_aegis = []
    margins_fixed = []
    attack_rounds = 0
    for r in range(ROUNDS):
        noise = rng.uniform(-0.01, 0.01)
        e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in VALIDATORS}
        d = {v: 0.0 for v in VALIDATORS}
        attacked = ATTACK_START <= r <= ATTACK_END
        if attacked:
            e[location] = evidence_level
            d[location] = drift_level
            attack_rounds += 1
        commit = {v: True for v in VALIDATORS}
        trace = k.step(e, d, {v: True for v in VALIDATORS}, commit,
                        height=1, view=r, proposal_id=f"grid-{location}-{seed}-{evidence_level}-{drift_level}")
        fixed_threshold = FIXED_Q * trace.total_weight
        fixed_finalized = trace.commit_weight >= fixed_threshold
        aegis_all_final += int(trace.finalized)
        fixed_all_final += int(fixed_finalized)
        margins_aegis.append(trace.commit_weight - trace.quorum_weight)
        margins_fixed.append(trace.commit_weight - fixed_threshold)
        if attacked:
            aegis_attack_final += int(trace.finalized)
            fixed_attack_final += int(fixed_finalized)
    return {
        "location": location,
        "evidence": evidence_level,
        "drift": drift_level,
        "seed": seed,
        "aegis_attack_finalization_rate": aegis_attack_final / attack_rounds,
        "fixed_attack_finalization_rate": fixed_attack_final / attack_rounds,
        "aegis_overall_finalization_rate": aegis_all_final / ROUNDS,
        "fixed_overall_finalization_rate": fixed_all_final / ROUNDS,
        "attack_finalization_difference": (aegis_attack_final - fixed_attack_final) / attack_rounds,
        "mean_aegis_margin": mean(margins_aegis),
        "mean_fixed_margin": mean(margins_fixed),
    }


def run_grid() -> list[dict]:
    rows = []
    for location in ATTACK_LOCATIONS:
        for e in EVIDENCE_LEVELS:
            for d in DRIFT_LEVELS:
                for seed in SEEDS:
                    rows.append(run_trace(location, e, d, seed))
    return rows


def write_csv(rows: list[dict], path: str | Path = "experiments/comparative_grid.csv") -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    rows = run_grid()
    write_csv(rows)
    print(f"wrote experiments/comparative_grid.csv ({len(rows)} rows)")
