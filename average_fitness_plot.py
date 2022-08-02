import json
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = (10, 4)

average_instance = []

for i in range(1, 7):
    average = 0
    for j in range(0, 30):
        json_file = open("file_{}/fistness_history_test_{}.json".format(i, j))

        json_obj = json.load(json_file)

        history = json_obj["history"]

        average += history[len(history)-1]
    average_instance.append(int(average/30))

print(average_instance)

# plt.plot(average_instance)

# optimal = [24381, 59312, 120130, 23064, 59187, 117726]

X = ['File 1', 'File 2', 'File 3', 'File 4', 'File 5', "File 6"]
Y_optimal = [24381, 59312, 120130, 23064, 59187, 117726]
Y_GA = average_instance

X_axis = np.arange(len(X))

plt.bar(X_axis - 0.2, Y_GA, 0.4, label='Average Fitness', color="royalblue")
plt.bar(X_axis + 0.2, Y_optimal, 0.4, label='Optimal value', color='firebrick')

plt.xticks(X_axis, X)
plt.xlabel("Instances", fontsize=13)
plt.ylabel("Average fitness (#)", fontsize=13)
plt.title("Best chromosomes fitness average", fontsize=13)
plt.legend()
plt.savefig("best_chromo_fitness_average.png", bbox_inches="tight")
plt.show()