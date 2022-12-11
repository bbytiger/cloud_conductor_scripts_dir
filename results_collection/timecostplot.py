import matplotlib.pyplot as plt
import numpy as np

x = [32.87103542, 24.96560801, 21.92120118]
y = [0.004802823508, 0.008405088031, 0.01960729661]
labels = [("AWS G4", "red"), ("AWS G5", "blue"), ("GCP TPU", "green")]

for i in range(3):
    plt.scatter(x[i], y[i], label=labels[i][0], color=labels[i][1])
plt.title("Comparing Hardware Accelerators Across Clouds")
plt.xlabel("Runtime (s)")
plt.ylabel("Cost ($)")
plt.legend()
plt.show()