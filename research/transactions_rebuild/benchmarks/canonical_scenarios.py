"""Seeded, reproducible scenario benchmark for the canonical tag4 kernel.

Each seed controls only the explicitly documented detector-noise perturbation.
The attack schedule itself is fixed by scenario definition. Repeating the same
seed reproduces the exact trace; different seeds provide independent replicates.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Dict, Iterable

from ..kernel.tag4_kernel import AegisKernel, ValidatorState

SCENARIOS = ("clean", "burst", "slow_drift", "stealth", "equivocation", "mixed")
SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)


def make_kernel() -> AegisKernel:
    return AegisKernel([
        ValidatorState("A", [0.90] * 4),
        ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4),
        ValidatorState("D", [0.84] * 4),
    ])


def scenario_input(name: str, k: int, rng: random.Random) -> tuple[Dict[str, float], Dict[str, float], bool]:
    noise = rng.uniform(-0.01, 0.01)
    e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in "ABCD"}
    d = {v: 0.0 for v in "ABCD"}
    attacked = False

    if name == "burst" and 5 <= k <= 7:
        e["C"], d["C"], attacked = 0.90, 0.80, True
    elif name == "slow_drift" and 5 <= k <= 18:
        e["C"], d["C"], attacked = min(0.75, 0.05 + 0.015 * (k - 5)), 0.02, True
    elif name == "stealth" and 5 <= k <= 18:
        e["C"], d["C"], attacked = min(0.30, 0.08 + 0.004 * (k - 5)), 0.03, True
    elif name == "equivocation" and 5 <= k <= 18:
        e["C"], attacked = 0.05, True
    elif name == "mixed" and 5 <= k <= 18:
        e["C"], e["D"] = min(0.85, 0.10 + 0.02 * (k - 5)), 0.55 if 8 <= k <= 12 else 0.10
        d["C"], d["D"], attacked = 0.10, 0.60 if 8 <= k <= 12 else 0.02, True
    return e, d, attacked


def run_case(name: str, seed: int, rounds: int = 30) -> list[dict]:
    kernel = make_kernel()
    rng = random.Random(seed)
    rows: list[dict] = []
    detected_at = None
    recovered_at = None
    attack_end = 18 if name != "burst" else 7

    for k in range(rounds):
        e, d, attacked = scenario_input(name, k, rng)
        prepare = {v: True for v in "ABCD"}
        commit = {v: True for v in "ABCD"}
        if name == "equivocation" and attacked:
            commit["C"] = False
        trace = kernel.step(e, d, prepare, commit, height=1, view=k, proposal_id=f"{name}-{seed}")
        if detected_at is None and attacked and max(e.values()) >= 0.30:
            detected_at = k
        if detected_at is not None and k > attack_end and max(e.values()) < 0.30 and recovered_at is None:
            recovered_at = k
        rows.append({
            "scenario": name,
            "seed": seed,
            "round": k,
            "finalized": int(trace.finalized),
            "quorum_margin": trace.commit_weight - trace.quorum_weight,
            "detected": int(detected_at is not None and k >= detected_at),
            "recovered": int(recovered_at is not None and k >= recovered_at),
            "attack_active": int(attacked),
            "max_evidence": max(e.values()),
            "max_drift": max(d.values()),
            "quorum_fraction": trace.quorum_fraction,
        })
    return rows


def run_all(seeds: Iterable[int] = SEEDS) -> list[dict]:
    return [row for seed in seeds for scenario in SCENARIOS for row in run_case(scenario, seed)]


def write_csv(path: str | Path, rows: list[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    target = Path("experiments/canonical_scenarios.csv")
    write_csv(target, run_all())
    print(f"wrote {target}")
