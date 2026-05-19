import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

baseline = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

predictive = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

baseline.columns = [c.strip().lower() for c in baseline.columns]
predictive.columns = [c.strip().lower() for c in predictive.columns]

base = baseline.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

pred = predictive.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

diff = pred - base

fig, ax = plt.subplots(figsize=(10,7))

im = ax.imshow(
    diff.values,
    cmap="coolwarm",
    origin="lower",
    aspect="auto"
)

ax.set_xticks(np.arange(len(diff.columns)))
ax.set_yticks(np.arange(len(diff.index)))

ax.set_xticklabels(diff.columns)
ax.set_yticklabels(diff.index)

ax.set_xlabel("Slashing Rate λ", fontsize=12)
ax.set_ylabel("Recovery Rate ρ", fontsize=12)

ax.set_title(
    "Predictive Containment Survivability Deformation",
    fontsize=15,
    pad=15
)

for i in range(diff.shape[0]):
    for j in range(diff.shape[1]):

        val = int(diff.iloc[i, j])

        ax.text(
            j,
            i,
            f"{val:+d}",
            ha="center",
            va="center",
            fontsize=9,
            color="black"
        )

cbar = fig.colorbar(im)

cbar.set_label(
    "Predictive − Baseline Finalizations",
    rotation=90,
    fontsize=11
)

ax.text(
    0.7,
    4.6,
    "Localized\nStabilization",
    fontsize=10,
    bbox=dict(facecolor="white", alpha=0.7)
)

ax.text(
    4.0,
    1.0,
    "Metastable\nFragmentation",
    fontsize=10,
    bbox=dict(facecolor="white", alpha=0.7)
)

plt.tight_layout()

plt.savefig(
    "experiments/difference_heatmap_publication.png",
    dpi=500,
    bbox_inches="tight"
)

plt.savefig(
    "experiments/difference_heatmap_publication.pdf",
    bbox_inches="tight"
)

print("Generated difference heatmap.")
