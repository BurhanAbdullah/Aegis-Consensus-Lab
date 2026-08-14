"""Print aggregate, non-cherry-picked summaries of publication experiments."""
from __future__ import annotations
import csv
from pathlib import Path
from statistics import mean, stdev
from math import sqrt


def rows(path):
    with Path(path).open(encoding="utf-8", newline="") as f: return list(csv.DictReader(f))


def ci95(xs):
    m = mean(xs)
    if len(xs) < 2: return m, m, m
    h = 1.96 * stdev(xs) / sqrt(len(xs)); return m, m - h, m + h


if __name__ == "__main__":
    comp = rows("experiments/comparative_grid.csv")
    print("COMPARATIVE_GRID rows", len(comp))
    for field in ("aegis_minus_q67_difference", "aegis_minus_q75_difference"):
        diffs = [float(r[field]) for r in comp]
        print("COMPARATIVE_GRID", field, "mean_ci95", ci95(diffs), "positive", sum(x > 1e-12 for x in diffs), "negative", sum(x < -1e-12 for x in diffs))
        for count in sorted({int(r["attack_count"]) for r in comp}):
            xs = [float(r[field]) for r in comp if int(r["attack_count"]) == count]
            print("COMPARATIVE_GRID", field, "attack_count", count, ci95(xs))

    abl = rows("experiments/ablation.csv")
    for variant in sorted({r["variant"] for r in abl}):
        xs = [float(r["attack_finalization_rate"]) for r in abl if r["variant"] == variant]
        unsafe = [float(r["unsafe_certificate_boundary_fraction"]) for r in abl if r["variant"] == variant]
        safety = [float(r["mean_safety_margin"]) for r in abl if r["variant"] == variant]
        print("ABLATION", variant, "availability_ci95", ci95(xs), "unsafe_boundary_ci95", ci95(unsafe), "safety_margin_ci95", ci95(safety))

    loc = rows("experiments/localization.csv")
    for v in sorted({r["location"] for r in loc}):
        risk = [float(r["risk_activation_rate"]) for r in loc if r["location"] == v]
        drop = [float(r["influence_drop"]) for r in loc if r["location"] == v]
        print("LOCALIZATION", v, "risk_activation_ci95", ci95(risk), "influence_drop_ci95", ci95(drop))
