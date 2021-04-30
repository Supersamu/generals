import numpy as np
import pandas as pd
import itertools
from queue import PriorityQueue


def calc_score(own_strat, others_strat):
    return np.sum(own_strat > others_strat)


def change_to_random_new_strat(old_strat):
    from_army = None
    while from_army is None:
        from_army = np.random.randint(0, 6)
        if old_strat[from_army] == 0:
            from_army = None
    to_army = None
    while to_army is None:
        to_army = np.random.randint(0, 6)
        if to_army == from_army:
            to_army = None
    new_strat = np.copy(old_strat)
    new_strat[from_army] -= 1
    new_strat[to_army] += 1
    return new_strat

x = pd.read_csv(r'generals.csv')
orig_strats = x.to_numpy()

starting_strats = np.copy(orig_strats)
indices = list(range(20))
cutoff_scores = [200, 265, 270, 275]
cutoff_scores.append([275]*16)
dict_for_cutoff_score = dict(zip(indices, cutoff_scores))
for _ in range(4):
    cutoff_score = dict_for_cutoff_score[_]
    print(len(starting_strats))
    print('iteration ' + str(_))
    set_of_strats_as_tuples = set()
    for strat in starting_strats:
        perms = list(set(itertools.permutations(tuple(strat))))
        set_of_strats_as_tuples.update(perms)
    list_of_strats_as_tuples = list(set_of_strats_as_tuples)
    best_strats = PriorityQueue()
    total_strats = 0
    for strat_as_tuple in list_of_strats_as_tuples:
        strat_as_array = np.asarray(strat_as_tuple)
        score = calc_score(strat_as_array, orig_strats)
        if score > cutoff_score:
            best_strats.put((-score, strat_as_tuple))
            total_strats += 1
    print('total strats to look at = ' + str(total_strats))
    starting_strats = set()
    strat_counter = 0
    for _ in range(best_strats._qsize()):  # all from the priority queue
        if strat_counter % 100 == 0:
            print('looking at strat ' + str(strat_counter))
        x = best_strats.get()
        strat_as_tuple = x[1]
        for l in range(3):  # different number of explorations
            new_strat = np.asarray(strat_as_tuple)
            best_new_strat = None
            for k in range(5 + l*10):  # different number of initial random changes to the strat
                new_strat = change_to_random_new_strat(new_strat)
            current_score = calc_score(new_strat, orig_strats)
            for j in range(100):  # greedy algorithm to search better strat
                old_strat = np.copy(new_strat)
                new_strat = change_to_random_new_strat(new_strat)
                new_score = calc_score(new_strat, orig_strats)
                if new_score > current_score:
                    best_new_strat = new_strat
                    current_score = new_score
                else:
                    new_strat = old_strat
            if best_new_strat is not None and current_score > cutoff_score:
                starting_strats.add(tuple(best_new_strat))
        strat_counter += 1

set_of_strats_as_tuples = set()
for strat in starting_strats:
    perms = list(set(itertools.permutations(tuple(strat))))
    set_of_strats_as_tuples.update(perms)
list_of_strats_as_tuples = list(set_of_strats_as_tuples)

best_strats = PriorityQueue()

for strat_as_tuple in list_of_strats_as_tuples:
    strat_as_array = np.asarray(strat_as_tuple)
    score = calc_score(strat_as_array, orig_strats)
    best_strats.put((-score, strat_as_tuple))

for i in range(10):
    x = best_strats.get()
    score = - x[0]
    strat_as_tuple = x[1]
    print(score, strat_as_tuple)