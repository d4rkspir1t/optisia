import numpy as np
import pprint
from numpy import random


def make_population(onoff_switches, multi_switches, pop_size, algo, recalgo, forth_onoff, forth_multi):
    population = []
    while len(population) != pop_size:
        chromosome = {}
        rng = np.random.randint(2, size=len(onoff_switches.values()))
        for idx, (key, switch) in enumerate(onoff_switches.items()):
            chromosome[key] = switch[rng[idx]]

        if chromosome['ct'] != '':
            i = np.random.random_integers(0, 3)
            chromosome['cta'] = multi_switches['cta'][i]
            i = np.random.random_integers(0, 2)
            chromosome['ctb'] = multi_switches['ctb'][i]
        if chromosome['rsd'] != '':
            i = np.random.random_integers(0, 2)
            chromosome['r'] = multi_switches['r'][i]

        if algo == 'Forth' or recalgo == 'Forth':
            i = np.random.random_integers(0, 1)
            chromosome['bbcomp'] = forth_onoff['bbcomp'][i]
            i = np.random.random_integers(0, 2)
            chromosome['crlow'] = forth_multi['crlow'][i]
            i = np.random.random_integers(0, 2)
            chromosome['comlow'] = forth_multi['comlow'][i]
            i = np.random.random_integers(0, 3)
            chromosome['cmin'] = forth_multi['cmin'][i]
        if chromosome not in population:
            population.append(chromosome)
    pprint.pprint(population)
    print('-' * 50)

    return population


def artificial_selection(fitnesses, param_table, select_ratio=0.4):
    cut = int(len(fitnesses)*select_ratio)
    we_happy_few = [i[0] for i in sorted(enumerate(fitnesses), key=lambda x:x[1])][-cut:]
    kept_params = {}
    for idx in we_happy_few:
        kept_params[idx] = param_table[idx]
    # print(we_happy_few)
    # pprint.pprint(kept_params)
    return kept_params


def mutation(child, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo):
    mutation_idx = random.randint(0, len(child)-1)
    keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
    key = keys[mutation_idx]
    if key in onoff_switches.keys():
        i = np.random.random_integers(0, 1)
        prev_value = child[mutation_idx]
        child[mutation_idx] = onoff_switches[key][i]
        if prev_value != child[mutation_idx]:
            if child[2] != '':
                i = np.random.random_integers(0, 3)
                child[3] = multi_switches['cta'][i]
                i = np.random.random_integers(0, 2)
                child[4] = multi_switches['ctb'][i]
            if child[5] != '':
                i = np.random.random_integers(0, 2)
                child[6] = multi_switches['r'][i]
    elif key in multi_switches.keys():
        if child[2] != '':
            if mutation_idx == 3:
                i = np.random.random_integers(0, 3)
                child[mutation_idx] = multi_switches[key][i]
            if mutation_idx == 4:
                i = np.random.random_integers(0, 2)
                child[mutation_idx] = multi_switches[key][i]
        if child[5] != '':
            if mutation_idx == 6:
                i = np.random.random_integers(0, 2)
                child[mutation_idx] = multi_switches[key][i]
    elif key in forth_onoff_sw.keys():
        i = np.random.random_integers(0, 1)
        child[mutation_idx] = forth_onoff_sw[key][i]
    elif key in forth_multi_sw.keys():
        if key != 'cmin':
            i = np.random.random_integers(0, 2)
            child[mutation_idx] = forth_multi_sw[key][i]
        else:
            i = np.random.random_integers(0, 3)
            child[mutation_idx] = forth_multi_sw[key][i]
    return child


def breed(male_mrna, female_mrna, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo):
    male_trna = [male_mrna[0],
                 male_mrna[1],
                 male_mrna[2],
                 male_mrna[4],
                 male_mrna[6],
                 male_mrna[7],
                 male_mrna[9],
                 male_mrna[11],
                 male_mrna[15],
                 male_mrna[19],
                 male_mrna[20]]
    female_trna = [female_mrna[0],
                   female_mrna[1],
                   female_mrna[2],
                   female_mrna[4],
                   female_mrna[6],
                   female_mrna[7],
                   female_mrna[9],
                   female_mrna[11],
                   female_mrna[15],
                   female_mrna[19],
                   female_mrna[20]]
    children = []
    for _ in range(2):
        child = []
        for param in range(0, len(male_trna)):
            child.append(random.choice([female_trna[param],
                                        male_trna[param]]))
        # mutate child
        mut_child = mutation(child, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo)
        # make FULL param dict out of it
        keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
        child_member = {}
        for idx, key in enumerate(keys):
            child_member[key] = mut_child[idx]
        children.append(child_member)
    return children


def cross_breeding(happy_few, population_size, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo):
    parent_count = len(happy_few.values())
    need = population_size-parent_count
    print(happy_few)
    print('P count %d, need %d' % (parent_count, need))
    population = []
    for idx, params in enumerate(happy_few.values()):
        keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
        real_params = [params[0],
                       params[1],
                       params[2],
                       params[4],
                       params[6],
                       params[7],
                       params[9],
                       params[11],
                       params[15],
                       params[19],
                       params[20]]
        member = {}
        for idx, key in enumerate(keys):
            member[key] = real_params[idx]
        population.append(member)
    while len(population) != need:
        male = random.randint(0, parent_count-1)
        male_key = list(happy_few.keys())[male]
        female = random.randint(0, parent_count-1)
        female_key = list(happy_few.keys())[female]
        if male != female:
            male_mrna = happy_few[male_key]
            female_mrna = happy_few[female_key]
            children = breed(male_mrna, female_mrna, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo)
            for child in children:
                if child not in population:
                    population.append(child)
            print(len(population))
    return population
