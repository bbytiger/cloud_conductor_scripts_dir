import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(9, 8))

coredata = [
    ([
        (0.009965237234, 37.96685137, "AWS c5n2xlarge + AWS G5"), 
        (0.01017798953, 41.00190295, "AWS c42xlarge + AWS G5"), 
        (0.01025389365, 40.3723215, "AWS c5nxlarge + AWS G5"),
        (0.009434821218, 43.59394707, "AWS c4xlarge + AWS G5"),
        (0.006575725004, 48.90733035, "AWS c42xlarge + AWS G4")
    ], "AWS only", "orange"),
    ([
        (0.0205076998, 34.01508636, "GCP e2-standard-8 + GCP TPU"),
    ], "GCP only", "blue"),
    ([
        (0.009305491221, 37.0594932, "GCP e2-standard-8 + AWS G5"),
        (0.009148850984, 44.94551004, "GCP e2-standard-4 + AWS G5"),
    ], "GCP to AWS", "green"),
    ([
        (0.02163744581, 34.92244453, "AWS c5n2xlarge + GCP TPU"),
        (0.02185019811, 37.95749612, "AWS c42xlarge + GCP TPU"),
    ], "AWS to GCP", "red")
]

def create_offsets(label):
    if label == "GCP e2-standard-8 + GCP TPU":
        return (40,10)
    if label == "AWS c5n2xlarge + GCP TPU" or label == "AWS c42xlarge + GCP TPU":
        return (20, 10)
    if label == "AWS c5nxlarge + AWS G5":
        return (0, 20)
    if label == "AWS c42xlarge + AWS G4":
        return (-20, 10)
    else:
        return (0,10)

for i in range(4):
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
                    xytext=create_offsets(y[2]), # distance from text to points (x,y)
                    ha='center',
                    fontsize=12)

plt.title("Comparing Cost and Performance of MNIST Pipeline Across Clouds")
plt.xlabel("Runtime (s)")
plt.ylabel("Cost ($)")
plt.legend()
plt.show()