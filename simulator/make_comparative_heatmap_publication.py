import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# LOAD DATA
# =====================================================

baseline = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

predictive = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

# =====================================================
# NORMALIZE COLUMNS
# =====================================================

baseline.columns = [
    c.strip().upper() for c in baseline.columns
]

predictive.columns = [
    c.strip().upper() for c in predictive.columns
]

# =====================================================
# DETECT VALUE COLUMN
# =====================================================

value_column = None

for candidate in [
    "SUCCESS",
    "SUCCESSES",
    "FINALIZATIONS",
    "VALUE"
]:
    if candidate in baseline.columns:
        value_column = candidate
        break

if value_column is None:
    raise Exception(
        f"Could not detect value column. Found: {baseline.columns}"
    )

print(f"Using value column: {value_column}")

# =====================================================
# PIVOT
# =====================================================

base = baseline.pivot(
    index="RECOVER",
    columns="SLASH",
    values=value_column
)

pred = predictive.pivot(
    index="RECOVER",
    columns="SLASH",
    values=value_column
)

# =====================================================
# FIGURE
# =====================================================

plt.rcParams.update({
    "font.size": 14,
    "font.family": "DejaVu Sans"
})

fig, axes = plt.subplots(
    1,
    2,
    figsize=(24, 10)
)

fig.subplots_adjust(
    wspace=0.18,
    bottom=0.15,
    top=0.88
)

vmin = min(base.min().min(), pred.min().min())
vmax = max(base.max().max(), pred.max().max())

# =====================================================
# BASELINE PANEL
# =====================================================

im1 = axes[0].imshow(
    base.values,
    cmap="viridis",
    aspect="auto",
    origin="lower",
    vmin=vmin,
    vmax=vmax
)

axes[0].set_title(
    "Baseline Governance",
    fontsize=24,
    fontweight="bold",
    pad=20
)

axes[0].set_xlabel(
    "Slashing Rate λ",
    fontsize=20,
    fontweight="bold"
)

axes[0].set_ylabel(
    "Recovery Rate ρ",
    fontsize=20,
    fontweight="bold"
)

axes[0].set_xticks(range(len(base.columns)))
axes[0].set_xticklabels(base.columns, fontsize=16)

axes[0].set_yticks(range(len(base.index)))
axes[0].set_yticklabels(base.index, fontsize=16)

# =====================================================
# PREDICTIVE PANEL
# =====================================================

im2 = axes[1].imshow(
    pred.values,
    cmap="viridis",
    aspect="auto",
    origin="lower",
    vmin=vmin,
    vmax=vmax
)

axes[1].set_title(
    "Predictive Governance",
    fontsize=24,
    fontweight="bold",
    pad=20
)

axes[1].set_xlabel(
    "Slashing Rate λ",
    fontsize=20,
    fontweight="bold"
)

axes[1].set_ylabel(
    "Recovery Rate ρ",
    fontsize=20,
    fontweight="bold"
)

axes[1].set_xticks(range(len(pred.columns)))
axes[1].set_xticklabels(pred.columns, fontsize=16)

axes[1].set_yticks(range(len(pred.index)))
axes[1].set_yticklabels(pred.index, fontsize=16)

# =====================================================
# ANNOTATIONS
# =====================================================

for i in range(base.shape[0]):
    for j in range(base.shape[1]):

        val = int(base.values[i, j])

        color = "white" if val < 140 else "black"

        axes[0].text(
            j,
            i,
            str(val),
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=color
        )

for i in range(pred.shape[0]):
    for j in range(pred.shape[1]):

        val = int(pred.values[i, j])

        color = "white" if val < 140 else "black"

        axes[1].text(
            j,
            i,
            str(val),
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=color
        )

# =====================================================
# COLORBAR
# =====================================================

cbar = fig.colorbar(
    im2,
    ax=axes,
    shrink=0.92,
    pad=0.02
)

cbar.set_label(
    "Consensus Finalizations",
    fontsize=18,
    fontweight="bold",
    labelpad=18
)

cbar.ax.tick_params(labelsize=14)

# =====================================================
# FOOTNOTE
# =====================================================

fig.text(
    0.5,
    0.04,
    "Higher values indicate greater synchronization survivability across governance regimes.",
    ha="center",
    fontsize=15,
    bbox=dict(
        facecolor="whitesmoke",
        edgecolor="gray",
        boxstyle="round,pad=0.6"
    )
)

# =====================================================
# SAVE
# =====================================================

plt.savefig(
    "experiments/comparative_governance_landscapes_publication.png",
    dpi=600,
    bbox_inches="tight"
)

plt.savefig(
    "experiments/comparative_governance_landscapes_publication.pdf",
    bbox_inches="tight"
)

print()
print("Generated:")
print("  experiments/comparative_governance_landscapes_publication.png")
print("  experiments/comparative_governance_landscapes_publication.pdf")

