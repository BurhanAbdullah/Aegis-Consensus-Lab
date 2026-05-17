import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# LOAD DATA
# =====================================================

results = pd.read_csv("metrics/results.csv")
trust = pd.read_csv("history/trust.csv")

# =====================================================
# SUCCESS / FAILURE OVER TIME
# =====================================================

results["success_binary"] = results["status"].apply(
    lambda x: 1 if x == "success" else 0
)

plt.figure(figsize=(12,5))

plt.plot(results["round"], results["success_binary"])

plt.xlabel("Round")
plt.ylabel("Consensus Success")
plt.title("Consensus Survivability Over Time")

plt.savefig("plots/survivability.png")

# =====================================================
# SAFETY EVOLUTION
# =====================================================

plt.figure(figsize=(12,5))

plt.plot(results["round"], results["safety"])

plt.xlabel("Round")
plt.ylabel("Safety Envelope")
plt.title("Epistemic Safety Evolution")

plt.savefig("plots/safety.png")

# =====================================================
# QUORUM VS PREPARE
# =====================================================

plt.figure(figsize=(12,5))

plt.plot(results["round"], results["quorum"], label="Quorum")
plt.plot(results["round"], results["prepare_weight"], label="Prepare")

plt.legend()

plt.xlabel("Round")
plt.ylabel("Weight")
plt.title("Quorum vs Prepare Weight")

plt.savefig("plots/quorum_prepare.png")

# =====================================================
# TRUST TRAJECTORIES
# =====================================================

plt.figure(figsize=(12,5))

for validator in trust["validator"].unique():

    subset = trust[trust["validator"] == validator]

    plt.plot(
        subset["round"],
        subset["trust"],
        label=validator
    )

plt.legend()

plt.xlabel("Round")
plt.ylabel("Trust")
plt.title("Validator Trust Trajectories")

plt.savefig("plots/trust.png")

print()
print("Plots generated:")
print("  plots/survivability.png")
print("  plots/safety.png")
print("  plots/quorum_prepare.png")
print("  plots/trust.png")
