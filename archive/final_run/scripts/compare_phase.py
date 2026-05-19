import pandas as pd
import matplotlib.pyplot as plt

baseline = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

predictive = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

# ============================================
# PIVOTS
# ============================================

base_pivot = baseline.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

pred_pivot = predictive.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

difference = pred_pivot - base_pivot

# ============================================
# BASELINE HEATMAP
# ============================================

plt.figure(figsize=(8, 6))

plt.imshow(
    base_pivot,
    origin="lower",
    aspect="auto"
)

plt.colorbar(label="Successes")

plt.xticks(
    range(len(base_pivot.columns)),
    base_pivot.columns
)

plt.yticks(
    range(len(base_pivot.index)),
    base_pivot.index
)

plt.xlabel("SLASH")
plt.ylabel("RECOVER")

plt.title("Baseline Adaptive Consensus")

plt.tight_layout()

plt.savefig(
    "experiments/baseline_heatmap.png"
)

plt.close()

# ============================================
# PREDICTIVE HEATMAP
# ============================================

plt.figure(figsize=(8, 6))

plt.imshow(
    pred_pivot,
    origin="lower",
    aspect="auto"
)

plt.colorbar(label="Successes")

plt.xticks(
    range(len(pred_pivot.columns)),
    pred_pivot.columns
)

plt.yticks(
    range(len(pred_pivot.index)),
    pred_pivot.index
)

plt.xlabel("SLASH")
plt.ylabel("RECOVER")

plt.title("Predictive Epistemic Governance")

plt.tight_layout()

plt.savefig(
    "experiments/predictive_heatmap.png"
)

plt.close()

# ============================================
# DIFFERENCE HEATMAP
# ============================================

plt.figure(figsize=(8, 6))

plt.imshow(
    difference,
    origin="lower",
    aspect="auto"
)

plt.colorbar(label="Predictive - Baseline")

plt.xticks(
    range(len(difference.columns)),
    difference.columns
)

plt.yticks(
    range(len(difference.index)),
    difference.index
)

plt.xlabel("SLASH")
plt.ylabel("RECOVER")

plt.title("Phase Topology Shift")

for i in range(len(difference.index)):
    for j in range(len(difference.columns)):

        plt.text(
            j,
            i,
            str(int(difference.iloc[i, j])),
            ha="center",
            va="center"
        )

plt.tight_layout()

plt.savefig(
    "experiments/difference_heatmap.png"
)

plt.close()

print("Generated:")
print("  baseline_heatmap.png")
print("  predictive_heatmap.png")
print("  difference_heatmap.png")
