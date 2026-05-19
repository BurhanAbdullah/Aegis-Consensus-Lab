import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

base = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

pred = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

base.columns = [c.strip().lower() for c in base.columns]
pred.columns = [c.strip().lower() for c in pred.columns]

base_table = base.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

pred_table = pred.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

vmin = min(
    base_table.values.min(),
    pred_table.values.min()
)

vmax = max(
    base_table.values.max(),
    pred_table.values.max()
)

fig, axes = plt.subplots(
    1,
    2,
    figsize=(15,6)
)

titles = [
    "Baseline Governance",
    "Predictive Governance"
]

tables = [
    base_table,
    pred_table
]

for ax, table, title in zip(
    axes,
    tables,
    titles
):

    im = ax.imshow(
        table.values,
        cmap="viridis",
        origin="lower",
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )

    ax.set_xticks(np.arange(len(table.columns)))
    ax.set_yticks(np.arange(len(table.index)))

    ax.set_xticklabels(table.columns)
    ax.set_yticklabels(table.index)

    ax.set_xlabel("Slashing Rate λ")
    ax.set_ylabel("Recovery Rate ρ")

    ax.set_title(title)

    for i in range(table.shape[0]):
        for j in range(table.shape[1]):

            val = int(table.iloc[i, j])

            ax.text(
                j,
                i,
                str(val),
                ha="center",
                va="center",
                fontsize=8,
                color="white" if val < 140 else "black"
            )

fig.colorbar(
    im,
    ax=axes.ravel().tolist(),
    label="Consensus Finalizations"
)

plt.tight_layout()

plt.savefig(
    "experiments/comparative_governance_landscapes.png",
    dpi=500,
    bbox_inches="tight"
)

plt.savefig(
    "experiments/comparative_governance_landscapes.pdf",
    bbox_inches="tight"
)

print("Generated comparative governance panel.")
