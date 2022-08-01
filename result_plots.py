import json
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 4)
for i in range(6, 7):
    for j in range(0, 30):
        json_file = open("file_{}/fistness_history_test_{}.json".format(i, j))

        json_obj = json.load(json_file)

        history = json_obj["history"]

        plt.plot(history)

optimal = [117726 for i in range(0, 200)]

plt.plot(optimal, color='r', linestyle='--')
plt.ylabel('Fitness value', fontsize=13)
plt.xlabel('Generation', fontsize=13)
plt.grid(linestyle="--")
plt.title("Best chromosome fitness - Instance 1")
plt.savefig("fitness_x_generation_file_6.png", bbox_inches="tight")
plt.show()