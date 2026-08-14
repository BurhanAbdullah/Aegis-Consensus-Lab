"""Generate publication figures from frozen comparative, ablation, and localization CSV artifacts."""
from __future__ import annotations
from pathlib import Path
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("experiments/figures")
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(fig, stem):
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def comparative_heatmap():
    rows = read_csv("experiments/comparative_grid.csv")
    e_levels = sorted({float(r["evidence"]) for r in rows})
    counts = sorted({int(r["attack_count"]) for r in rows})
    policies = (("q67", "aegis_minus_q67_difference"), ("q75", "aegis_minus_q75_difference"))
    for suffix, field in policies:
        vals = np.zeros((len(counts), len(e_levels)))
        n = np.zeros_like(vals)
        for r in rows:
            i = counts.index(int(r["attack_count"]))
            j = e_levels.index(float(r["evidence"]))
            vals[i, j] += float(r[field])
            n[i, j] += 1
        vals /= n
        fig, ax = plt.subplots(figsize=(6.6, 4.8))
        im = ax.imshow(vals, origin="lower", aspect="auto")
        ax.set_xticks(range(len(e_levels)), [f"{x:.2f}" for x in e_levels])
        ax.set_yticks(range(len(counts)), counts)
        ax.set_xlabel("Attack evidence")
        ax.set_ylabel("Number of compromised validators")
        ax.set_title(f"AEGIS minus fixed quorum ({'q = 0.67' if suffix == 'q67' else 'q = 0.75'})")
        fig.colorbar(im, ax=ax, label="Attack-period finalization-rate difference")
        save(fig, f"comparative_attack_phase_{suffix}")


def ablation_bar():
    rows = read_csv("experiments/ablation.csv")
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["variant"]].append(float(r["attack_finalization_rate"]))
    names = list(grouped)
    means = [np.mean(grouped[n]) for n in names]
    cis = [1.96 * np.std(grouped[n], ddof=1) / np.sqrt(len(grouped[n])) if len(grouped[n]) > 1 else 0 for n in names]
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    x = np.arange(len(names))
    ax.bar(x, means, yerr=cis, capsize=4)
    ax.set_xticks(x, [n.replace("_", "\n") for n in names])
    ax.set_ylabel("Attack-period finalization rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("Component ablation: availability")
    save(fig, "component_ablation")


def ablation_safety_bar():
    rows = read_csv("experiments/ablation.csv")
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["variant"]].append(float(r["unsafe_certificate_boundary_fraction"]))
    names = list(grouped)
    means = [np.mean(grouped[n]) for n in names]
    cis = [1.96 * np.std(grouped[n], ddof=1) / np.sqrt(len(grouped[n])) if len(grouped[n]) > 1 else 0 for n in names]
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    x = np.arange(len(names))
    ax.bar(x, means, yerr=cis, capsize=4)
    ax.set_xticks(x, [n.replace("_", "\n") for n in names])
    ax.set_ylabel("Fraction at or below certificate boundary")
    ax.set_ylim(0, 1.05)
    ax.set_title("Component ablation: analytical safety boundary")
    save(fig, "component_ablation_safety")


def localization_heatmap():
    rows = read_csv("experiments/localization.csv")
    locations = sorted({r["location"] for r in rows})
    magnitudes = sorted({float(r["magnitude"]) for r in rows})
    vals = np.zeros((len(locations), len(magnitudes)))
    counts = np.zeros_like(vals)
    for r in rows:
        i = locations.index(r["location"])
        j = magnitudes.index(float(r["magnitude"]))
        vals[i, j] += float(r["influence_drop"])
        counts[i, j] += 1
    vals /= counts
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    im = ax.imshow(vals, origin="lower", aspect="auto")
    ax.set_xticks(range(len(magnitudes)), [f"{x:.2f}" for x in magnitudes])
    ax.set_yticks(range(len(locations)), locations)
    ax.set_xlabel("Attack evidence magnitude")
    ax.set_ylabel("Attacked validator")
    ax.set_title("Localization: influence reduction under attack")
    fig.colorbar(im, ax=ax, label="Influence drop")
    save(fig, "attack_localization")


if __name__ == "__main__":
    comparative_heatmap()
    ablation_bar()
    ablation_safety_bar()
    localization_heatmap()
    print(f"wrote publication figures to {OUT}")
