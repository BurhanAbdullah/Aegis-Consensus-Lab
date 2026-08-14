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
    diffs = [float(r["attack_finalization_difference"]) for r in comp]
    print("COMPARATIVE_GRID rows", len(comp)); print("COMPARATIVE_GRID difference mean_ci95", ci95(diffs))
    print("COMPARATIVE_GRID nonzero differences", sum(abs(x) > 1e-12 for x in diffs))
    print("COMPARATIVE_GRID positive AEGIS differences", sum(x > 1e-12 for x in diffs))
    print("COMPARATIVE_GRID negative AEGIS differences", sum(x < -1e-12 for x in diffs))
    for count in sorted({int(r["attack_count"]) for r in comp}):
        xs = [float(r["attack_finalization_difference"]) for r in comp if int(r["attack_count"]) == count]
        print("COMPARATIVE_GRID attack_count", count, ci95(xs))

    abl = rows("experiments/ablation.csv")
    for variant in sorted({r["variant"] for r in abl}):
        xs = [float(r["attack_finalization_rate"]) for r in abl if r["variant"] == variant]
        print("ABLATION", variant, ci95(xs))

    loc = rows("experiments/localization.csv")
    for v in sorted({r["location"] for r in loc}):
        xs = [float(r["risk_activation_rate"]) for r in loc if r["location"] == v]
        print("LOCALIZATION", v, ci95(xs))
