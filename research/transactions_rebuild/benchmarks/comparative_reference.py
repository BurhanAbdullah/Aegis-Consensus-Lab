"""Fair comparison against a fixed weighted-quorum reference.

This comparator intentionally uses the same seeded scenario traces as the
canonical benchmark. It is a fixed-quorum reference, not PBFT or HotStuff.
"""
from __future__ import annotations

from math import sqrt
from statistics import mean, stdev

from .canonical_scenarios import SCENARIOS, SEEDS, make_kernel, scenario_input

FIXED_Q = 0.67
Z95 = 1.96


def run_compare(rounds: int = 30) -> list[dict]:
    out: list[dict] = []
    for seed in SEEDS:
        for scenario in SCENARIOS:
            kernel = make_kernel()
            import random
            rng = random.Random(seed)
            for k in range(rounds):
                e, d, attacked = scenario_input(scenario, k, rng)
                commit = {v: True for v in "ABCD"}
                if scenario == "equivocation" and attacked:
                    commit["C"] = False
                trace = kernel.step(
                    e,
                    d,
                    {v: True for v in "ABCD"},
                    commit,
                    height=1,
                    view=k,
                    proposal_id=f"{scenario}-{seed}",
                )
                fixed_threshold = FIXED_Q * trace.total_weight
                fixed_finalized = trace.commit_weight >= fixed_threshold
                out.append({
                    "scenario": scenario,
                    "seed": seed,
                    "round": k,
                    "aegis_finalized": int(trace.finalized),
                    "fixed_quorum_finalized": int(fixed_finalized),
                    "aegis_margin": trace.commit_weight - trace.quorum_weight,
                    "fixed_margin": trace.commit_weight - fixed_threshold,
                })
    return out


def confidence_interval(values: list[float]) -> tuple[float, float, float]:
    n = len(values)
    m = mean(values)
    if n < 2:
        return m, m, m
    half = Z95 * stdev(values) / sqrt(n)
    return m, m - half, m + half


def summary(rows: list[dict]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for scenario in SCENARIOS:
        per_seed_aegis = []
        per_seed_fixed = []
        for seed in SEEDS:
            subset = [r for r in rows if r["scenario"] == scenario and r["seed"] == seed]
            per_seed_aegis.append(mean(r["aegis_finalized"] for r in subset))
            per_seed_fixed.append(mean(r["fixed_quorum_finalized"] for r in subset))
        am, alo, ahi = confidence_interval(per_seed_aegis)
        fm, flo, fhi = confidence_interval(per_seed_fixed)
        result[scenario] = {
            "aegis_mean": am,
            "aegis_ci95_low": alo,
            "aegis_ci95_high": ahi,
            "fixed_quorum_mean": fm,
            "fixed_quorum_ci95_low": flo,
            "fixed_quorum_ci95_high": fhi,
            "mean_difference": am - fm,
            "seed_count": len(SEEDS),
        }
    return result


if __name__ == "__main__":
    rows = run_compare()
    for scenario, values in summary(rows).items():
        print(scenario, values)
