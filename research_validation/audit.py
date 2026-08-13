#!/usr/bin/env python3
"""Evidence-first audit for the public AEGIS research artifact.

The script intentionally does not manufacture a new theorem. It audits the
historical phase-space evidence and runs independent numerical sanity checks.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def audit_phase_space(root: Path, out: Path) -> dict:
    b = pd.read_csv(root / "archive/final_run/experiments/phase_space_baseline.csv")
    p = pd.read_csv(root / "archive/final_run/experiments/phase_space_predictive.csv")
    m = b.merge(p, on=["slash", "recover"], suffixes=("_baseline", "_predictive"))
    m["delta_successes"] = m.successes_predictive - m.successes_baseline
    m["predictive_better"] = m.delta_successes > 0
    m["baseline_better"] = m.delta_successes < 0
    m["tie"] = m.delta_successes == 0

    summary = {
        "cells": int(len(m)),
        "predictive_better_cells": int(m.predictive_better.sum()),
        "baseline_better_cells": int(m.baseline_better.sum()),
        "ties": int(m.tie.sum()),
        "mean_delta": float(m.delta_successes.mean()),
        "median_delta": float(m.delta_successes.median()),
        "min_delta": int(m.delta_successes.min()),
        "max_delta": int(m.delta_successes.max()),
    }
    m.to_csv(out / "phase_space_comparison.csv", index=False)
    return summary


def run_blind_recurrence(out: Path) -> dict:
    """Independent recurrence test for a generic bounded recovery/pruning model.

    This is deliberately a falsification harness, not a claim that the current
    Bash implementation has this exact recurrence. It tests whether a simple
    proposed gain-ratio intuition is sufficient under finite horizons and
    clipping. The output must not be used as proof of the AEGIS theorem.
    """
    rows = []
    for rho_recover in np.linspace(0.0, 1.0, 11):
        for prune in np.linspace(0.0, 1.0, 11):
            for initial in (0.25, 0.5, 0.75, 1.0):
                x = initial
                for _ in range(500):
                    x = float(np.clip(x * (1.0 - prune) + rho_recover * (1.0 - x), 0.0, 1.0))
                rows.append({
                    "rho_recover": rho_recover,
                    "prune": prune,
                    "initial": initial,
                    "asymptotic_x": x,
                    "nonzero": x > 1e-6,
                })
    df = pd.DataFrame(rows)
    df.to_csv(out / "independent_recurrence.csv", index=False)
    return {
        "configs": len(df),
        "nonzero_fraction": float(df.nonzero.mean()),
        "note": "Generic recurrence sanity check only; not a proof of the AEGIS model.",
    }


def solver_check(out: Path) -> dict:
    result = {"pandapower": "NOT_RUN", "pypsa": "NOT_RUN", "cases": []}
    try:
        import pandapower as pp
        import pandapower.networks as pn
        result["pandapower"] = pp.__version__
        for name, builder in [("case14", pn.case14), ("case30", pn.case30), ("case57", pn.case57), ("case118", pn.case118)]:
            net = builder()
            pp.runpp(net, algorithm="nr", calculate_voltage_angles=True, tolerance_mva=1e-8, max_iteration=50)
            result["cases"].append({
                "case": name,
                "converged": bool(net.converged),
                "max_vm_pu": float(net.res_bus.vm_pu.max()),
                "min_vm_pu": float(net.res_bus.vm_pu.min()),
                "max_line_loading_pct": float(net.res_line.loading_percent.max()) if len(net.res_line) else 0.0,
            })
    except Exception as exc:
        result["pandapower"] = f"ERROR: {exc}"

    try:
        import pypsa
        result["pypsa"] = getattr(pypsa, "__version__", "installed")
    except Exception as exc:
        result["pypsa"] = f"NOT_AVAILABLE: {exc}"

    (out / "solver_check.json").write_text(json.dumps(result, indent=2))
    return result


def make_figures(out: Path) -> None:
    import matplotlib.pyplot as plt

    df = pd.read_csv(out / "phase_space_comparison.csv")
    pivot = df.pivot(index="slash", columns="recover", values="delta_successes")
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(pivot.values, aspect="auto", origin="lower")
    ax.set_xticks(range(len(pivot.columns)), pivot.columns)
    ax.set_yticks(range(len(pivot.index)), pivot.index)
    ax.set_xlabel("Recovery parameter")
    ax.set_ylabel("Slash parameter")
    ax.set_title("Predictive minus baseline successes")
    fig.colorbar(im, ax=ax, label="Δ successes")
    fig.tight_layout()
    fig.savefig(out / "fig_phase_space_delta.pdf", bbox_inches="tight")
    fig.savefig(out / "fig_phase_space_delta.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    rec = pd.read_csv(out / "independent_recurrence.csv")
    grouped = rec.groupby("rho_recover", as_index=False)["asymptotic_x"].mean()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(grouped.rho_recover, grouped.asymptotic_x, marker="o")
    ax.set_xlabel("Recovery coefficient")
    ax.set_ylabel("Mean asymptotic state")
    ax.set_title("Independent recurrence sanity check")
    fig.tight_layout()
    fig.savefig(out / "fig_independent_recurrence.pdf", bbox_inches="tight")
    fig.savefig(out / "fig_independent_recurrence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="research_validation/results")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    report = {
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "phase_space": audit_phase_space(root, out),
        "independent_recurrence": run_blind_recurrence(out),
        "solver_check": solver_check(out),
    }
    (out / "audit_summary.json").write_text(json.dumps(report, indent=2))
    make_figures(out)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
