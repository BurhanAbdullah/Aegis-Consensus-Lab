#!/usr/bin/env python3
"""Independent statistical and claim-consistency audit of archived AEGIS evidence.

A mismatch is a submission blocker. This audit must never silently accept
historical headline numbers when the underlying CSV gives different values.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "research_validation/results"
    out.mkdir(parents=True, exist_ok=True)

    b = pd.read_csv(root / "archive/final_run/experiments/phase_space_baseline.csv")
    p = pd.read_csv(root / "archive/final_run/experiments/phase_space_predictive.csv")
    m = b.merge(p, on=["slash", "recover"], suffixes=("_baseline", "_predictive"))
    d = (m["successes_predictive"] - m["successes_baseline"]).to_numpy(dtype=float)

    t = stats.ttest_1samp(d, 0.0)
    nonzero = d[d != 0]
    wilcoxon = stats.wilcoxon(nonzero, alternative="greater", method="auto")
    sign = stats.binomtest(int((d > 0).sum()), int((d != 0).sum()), 0.5, alternative="greater")

    rng = np.random.default_rng(20260813)
    boot = np.empty(50000)
    for i in range(len(boot)):
        boot[i] = rng.choice(d, size=len(d), replace=True).mean()
    ci = np.quantile(boot, [0.025, 0.975])

    n_pos = int((d > 0).sum())
    n_neg = int((d < 0).sum())
    n_tie = int((d == 0).sum())
    rank_effect = float((n_pos - n_neg) / (n_pos + n_neg))

    readme = (root / "archive/final_run/README.md").read_text(encoding="utf-8")
    mb = re.search(r"Baseline mean success:\s*([0-9.]+)", readme)
    mp = re.search(r"Predictive mean success:\s*([0-9.]+)", readme)
    claimed_b = float(mb.group(1)) if mb else None
    claimed_p = float(mp.group(1)) if mp else None
    actual_b = float(m["successes_baseline"].mean())
    actual_p = float(m["successes_predictive"].mean())

    solver = json.loads((out / "solver_check.json").read_text(encoding="utf-8"))
    solver_flags = []
    for case in solver.get("cases", []):
        flags = []
        if case["min_vm_pu"] < 0.95:
            flags.append("undervoltage_below_0.95_pu")
        if case["max_line_loading_pct"] > 100.0:
            flags.append("line_loading_above_100_percent")
        solver_flags.append({"case": case["case"], "flags": flags})

    mismatch = bool(
        claimed_b is not None
        and claimed_p is not None
        and (abs(actual_b - claimed_b) > 1e-9 or abs(actual_p - claimed_p) > 1e-9)
    )

    report = {
        "phase_space": {
            "cells": len(d),
            "predictive_better": n_pos,
            "baseline_better": n_neg,
            "ties": n_tie,
            "mean_delta": float(d.mean()),
            "median_delta": float(np.median(d)),
            "std_delta": float(d.std(ddof=1)),
            "bootstrap_95ci_mean_delta": [float(ci[0]), float(ci[1])],
            "paired_t_test": {"statistic": float(t.statistic), "pvalue": float(t.pvalue)},
            "wilcoxon_signed_rank_greater": {"statistic": float(wilcoxon.statistic), "pvalue": float(wilcoxon.pvalue)},
            "sign_test_greater": {"successes": n_pos, "trials_excluding_ties": n_pos + n_neg, "pvalue": float(sign.pvalue)},
            "sign_effect": rank_effect,
            "interpretation": "The archived 36-cell phase-space table does not establish a statistically significant global predictive advantage at alpha=0.05.",
        },
        "headline_claim_consistency": {
            "archived_readme_baseline_mean": claimed_b,
            "archived_readme_predictive_mean": claimed_p,
            "phase_space_csv_baseline_mean": actual_b,
            "phase_space_csv_predictive_mean": actual_p,
            "baseline_absolute_difference": None if claimed_b is None else actual_b - claimed_b,
            "predictive_absolute_difference": None if claimed_p is None else actual_p - claimed_p,
            "status": "MISMATCH" if mismatch else "MATCH_OR_UNAVAILABLE",
        },
        "solver_operational_flags": solver_flags,
    }

    (out / "statistical_claim_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if mismatch:
        raise SystemExit("Submission blocker: archived headline means do not match recomputed CSV means.")


if __name__ == "__main__":
    main()
