"""Generate manuscript tables only from frozen release experiment artifacts.

No values are hard-coded. The script fails closed if either source artifact is
missing, if the traces differ in round IDs, or if the frozen release is not the
expected 200-round artifact set.
"""
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

BASE = Path("archive/final_run/experiments/results.csv")
PRED = Path("archive/final_run/experiments/results_predictive.csv")
OUT_CSV = Path("experiments/publication_comparison.csv")
OUT_TEX = Path("experiments/publication_tables.tex")


def load(path: Path):
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"empty artifact: {path}")
    return rows


def summarize(rows):
    return {
        "rounds": len(rows),
        "success_rate": sum(r["status"] == "success" for r in rows) / len(rows),
        "mean_quorum": mean(float(r["quorum"]) for r in rows),
        "mean_safety": mean(float(r["safety"]) for r in rows),
        "mean_commit": mean(float(r["commit_weight"]) for r in rows),
        "mean_total_weight": mean(float(r["total_weight"]) for r in rows),
    }


def run():
    base, pred = load(BASE), load(PRED)
    if len(base) != 200 or len(pred) != 200:
        raise ValueError("publication release artifacts must each contain exactly 200 rounds")
    base_rounds = [int(r["round"]) for r in base]
    pred_rounds = [int(r["round"]) for r in pred]
    if base_rounds != pred_rounds:
        raise ValueError("reference and predictive artifacts do not share identical round IDs")

    sb, sp = summarize(base), summarize(pred)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fields = ["metric", "reference", "predictive", "predictive_minus_reference"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for metric in ["success_rate", "mean_quorum", "mean_safety", "mean_commit", "mean_total_weight"]:
            w.writerow({"metric": metric, "reference": f"{sb[metric]:.10g}",
                        "predictive": f"{sp[metric]:.10g}",
                        "predictive_minus_reference": f"{sp[metric]-sb[metric]:.10g"})

    tex = r"""% Auto-generated from archive/final_run/experiments/*.csv; do not edit by hand.
\begin{table}[t]
\centering
\caption{Reproducible comparison from the frozen 200-round release traces.}
\label{tab:release-comparison}
\begin{tabular}{lrrr}
\toprule
Metric & Reference & Predictive & Difference \\
\midrule
"""
    labels = {
        "success_rate": "Finalization rate",
        "mean_quorum": "Mean quorum weight",
        "mean_safety": "Mean safety score",
        "mean_commit": "Mean commit weight",
        "mean_total_weight": "Mean total governance weight",
    }
    for metric in labels:
        if metric == "success_rate":
            tex += f"{labels[metric]} (\%) & {100*sb[metric]:.2f} & {100*sp[metric]:.2f} & {100*(sp[metric]-sb[metric]):+.2f} \\\n"
        else:
            tex += f"{labels[metric]} & {sb[metric]:.2f} & {sp[metric]:.2f} & {sp[metric]-sb[metric]:+.2f} \\\n"
    tex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    OUT_TEX.write_text(tex, encoding="utf-8")
    return OUT_CSV, OUT_TEX


if __name__ == "__main__":
    csv_path, tex_path = run()
    print(f"generated {csv_path} and {tex_path}")
