import json
import matplotlib.pyplot as plt

file = 9

plt.rcParams["figure.figsize"] = (10, 4)
for i in range(file, file+1):
    for j in range(0, 30):
        json_file = open("file_{}/fistness_history_test_{}.json".format(i, j))

        json_obj = json.load(json_file)

        history = json_obj["history"]

        plt.plot(history)

optimal_value = [24381, 59312, 120130, 23064, 59187, 117726, 21946, 56693, 115868]
optimal = [optimal_value[file-1] for i in range(0, 500)]

plt.plot(optimal, color='r', linestyle='--')
plt.ylabel('Fitness (#)', fontsize=13)
plt.xlabel('Generation', fontsize=13)
plt.grid(linestyle="--")
plt.title("Best chromosome fitness - Instance 1", fontsize=13)
plt.savefig("fitness_x_generation_file_{}.png".format(file), bbox_inches="tight")
plt.show()