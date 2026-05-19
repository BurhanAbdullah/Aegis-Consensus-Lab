import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

df = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

df.columns = [c.strip().lower() for c in df.columns]

table = df.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

regime = np.zeros_like(table.values)

for i in range(table.shape[0]):
    for j in range(table.shape[1]):

        val = table.values[i, j]

        if val >= 160:
            regime[i, j] = 3
        elif val >= 120:
            regime[i, j] = 2
        elif val >= 80:
            regime[i, j] = 1
        else:
            regime[i, j] = 0

cmap = ListedColormap([
    "#440154",
    "#31688e",
    "#35b779",
    "#fde725"
])

labels = [
    "Collapse",
    "Turbulent",
    "Metastable",
    "Stable"
]

fig, ax = plt.subplots(figsize=(10,7))

im = ax.imshow(
    regime,
    cmap=cmap,
    origin="lower",
    aspect="auto"
)

ax.set_xticks(np.arange(len(table.columns)))
ax.set_yticks(np.arange(len(table.index)))

ax.set_xticklabels(table.columns)
ax.set_yticklabels(table.index)

ax.set_xlabel("Slashing Rate λ")
ax.set_ylabel("Recovery Rate ρ")

ax.set_title(
    "Governance Regime Classification Map",
    fontsize=15
)

for i in range(regime.shape[0]):
    for j in range(regime.shape[1]):

        ax.text(
            j,
            i,
            labels[regime[i, j]],
            ha="center",
            va="center",
            fontsize=7,
            color="black"
        )

cbar = fig.colorbar(
    im,
    ticks=[0,1,2,3]
)

cbar.ax.set_yticklabels(labels)

plt.tight_layout()

plt.savefig(
    "experiments/regime_classification_map.png",
    dpi=500,
    bbox_inches="tight"
)

plt.savefig(
    "experiments/regime_classification_map.pdf",
    bbox_inches="tight"
)

print("Generated regime classification map.")
