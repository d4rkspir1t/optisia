import numpy as np
import pprint


def make_population(onoff_switches, multi_switches, pop_size=100):
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
