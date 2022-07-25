import json
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm


def calculate_fitness(croma, items_profit):
    profit = 0
    item = 0
    for bit in croma:
        if bit == '1':
            profit += items_profit[item]
        item += 1

    return profit


def roulette_selection(parents_pool, population_size):
    roulette = []

    new_parents = []

    while len(new_parents) < population_size:
        for parent in parents_pool:
            slot_size = int(parent["fitness"] * 10)

            for i in range(0, slot_size):
                roulette.append({"id": parent["id"], "fitness": parent["fitness"]})

        selected = random.randrange(0, len(roulette))

        new_parents.append(roulette[selected])

    return new_parents


def crossover(parent1, parent2, weights, capacities):
    position = random.randrange(0, 100)

    new_parent1 = parent1[0:position] + parent2[position:len(parent2)]
    new_parent2 = parent2[0:position] + parent1[position:len(parent1)]

    new_parent1 = validate_cromo(new_parent1, weights, capacities)
    new_parent2 = validate_cromo(new_parent2, weights, capacities)

    return new_parent1, new_parent2


def mutation(parent1, parent2, mutation_param, weights, capacities):
    for i in range(0, len(parent1)):
        if random.randrange(0, 100) < mutation_param + 1:
            if parent1[i] == '1':
                parent1 = parent1[:i] + '0' + parent1[i + 1:]
            else:
                parent1 = parent1[:i] + '1' + parent1[i + 1:]

    parent1 = validate_cromo(parent1, weights, capacities)
    parent2 = validate_cromo(parent2, weights, capacities)
    return parent1, parent2


def read_file(path):
    file = open(path)
    lines = file.readlines()

    count = 0
    for line in lines:
        count += 1
        print(f'line {count}: {line}')


def validate_cromo(croma, weights, capacities):
    for slot in range(0, 5):
        current_weight = 0
        item = 0
        for bit in croma:
            print(item)
            print(slot)
            print("bit = {}".format(bit))
            if bit == '1':
                print(weights)
                print(weights[slot][item])
                current_weight += weights[slot][item]
            item += 1
        while current_weight > capacities[slot]:
            random_item = random.randrange(0, 100)
            if croma[random_item] == '1':
                croma = croma[0:random_item] + '0' + croma[random_item + 1:100]
                current_weight -= weights[slot][random_item]
    return croma


def my_AG(population_size, number_of_generations, crossover_param, mutation_param, file_name):
    random.seed(55)
    population = {}
    population[0] = []
    best_fitness = {"history": []}

    for generation in range(0, number_of_generations):
        print("----------------------------------------------------------------------------------------------")
        print("Generation", generation)
        print("----------------------------------------------------------------------------------------------")

        population[generation + 1] = []

        items_profit = [504, 803, 667, 1103, 834, 585, 811, 856, 690, 832, 846, 813, 868, 793, 825, 1002, 860, 615, 540,
                        797, 616, 660, 707, 866, 647, 746, 1006, 608, 877, 900, 573, 788, 484, 853, 942, 630, 591, 630,
                        640, 1169, 932, 1034, 957, 798, 669, 625, 467, 1051, 552, 717, 654, 388, 559, 555, 1104, 783,
                        959, 668, 507, 855, 986, 831, 821, 825, 868, 852, 832, 828, 799, 686, 510, 671, 575, 740, 510,
                        675, 996, 636, 826, 1022, 1140, 654, 909, 799, 1162, 653, 814, 625, 599, 476, 767, 954, 906,
                        904, 649, 873, 565, 853, 1008, 632]

        weights = {0: [], 1: [], 2: [], 3: [], 4: []}

        capacities = {0: 11927, 1: 13727, 2: 11551, 3: 13056, 4: 13460}

        if not generation:
            # READ INSTANCE (ONLY FIRST INSTANCE)
            # read_file(path="instances/mknapcb1.txt")

            weights[0] = [42, 41, 523, 215, 819, 551, 69, 193, 582, 375, 367, 478, 162, 898, 550, 553, 298, 577, 493,
                          183, 260, 224, 852, 394, 958, 282, 402, 604, 164, 308, 218, 61, 273, 772, 191, 117, 276,
                          877, 415, 873, 902, 465, 320, 870, 244, 781, 86, 622, 665, 155, 680, 101, 665, 227, 597,
                          354, 597, 79, 162, 998, 849, 136, 112, 751, 735, 884, 71, 449, 266, 420, 797, 945, 746, 46,
                          44, 545, 882, 72, 383, 714, 987, 183, 731, 301, 718, 91, 109, 567, 708, 507, 983, 808, 766,
                          615, 554, 282, 995, 946, 651, 298]

            weights[1] = [509, 883, 229, 569, 706, 639, 114, 727, 491, 481, 681, 948, 687, 941, 350, 253, 573, 40,
                          124, 384, 660, 951, 739, 329, 146, 593, 658, 816, 638, 717, 779, 289, 430, 851, 937, 289,
                          159, 260, 930, 248, 656, 833, 892, 60, 278, 741, 297, 967, 86, 249, 354, 614, 836, 290, 893,
                          857, 158, 869, 206, 504, 799, 758, 431, 580, 780, 788, 583, 641, 32, 653, 252, 709, 129,
                          368, 440, 314, 287, 854, 460, 594, 512, 239, 719, 751, 708, 670, 269, 832, 137, 356, 960,
                          651, 398, 893, 407, 477, 552, 805, 881, 850]

            weights[2] = [806, 361, 199, 781, 596, 669, 957, 358, 259, 888, 319, 751, 275, 177, 883, 749, 229, 265,
                          282, 694, 819, 77, 190, 551, 140, 442, 867, 283, 137, 359, 445, 58, 440, 192, 485, 744, 844,
                          969, 50, 833, 57, 877, 482, 732, 968, 113, 486, 710, 439, 747, 174, 260, 877, 474, 841, 422,
                          280, 684, 330, 910, 791, 322, 404, 403, 519, 148, 948, 414, 894, 147, 73, 297, 97, 651, 380,
                          67, 582, 973, 143, 732, 624, 518, 847, 113, 382, 97, 905, 398, 859, 4, 142, 110, 11, 213,
                          398, 173, 106, 331, 254, 447]

            weights[3] = [404, 197, 817, 1000, 44, 307, 39, 659, 46, 334, 448, 599, 931, 776, 263, 980, 807, 378, 278,
                          841, 700, 210, 542, 636, 388, 129, 203, 110, 817, 502, 657, 804, 662, 989, 585, 645, 113,
                          436, 610, 948, 919, 115, 967, 13, 445, 449, 740, 592, 327, 167, 368, 335, 179, 909, 825,
                          614, 987, 350, 179, 415, 821, 525, 774, 283, 427, 275, 659, 392, 73, 896, 68, 982, 697, 421,
                          246, 672, 649, 731, 191, 514, 983, 886, 95, 846, 689, 206, 417, 14, 735, 267, 822, 977, 302,
                          687, 118, 990, 323, 993, 525, 322]

            weights[4] = [475, 36, 287, 577, 45, 700, 803, 654, 196, 844, 657, 387, 518, 143, 515, 335, 942, 701, 332,
                          803, 265, 922, 908, 139, 995, 845, 487, 100, 447, 653, 649, 738, 424, 475, 425, 926, 795,
                          47, 136, 801, 904, 740, 768, 460, 76, 660, 500, 915, 897, 25, 716, 557, 72, 696, 653, 933,
                          420, 582, 810, 861, 758, 647, 237, 631, 271, 91, 75, 756, 409, 440, 483, 336, 765, 637, 981,
                          980, 202, 35, 594, 689, 602, 76, 767, 693, 893, 160, 785, 311, 417, 748, 375, 362, 617, 553,
                          474, 915, 457, 261, 350, 635]

            for i in range(0, population_size):
                new_cromo = ""
                for bit in range(0, 100):
                    coin = random.randrange(0, 2)
                    if coin:
                        new_cromo += '1'
                    else:
                        new_cromo += '0'

                new_cromo = validate_cromo(new_cromo, weights, capacities)

                population[generation].append({"id": new_cromo, "fitness": calculate_fitness(new_cromo, items_profit)})

        value = 0

        for cromo in population[generation]:
            if cromo["fitness"] > value:
                value = cromo["fitness"]
                best_cromo = cromo
        print("BEST CROMO FITNESS", best_cromo["fitness"])
        best_fitness["history"].append(best_cromo["fitness"])

        parents_pool = population[generation]

        selected_parents = roulette_selection(parents_pool, population_size)

        it = 0

        while it < len(selected_parents):
            parent1 = selected_parents[it]
            it += 1
            parent2 = selected_parents[it]

            if random.randrange(0, 100) < crossover_param + 1:
                parent1["id"], parent2["id"] = crossover(parent1["id"], parent2["id"], weights, capacities)

            parent1["id"], parent2["id"] = mutation(parent1["id"], parent2["id"], mutation_param, weights, capacities)

            population[generation + 1].append({"id": parent1["id"], "fitness": calculate_fitness(parent1["id"],
                                                                                                 items_profit)})
            population[generation + 1].append({"id": parent2["id"], "fitness": calculate_fitness(parent2["id"],
                                                                                                 items_profit)})
            it += 1

        index_out = random.randrange(0, len(population[generation + 1]))
        population[generation + 1][index_out] = best_cromo

        print(best_cromo)
        generation += 1
    fitness_file = open("fistness_history_{}.json".format(file_name), "w")
    json.dump(best_fitness, fitness_file)
    return population


if __name__ == '__main__':
    file_name = str(input())
    all_population = my_AG(population_size=20,
                           number_of_generations=20,
                           crossover_param=75,
                           mutation_param=1,
                           file_name=file_name)

    # x = []
    # y = []
    # z = []
    # c = []
    #
    # for generation in all_population:
    #     for croma in all_population[generation]:
    #         c.append(generation)
    #         x.append((int(croma["id"][0:22], 2) * (200 / (2 ** 22 - 1))) - 100)
    #         y.append((int(croma["id"][22:44], 2) * (200 / (2 ** 22 - 1))) - 100)
    #         z.append(croma["fitness"])
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.scatter(x, y, z, c=c, cmap=cm.coolwarm, marker='o')
    #
    # plt.savefig("GA_F6.png")
    #
    # # plt.colorbar(label="Generation", orientation="horizontal", c=c, cmap=cm.coolwarm)
    # plt.show()

    # (100 - 40) BEST CROMO FITNESS 0.9999993979950594
    # (10 - 400) BEST CROMO FITNESS 0.9999999988619942
