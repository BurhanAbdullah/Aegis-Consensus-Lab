#!/usr/bin/env python3
"""Evidence-first validation for the public AEGIS research artifact.

This audit deliberately separates three things:
1. what the archived data actually show;
2. what independent numerical solvers can validate; and
3. what the proposed mathematical theorem would require from the implementation.

It never silently edits or reinterprets the frozen archive/final_run evidence.
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
from scipy import stats


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def phase_space_audit(root: Path, out: Path) -> dict:
    b = pd.read_csv(root / "archive/final_run/experiments/phase_space_baseline.csv")
    p = pd.read_csv(root / "archive/final_run/experiments/phase_space_predictive.csv")
    keys = ["slash", "recover"]
    m = b.merge(p, on=keys, suffixes=("_baseline", "_predictive"))
    if len(m) != 36 or m[keys].duplicated().any():
        raise RuntimeError("Expected exactly 36 unique phase-space cells.")

    m["delta_successes"] = m.successes_predictive - m.successes_baseline
    d = m.delta_successes.to_numpy(dtype=float)
    nonzero = d[d != 0]

    t = stats.ttest_rel(m.successes_predictive, m.successes_baseline)
    w = stats.wilcoxon(d, zero_method="wilcox", alternative="two-sided", method="auto")
    sign = stats.binomtest(int((nonzero > 0).sum()), len(nonzero), 0.5, alternative="two-sided")

    # Deterministic bootstrap of the paired mean difference.
    rng = np.random.default_rng(20260813)
    boot = rng.choice(d, size=(20000, len(d)), replace=True).mean(axis=1)
    ci_low, ci_high = np.quantile(boot, [0.025, 0.975])

    mean_b = float(m.successes_baseline.mean())
    mean_p = float(m.successes_predictive.mean())
    mean_d = float(d.mean())
    sd_d = float(d.std(ddof=1))
    dz = mean_d / sd_d if sd_d else float("nan")

    summary = {
        "cells": int(len(m)),
        "baseline_mean": mean_b,
        "predictive_mean": mean_p,
        "paired_mean_delta": mean_d,
        "paired_sd_delta": sd_d,
        "paired_cohens_dz": float(dz),
        "predictive_better_cells": int((d > 0).sum()),
        "baseline_better_cells": int((d < 0).sum()),
        "ties": int((d == 0).sum()),
        "min_delta": int(d.min()),
        "max_delta": int(d.max()),
        "paired_t": float(t.statistic),
        "paired_t_p": float(t.pvalue),
        "wilcoxon_statistic": float(w.statistic),
        "wilcoxon_p": float(w.pvalue),
        "exact_sign_p": float(sign.pvalue),
        "bootstrap_mean_delta_ci95": [float(ci_low), float(ci_high)],
        "conclusion": "phase-dependent restructuring; no statistically significant universal improvement at alpha=0.05",
    }
    m.to_csv(out / "phase_space_comparison.csv", index=False)
    return summary


def metadata_reconciliation(root: Path, phase: dict) -> dict:
    # These are the values printed by the historical archived README. They are
    # retained as metadata for audit purposes, not treated as ground truth.
    historical = {"baseline_mean": 143.14, "predictive_mean": 115.03}
    mismatch = (
        not math.isclose(historical["baseline_mean"], phase["baseline_mean"], abs_tol=1e-9)
        or not math.isclose(historical["predictive_mean"], phase["predictive_mean"], abs_tol=1e-9)
    )
    return {
        "historical_readme_values": historical,
        "recomputed_csv_values": {
            "baseline_mean": phase["baseline_mean"],
            "predictive_mean": phase["predictive_mean"],
        },
        "mismatch": mismatch,
        "status": "STALE_METADATA" if mismatch else "CONSISTENT",
        "action": "Do not use historical README means as experimental evidence; use recomputed CSV means.",
    }


def independent_recurrence(out: Path) -> dict:
    """Falsification sanity check only; not the AEGIS theorem.

    The recurrence is intentionally generic. It must never be presented as an
    implementation of the archived Bash consensus model or as proof of Lambda.
    """
    rows = []
    for rho in np.linspace(0.0, 1.0, 11):
        for prune in np.linspace(0.0, 1.0, 11):
            for initial in (0.25, 0.5, 0.75, 1.0):
                x = initial
                for _ in range(500):
                    x = float(np.clip(x * (1.0 - prune) + rho * (1.0 - x), 0.0, 1.0))
                rows.append({"rho_recover": rho, "prune": prune, "initial": initial, "asymptotic_x": x, "nonzero": x > 1e-6})
    df = pd.DataFrame(rows)
    df.to_csv(out / "independent_recurrence.csv", index=False)
    return {
        "configs": int(len(df)),
        "nonzero_fraction": float(df.nonzero.mean()),
        "interpretation": "generic recurrence sanity check only; not proof of the AEGIS Lambda theorem",
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
                "min_vm_pu": float(net.res_bus.vm_pu.min()),
                "max_vm_pu": float(net.res_bus.vm_pu.max()),
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
    ax.set_title("Predictive − baseline success count")
    fig.colorbar(im, ax=ax, label="Δ successes")
    fig.tight_layout()
    fig.savefig(out / "fig_phase_space_delta.pdf", bbox_inches="tight")
    fig.savefig(out / "fig_phase_space_delta.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # A compact statistical effect plot for the paper.
    d = df.delta_successes.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axhline(0, linewidth=1)
    ax.plot(np.arange(1, len(d) + 1), d, marker="o", linewidth=1)
    ax.set_xlabel("Phase-space cell")
    ax.set_ylabel("Predictive − baseline successes")
    ax.set_title("Paired phase-space effect")
    fig.tight_layout()
    fig.savefig(out / "fig_paired_effect.pdf", bbox_inches="tight")
    fig.savefig(out / "fig_paired_effect.png", dpi=300, bbox_inches="tight")
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

    phase = phase_space_audit(root, out)
    report = {
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "phase_space": phase,
        "metadata_reconciliation": metadata_reconciliation(root, phase),
        "independent_recurrence": independent_recurrence(out),
        "solver_check": solver_check(out),
        "claim_audit": {
            "recovery_elasticity_lambda": "NOT_EMPIRICALLY_PROVEN_BY_ARCHIVED_IMPLEMENTATION",
            "reason": "The archived consensus_v4.sh uses fixed SLASH/RECOVER parameters and heuristic trust updates; it does not explicitly implement the recurrence from which the proposed Lambda theorem is derived.",
            "physical_ac_grid_claim": "NOT_VALIDATED_BY_THIS_AUDIT",
            "reason_physical": "The current validation artifact contains generic pandapower test networks, not the claimed 9,450 AC evaluations or a reproducible attack-to-grid coupling dataset.",
        },
    }
    (out / "audit_summary.json").write_text(json.dumps(report, indent=2))
    make_figures(out)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
