import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("experiments/phase_space.csv")

# Normalize column names
df.columns = [c.strip().lower() for c in df.columns]

# ============================================
# PIVOT TABLE
# ============================================

table = df.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

# ============================================
# CREATE FIGURE
# ============================================

fig, ax = plt.subplots(figsize=(10, 7))

im = ax.imshow(
    table.values,
    cmap="viridis",
    origin="lower",
    aspect="auto"
)

# ============================================
# AXIS LABELS
# ============================================

ax.set_xticks(np.arange(len(table.columns)))
ax.set_yticks(np.arange(len(table.index)))

ax.set_xticklabels(table.columns)
ax.set_yticklabels(table.index)

ax.set_xlabel(
    "SLASH Penalty",
    fontsize=12
)

ax.set_ylabel(
    "RECOVER Rate",
    fontsize=12
)

ax.set_title(
    "AEGIS Adaptive Consensus Phase Space",
    fontsize=16,
    pad=15
)

# ============================================
# CELL ANNOTATIONS
# ============================================

for i in range(table.shape[0]):
    for j in range(table.shape[1]):

        val = int(table.iloc[i, j])

        color = "white"

        if val > 140:
            color = "black"

        ax.text(
            j,
            i,
            str(val),
            ha="center",
            va="center",
            fontsize=10,
            color=color
        )

# ============================================
# COLORBAR
# ============================================

cbar = fig.colorbar(im)

cbar.set_label(
    "Successful Consensus Finalizations",
    rotation=90,
    fontsize=11
)

# ============================================
# REGION LABELS
# ============================================

ax.text(
    0.6,
    4.7,
    "Stable Basin",
    fontsize=11,
    bbox=dict(facecolor="white", alpha=0.85)
)

ax.text(
    4.3,
    0.8,
    "Collapse\nRegion",
    fontsize=11,
    bbox=dict(facecolor="white", alpha=0.85)
)

# ============================================
# SAVE
# ============================================

plt.tight_layout()

plt.savefig(
    "experiments/phase_space_publication.png",
    dpi=400,
    bbox_inches="tight"
)

print()
print("Generated:")
print("experiments/phase_space_publication.png")
