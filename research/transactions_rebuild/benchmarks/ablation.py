"""Component ablation study using identical deterministic two-validator attacks.

Reports both availability and the analytical conflicting-certificate boundary
q > (1+b)/2, so an ablation cannot look better merely by finalizing more.
"""
from __future__ import annotations
import csv, random
from pathlib import Path
from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

SEEDS = (11, 23, 37, 41, 59, 71, 83, 97, 101, 113)
VALIDATORS = ("A", "B", "C", "D")
ATTACK_SET = ("C", "D")
VARIANTS = {
    "full": Params(), "no_adaptive_quorum": Params(alpha_q=0.0),
    "no_predictive_attenuation": Params(kappa=0.0), "no_drift_risk": Params(risk_gain=0.0),
    "uniform_trust_aggregation": Params(),
}


def make_kernel(variant):
    weights = (0.25, 0.25, 0.25, 0.25) if variant == "uniform_trust_aggregation" else (0.40, 0.30, 0.15, 0.15)
    return AegisKernel([
        ValidatorState("A", [0.90] * 4), ValidatorState("B", [0.88] * 4),
        ValidatorState("C", [0.86] * 4), ValidatorState("D", [0.84] * 4)],
        weights=weights, params=VARIANTS[variant])


def run_case(variant, seed, evidence=0.65, drift=0.50, rounds=30):
    k = make_kernel(variant); rng = random.Random(seed)
    attack_final = attack_rounds = overall_final = unsafe_rounds = 0
    availability_margins = []; safety_margins = []
    for r in range(rounds):
        noise = rng.uniform(-0.01, 0.01)
        e = {v: max(0.0, min(1.0, 0.02 + noise)) for v in VALIDATORS}; d = {v: 0.0 for v in VALIDATORS}
        attacked = 5 <= r <= 18; commit = {v: True for v in VALIDATORS}
        if attacked:
            for v in ATTACK_SET: e[v], d[v], commit[v] = evidence, drift, False
            attack_rounds += 1
        trace = k.step(e, d, {v: True for v in VALIDATORS}, commit, height=1, view=r,
                        proposal_id=f"ablation-{variant}-{seed}")
        overall_final += int(trace.finalized)
        availability_margins.append(trace.commit_weight - trace.quorum_weight)
        influence = trace.influence
        total_inf = sum(influence.values())
        byz_weight = sum(influence[v] for v in ATTACK_SET) / total_inf if total_inf else 1.0
        safety_margin = trace.quorum_fraction - (1.0 + byz_weight) / 2.0
        safety_margins.append(safety_margin)
        if safety_margin <= 0.0: unsafe_rounds += 1
        if attacked: attack_final += int(trace.finalized)
    return {"variant": variant, "seed": seed, "attack_set": "+".join(ATTACK_SET),
            "evidence": evidence, "drift": drift,
            "attack_finalization_rate": attack_final / attack_rounds,
            "overall_finalization_rate": overall_final / rounds,
            "mean_availability_margin": sum(availability_margins) / len(availability_margins),
            "mean_safety_margin": sum(safety_margins) / len(safety_margins),
            "unsafe_certificate_boundary_fraction": unsafe_rounds / rounds}


def run_all(): return [run_case(v, s) for v in VARIANTS for s in SEEDS]


def write_csv(rows, path="experiments/ablation.csv"):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    rows = run_all(); write_csv(rows); print(f"wrote experiments/ablation.csv ({len(rows)} rows)")
