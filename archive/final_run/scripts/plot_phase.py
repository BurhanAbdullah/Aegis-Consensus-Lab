import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("experiments/phase_space.csv")

pivot = df.pivot(
    index="recover",
    columns="slash",
    values="successes"
)

plt.figure(figsize=(10, 6))

plt.imshow(
    pivot,
    origin="lower",
    aspect="auto"
)

plt.colorbar(label="Successful Consensus Rounds")

plt.xticks(
    range(len(pivot.columns)),
    pivot.columns
)

plt.yticks(
    range(len(pivot.index)),
    pivot.index
)

plt.xlabel("SLASH")
plt.ylabel("RECOVER")

plt.title("AEGIS Adaptive Consensus Phase Space")

for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):

        plt.text(
            j,
            i,
            str(pivot.iloc[i, j]),
            ha="center",
            va="center"
        )

plt.tight_layout()

plt.savefig("experiments/phase_space.png")

print("Saved: experiments/phase_space.png")
