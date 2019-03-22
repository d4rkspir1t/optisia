import numpy as np
import pprint


def make_population(onoff_switches, multi_switches, pop_size, algo, forth_onoff, forth_multi):
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

        if algo == 'Forth':
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


def artificial_selection(select_ratio=0.2):
    pass


def mutation():
    pass


def cross_breeding():
    pass
