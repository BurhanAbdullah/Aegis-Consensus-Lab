import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

df.columns = [c.strip().lower() for c in df.columns]

table = df.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

fig, ax = plt.subplots(figsize=(10,7))

im = ax.imshow(
    table.values,
    cmap="viridis",
    origin="lower",
    aspect="auto"
)

ax.set_xticks(np.arange(len(table.columns)))
ax.set_yticks(np.arange(len(table.index)))

ax.set_xticklabels(table.columns)
ax.set_yticklabels(table.index)

ax.set_xlabel("Slashing Rate λ", fontsize=12)
ax.set_ylabel("Recovery Rate ρ", fontsize=12)

ax.set_title(
    "Baseline Governance Survivability Landscape",
    fontsize=15,
    pad=15
)

for i in range(table.shape[0]):
    for j in range(table.shape[1]):

        val = int(table.iloc[i, j])

        ax.text(
            j,
            i,
            str(val),
            ha="center",
            va="center",
            fontsize=9,
            color="white" if val < 140 else "black"
        )

cbar = fig.colorbar(im)

cbar.set_label(
    "Consensus Finalizations over 200 Rounds",
    rotation=90,
    fontsize=11
)

plt.tight_layout()

plt.savefig(
    "experiments/baseline_heatmap_publication.png",
    dpi=500,
    bbox_inches="tight"
)

plt.savefig(
    "experiments/baseline_heatmap_publication.pdf",
    bbox_inches="tight"
)

print("Generated baseline heatmap.")
