"""Generate publication comparison artifacts from the frozen release traces.

This generator is deliberately fail-closed.  It validates the input schema,
round coverage, numeric fields, and paired round identity before writing any
publication artifact.  Paths are resolved from the repository root rather than
from the caller's working directory so the same command behaves identically in
local runs and CI.
"""
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "archive" / "final_run" / "experiments" / "results.csv"
PRED = REPO_ROOT / "archive" / "final_run" / "experiments" / "results_predictive.csv"
OUT_CSV = REPO_ROOT / "experiments" / "publication_comparison.csv"
OUT_TEX = REPO_ROOT / "experiments" / "publication_tables.tex"

REQUIRED = {
    "round", "total_weight", "quorum", "safety", "prepare_weight",
    "commit_weight", "primary", "status",
}
NUMERIC = {
    "round", "total_weight", "quorum", "safety", "prepare_weight",
    "commit_weight",
}


def load(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"missing frozen release artifact: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"missing CSV header: {path}")
        missing = REQUIRED - set(reader.fieldnames)
        if missing:
            raise ValueError(f"{path}: missing required columns {sorted(missing)}")
        rows = list(reader)
    if len(rows) != 200:
        raise ValueError(f"{path}: expected exactly 200 rounds, found {len(rows)}")
    for index, row in enumerate(rows, start=1):
        for field in NUMERIC:
            try:
                float(row[field])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{path}: non-numeric {field!r} at row {index}") from exc
    rounds = [int(row["round"]) for row in rows]
    if rounds != list(range(1, 201)):
        raise ValueError(f"{path}: round IDs must be exactly 1..200")
    return rows


def summarize(rows: list[dict[str, str]]) -> dict[str, float]:
    return {
        "rounds": len(rows),
        "success_rate": sum(r["status"] == "success" for r in rows) / len(rows),
        "mean_quorum": mean(float(r["quorum"]) for r in rows),
        "mean_safety": mean(float(r["safety"]) for r in rows),
        "mean_commit": mean(float(r["commit_weight"]) for r in rows),
        "mean_total_weight": mean(float(r["total_weight"]) for r in rows),
    }


def run() -> tuple[Path, Path]:
    base, pred = load(BASE), load(PRED)
    base_rounds = [int(r["round"]) for r in base]
    pred_rounds = [int(r["round"]) for r in pred]
    if base_rounds != pred_rounds:
        raise ValueError("reference and predictive artifacts do not share identical round IDs")

    sb, sp = summarize(base), summarize(pred)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fields = ["metric", "reference", "predictive", "predictive_minus_reference"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for metric in ("success_rate", "mean_quorum", "mean_safety", "mean_commit", "mean_total_weight"):
            writer.writerow({
                "metric": metric,
                "reference": f"{sb[metric]:.10g}",
                "predictive": f"{sp[metric]:.10g}",
                "predictive_minus_reference": f"{sp[metric] - sb[metric]:.10g}",
            })

    labels = {
        "success_rate": "Finalization rate (\\%)",
        "mean_quorum": "Mean quorum weight",
        "mean_safety": "Mean safety score",
        "mean_commit": "Mean commit weight",
        "mean_total_weight": "Mean total governance weight",
    }
    lines = [
        "% Auto-generated from archive/final_run/experiments/*.csv; do not edit by hand.",
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Reproducible comparison from the frozen 200-round release traces.}",
        "\\label{tab:release-comparison}",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Metric & Reference & Predictive & Difference \\\\",
        "\\midrule",
    ]
    for metric, label in labels.items():
        if metric == "success_rate":
            values = (100 * sb[metric], 100 * sp[metric], 100 * (sp[metric] - sb[metric]))
            lines.append(f"{label} & {values[0]:.2f} & {values[1]:.2f} & {values[2]:+.2f} \\\\")
        else:
            values = (sb[metric], sp[metric], sp[metric] - sb[metric])
            lines.append(f"{label} & {values[0]:.2f} & {values[1]:.2f} & {values[2]:+.2f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")

    if OUT_CSV.stat().st_size == 0 or OUT_TEX.stat().st_size == 0:
        raise RuntimeError("publication artifact generation produced an empty file")
    return OUT_CSV, OUT_TEX


if __name__ == "__main__":
    csv_path, tex_path = run()
    print(f"generated {csv_path} and {tex_path}")
