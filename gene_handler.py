import numpy as np
import pprint
from numpy import random


def make_population(onoff_switches, multi_switches, pop_size, algo, recalgo, forth_onoff, forth_multi):
    population = []
    retry_count = 0
    while len(population) != pop_size:
        chromosome = {}
        rng = np.random.randint(2, size=len(onoff_switches.values()))
        for idx, (key, switch) in enumerate(onoff_switches.items()):
            chromosome[key] = switch[rng[idx]]

        if chromosome['ct'] != '':
            i = np.random.random_integers(0, 2)
            chromosome['cta'] = multi_switches['cta'][i]
            i = np.random.random_integers(0, 3)
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
            i = np.random.random_integers(0, 2)
            chromosome['cmin'] = forth_multi['cmin'][i]
        if chromosome not in population and retry_count != 50:
            population.append(chromosome)
            retry_count = 0
        else:
            retry_count += 1
    pprint.pprint(population)
    print('-' * 50)

    return population


def artificial_selection(fitnesses, param_table, select_ratio=0.34):
    cut = int(len(fitnesses)*select_ratio)
    we_happy_few = [i[0] for i in sorted(enumerate(fitnesses), key=lambda x:x[1])][-cut:]
    kept_params = {}
    for idx in we_happy_few:
        kept_params[idx] = param_table[idx]
    # print(we_happy_few)
    # pprint.pprint(kept_params)
    return kept_params


def mutation(child, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo):
    if algo == 'Forth' or recalgo == 'Forth':
        keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
    else:
        keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r']
    mutation_chance = (1/(len(keys)))*100
    print('Mutation chance: ', mutation_chance)
    for mut_idx, key in enumerate(keys):
        if np.random.random_integers(1, 100) <= mutation_chance:
            if key in onoff_switches.keys():
                print('ONOFF KEY %s' % key)
                i = np.random.random_integers(0, 1)
                child[mut_idx] = onoff_switches[key][i]
            elif key in multi_switches.keys():
                if child[2] != '':
                    if mut_idx == 3:
                        i = np.random.random_integers(0, 2)
                        child[mut_idx] = multi_switches[key][i]
                    if mut_idx == 4:
                        i = np.random.random_integers(0, 3)
                        child[mut_idx] = multi_switches[key][i]
                if child[5] != '':
                    if mut_idx == 6:
                        i = np.random.random_integers(0, 2)
                        child[mut_idx] = multi_switches[key][i]
            elif key in forth_onoff_sw.keys():
                i = np.random.random_integers(0, 1)
                child[mut_idx] = forth_onoff_sw[key][i]
            elif key in forth_multi_sw.keys():
                    i = np.random.random_integers(0, 2)
                    child[mut_idx] = forth_multi_sw[key][i]
    return child


def breed(male_mrna, female_mrna, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo):
    if algo == 'Forth' or recalgo == 'Forth':
        idx_for_trna = [0, 1, 2, 4, 6, 7, 9, 11, 15, 19, 20]
    else:
        idx_for_trna = [0, 1, 2, 4, 6, 7, 9]

    male_trna = [male_mrna[idx] for idx in idx_for_trna]
    female_trna = [female_mrna[idx] for idx in idx_for_trna]

    children = []
    for _ in range(4):  # TODO: make it a variable that depends on the needed amount and the starting parent count
        child = []
        for param in range(0, len(male_trna)):
            child.append(random.choice([female_trna[param],
                                        male_trna[param]]))
        # mutate child
        mut_child = mutation(child, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo)
        # make FULL param dict out of it
        if algo == 'Forth' or recalgo == 'Forth':
            keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
        else:
            keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r']
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
        if algo == 'Forth' or recalgo == 'Forth':
            keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r', 'crlow', 'comlow', 'cmin', 'bbcomp']
            idx_for_params = [0, 1, 2, 4, 6, 7, 9, 11, 15, 19, 20]
        else:
            keys = ['d', 'rrt', 'ct', 'cta', 'ctb', 'rsd', 'r']
            idx_for_params = [0, 1, 2, 4, 6, 7, 9]
        real_params = [params[idx] for idx in idx_for_params]

        member = {}
        for idx, key in enumerate(keys):
            member[key] = real_params[idx]
        population.append(member)
    print('Parents added: pop - %d' % len(population))
    retry_count = 0

    while len(population) != population_size and parent_count >= 2:
        remove_parents = False
        male = random.randint(0, parent_count-1)
        female = random.randint(0, parent_count-1)
        print('Parents selected')

        if male == female:
            if male != 0:
                male = male-1
            else:
                male = male+1

        male_key = list(happy_few.keys())[male]
        female_key = list(happy_few.keys())[female]
        male_mrna = happy_few[male_key]
        female_mrna = happy_few[female_key]
        children = breed(male_mrna, female_mrna, onoff_switches, multi_switches, forth_onoff_sw, forth_multi_sw, algo, recalgo)
        for child in children:
            if len(population) != population_size:
                population.append(child)
                remove_parents = True
        if remove_parents:
            del happy_few[male_key]
            del happy_few[female_key]
            parent_count = len(happy_few.values())
        print('Population length %d' % len(population))
    for member in population:
        if member['rsd'] == '-rsd' and member['r'] == '':
            i = np.random.random_integers(0, 2)
            member['r'] = multi_switches['r'][i]
            print('Preventive R generation')
        if member['ct'] == '-ct' and member['cta'] == '':
            i = np.random.random_integers(0, 2)
            member['cta'] = multi_switches['cta'][i]
            print('Preventive CTA generation')
        if member['ct'] == '-ct' and member['ctb'] == '':
            i = np.random.random_integers(0, 3)
            member['ctb'] = multi_switches['ctb'][i]
            print('Preventive CTB generation')
    return population
