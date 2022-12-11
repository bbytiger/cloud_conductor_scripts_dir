import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8, 7))

coredata = [
    ([
        (0.003355880642, 27.96567202, "c5n.large"), 
        (0.000942850146, 33.94260526, "c4.large"), 
        (0.0007097459252, 38.13218713, "e2-standard-2")
    ], "2 cores", "blue"),
    ([
        (0.001848805618, 15.40671349, "c5n.xlarge"),
        (0.001029733186, 18.62833905, "c4.xlarge"),
        (0.000743762953, 19.97990203, "e2-standard-4"),
    ], "4 cores", "red"),
    ([
        (0.001560149202, 13.00124335, "c5n.2xlarge"),
        (0.001772901496, 16.03629494, "c4.2xlarge"),
        (0.0009004031895, 12.09388518, "e2-standard-8"),
    ], "8 cores", "orange")
]

for i in range(3):
    plt.scatter(
        [y[1] for y in coredata[i][0]], 
        [y[0] for y in coredata[i][0]], 
        label=coredata[i][1], 
        color=coredata[i][2]
    )
    for y in coredata[i][0]:
        plt.annotate(y[2], # this is the text
                    (y[1],y[0]), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(10,10) if coredata[i][2] != "blue" else (0,10) , # distance from text to points (x,y)
                    ha='center',
                    fontsize=12)

plt.title("Comparing Cost and Performance Across # of Cores")
plt.xlabel("Runtime (s)")
plt.ylabel("Cost ($)")
plt.legend()
plt.show()