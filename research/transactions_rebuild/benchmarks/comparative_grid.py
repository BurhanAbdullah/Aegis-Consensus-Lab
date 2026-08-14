"""Pre-registered comparative stress grid for AEGIS and two static quorum policies."""
from __future__ import annotations
import csv, random
from itertools import combinations
from pathlib import Path
from statistics import mean
from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)
VALIDATORS = ("A", "B", "C", "D")
ATTACK_SETS = tuple(c for r in (1, 2, 3) for c in combinations(VALIDATORS, r))
EVIDENCE_LEVELS = (0.20, 0.35, 0.50, 0.65, 0.80, 0.95)
DRIFT_LEVELS = (0.00, 0.10, 0.25, 0.50, 0.75)
FIXED_Q67, FIXED_Q75 = 0.67, 0.75
ROUNDS, ATTACK_START, ATTACK_END = 30, 5, 18


def make_kernel(params=None):
    return AegisKernel([
        ValidatorState("A", [0.90] * 4), ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4), ValidatorState("D", [0.84] * 4)], params=params or Params())


def run_trace(attack_set, evidence_level, drift_level, seed, params=None):
    k = make_kernel(params); rng = random.Random(seed)
    aegis_attack = q67_attack = q75_attack = 0; attack_rounds = 0; ma = []; m67 = []; m75 = []
    for r in range(ROUNDS):
        noise = rng.uniform(-0.01, 0.01)
        e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in VALIDATORS}; d = {v: 0.0 for v in VALIDATORS}; commit = {v: True for v in VALIDATORS}
        attacked = ATTACK_START <= r <= ATTACK_END
        if attacked:
            for v in attack_set: e[v], d[v], commit[v] = evidence_level, drift_level, False
            attack_rounds += 1
        trace = k.step(e, d, {v: True for v in VALIDATORS}, commit, height=1, view=r,
                        proposal_id=f"grid-{''.join(attack_set)}-{seed}-{evidence_level}-{drift_level}")
        t67, t75 = FIXED_Q67 * trace.total_weight, FIXED_Q75 * trace.total_weight
        q67, q75 = trace.commit_weight >= t67, trace.commit_weight >= t75
        ma.append(trace.commit_weight - trace.quorum_weight); m67.append(trace.commit_weight - t67); m75.append(trace.commit_weight - t75)
        if attacked:
            aegis_attack += int(trace.finalized); q67_attack += int(q67); q75_attack += int(q75)
    return {"attack_set": "+".join(attack_set), "attack_count": len(attack_set), "evidence": evidence_level, "drift": drift_level, "seed": seed,
            "aegis_attack_finalization_rate": aegis_attack / attack_rounds,
            "fixed_q67_attack_finalization_rate": q67_attack / attack_rounds,
            "fixed_q75_attack_finalization_rate": q75_attack / attack_rounds,
            "aegis_minus_q67_difference": (aegis_attack - q67_attack) / attack_rounds,
            "aegis_minus_q75_difference": (aegis_attack - q75_attack) / attack_rounds,
            "mean_aegis_margin": mean(ma), "mean_fixed_q67_margin": mean(m67), "mean_fixed_q75_margin": mean(m75)}


def run_grid():
    return [run_trace(a, e, d, s) for a in ATTACK_SETS for e in EVIDENCE_LEVELS for d in DRIFT_LEVELS for s in SEEDS]


def write_csv(rows, path="experiments/comparative_grid.csv"):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    rows = run_grid(); write_csv(rows); print(f"wrote experiments/comparative_grid.csv ({len(rows)} rows)")
