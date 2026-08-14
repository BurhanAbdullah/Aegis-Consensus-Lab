"""Fair comparison against a fixed weighted-quorum reference.

This is deliberately named a *fixed-quorum reference*, not PBFT or HotStuff.
It uses the same validator states, evidence traces, seeds, and rounds as the
canonical AEGIS scenario benchmark. External protocol claims require separate
implementations and are not inferred from this comparator.
"""
from __future__ import annotations

from statistics import mean
from .canonical_scenarios import SCENARIOS, SEEDS, make_kernel, scenario_input

FIXED_Q = 0.67


def run_compare(rounds: int = 30) -> list[dict]:
    out = []
    for seed in SEEDS:
        for scenario in SCENARIOS:
            kernel = make_kernel()
            for k in range(rounds):
                e, d = scenario_input(scenario, k, seed)
                trace = kernel.step(
                    e, d,
                    {v: True for v in "ABCD"},
                    {v: True for v in "ABCD"},
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


def summary(rows: list[dict]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for scenario in SCENARIOS:
        subset = [r for r in rows if r["scenario"] == scenario]
        result[scenario] = {
            "aegis_finalization_rate": mean(r["aegis_finalized"] for r in subset),
            "fixed_quorum_finalization_rate": mean(r["fixed_quorum_finalized"] for r in subset),
            "mean_margin_difference": mean(r["aegis_margin"] - r["fixed_margin"] for r in subset),
        }
    return result


if __name__ == "__main__":
    rows = run_compare()
    for scenario, values in summary(rows).items():
        print(scenario, values)
