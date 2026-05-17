import pandas as pd

baseline = pd.read_csv(
    "experiments/phase_space_baseline.csv"
)

predictive = pd.read_csv(
    "experiments/phase_space_predictive.csv"
)

# ============================================
# GLOBAL STATISTICS
# ============================================

base_mean = baseline["successes"].mean()
pred_mean = predictive["successes"].mean()

base_std = baseline["successes"].std()
pred_std = predictive["successes"].std()

# ============================================
# STABLE REGIONS
# ============================================

base_stable = len(
    baseline[baseline["successes"] >= 180]
)

pred_stable = len(
    predictive[predictive["successes"] >= 180]
)

# ============================================
# TURBULENCE REGIONS
# ============================================

base_turbulence = len(
    baseline[
        (baseline["successes"] >= 60) &
        (baseline["successes"] <= 140)
    ]
)

pred_turbulence = len(
    predictive[
        (predictive["successes"] >= 60) &
        (predictive["successes"] <= 140)
    ]
)

# ============================================
# COLLAPSE REGIONS
# ============================================

base_collapse = len(
    baseline[baseline["successes"] < 60]
)

pred_collapse = len(
    predictive[predictive["successes"] < 60]
)

# ============================================
# OUTPUT
# ============================================

print("===================================")
print("AEGIS PHASE ANALYSIS")
print("===================================")

print()
print("GLOBAL SUCCESS")

print(f"Baseline mean     : {base_mean:.2f}")
print(f"Predictive mean   : {pred_mean:.2f}")

print()
print("GLOBAL VARIANCE")

print(f"Baseline stddev   : {base_std:.2f}")
print(f"Predictive stddev : {pred_std:.2f}")

print()
print("STABLE REGIONS (>=180)")

print(f"Baseline stable   : {base_stable}")
print(f"Predictive stable : {pred_stable}")

print()
print("TURBULENCE REGIONS (60-140)")

print(f"Baseline turbulence   : {base_turbulence}")
print(f"Predictive turbulence : {pred_turbulence}")

print()
print("COLLAPSE REGIONS (<60)")

print(f"Baseline collapse   : {base_collapse}")
print(f"Predictive collapse : {pred_collapse}")
