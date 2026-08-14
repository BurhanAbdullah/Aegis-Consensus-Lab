"""Deterministic scenario benchmark for the canonical tag4 kernel.

This benchmark intentionally contains no hidden randomness. Each seed is used
only to derive a deterministic phase offset, so results are replayable without
an RNG dependency. It reports safety/finalization, detection, recovery and
quorum-margin metrics for six explicit attack families.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable

from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

SCENARIOS = (
    "clean",
    "burst",
    "slow_drift",
    "stealth",
    "equivocation",
    "mixed",
)
SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)


def make_kernel() -> AegisKernel:
    return AegisKernel([
        ValidatorState("A", [0.90, 0.90, 0.90, 0.90]),
        ValidatorState("B", [0.88, 0.88, 0.88, 0.88]),
        ValidatorState("C", [0.86, 0.86, 0.86, 0.86]),
        ValidatorState("D", [0.84, 0.84, 0.84, 0.84]),
    ])


def scenario_input(name: str, k: int, seed: int) -> tuple[Dict[str, float], Dict[str, float]]:
    # Deterministic phase offset; this is not stochastic attack generation.
    phase = (seed % 7) / 100.0
    e = {v: 0.02 + phase for v in "ABCD"}
    d = {v: 0.00 for v in "ABCD"}

    if name == "burst" and 5 <= k <= 7:
        e["C"] = 0.90
        d["C"] = 0.80
    elif name == "slow_drift":
        e["C"] = min(0.75, 0.05 + 0.015 * k)
        d["C"] = 0.02
    elif name == "stealth":
        e["C"] = min(0.30, 0.08 + 0.004 * k)
        d["C"] = 0.03
    elif name == "equivocation":
        # Detector evidence remains benign; the malicious behavior is represented
        # by conflicting commit votes below, not by changing the state equations.
        e["C"] = 0.05
    elif name == "mixed":
        e["C"] = min(0.85, 0.10 + 0.02 * k)
        e["D"] = 0.55 if 8 <= k <= 12 else 0.10
        d["C"] = 0.10
        d["D"] = 0.60 if 8 <= k <= 12 else 0.02
    return e, d


def run_case(name: str, seed: int, rounds: int = 30) -> list[dict]:
    kernel = make_kernel()
    rows: list[dict] = []
    detected_at = None
    recovered_at = None
    attack_end = 12 if name in {"burst", "mixed"} else 29

    for k in range(rounds):
        e, d = scenario_input(name, k, seed)
        # A clean, deterministic honest vote pattern. Equivocation is represented
        # by omitting C from the commit certificate; no unsafe certificate should
        # be accepted because certificate validity is context- and weight-bound.
        prepare = {v: True for v in "ABCD"}
        commit = {v: True for v in "ABCD"}
        if name == "equivocation":
            commit["C"] = False
        trace = kernel.step(e, d, prepare, commit, height=1, view=k, proposal_id=f"{name}-{seed}")
        if detected_at is None and max(e.values()) >= 0.30:
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
            "max_evidence": max(e.values()),
            "max_drift": max(d.values()),
            "quorum_fraction": trace.quorum_fraction,
        })
    return rows


def run_all(seeds: Iterable[int] = SEEDS) -> list[dict]:
    out: list[dict] = []
    for seed in seeds:
        for scenario in SCENARIOS:
            out.extend(run_case(scenario, seed))
    return out


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
