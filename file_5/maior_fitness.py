import json

maior = 0

for i in range(0, 30):
    file = open("fistness_history_test_{}.json".format(i))
    json_obj = json.load(file)
    history = json_obj["history"]
    best = history[len(history)-1]
    if best > maior:
        maior = best

    print("FILE: {} | VALUE: {}".format(i, maior))