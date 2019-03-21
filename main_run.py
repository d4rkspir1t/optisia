import argparse
import numpy as np
import os
import pprint
import time

import gene_handler as gh
from jar_handler import JarCall
from switch_handler import Switches


def parse_samples(path=''):
    pieces = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            pieces.append(os.path.join(root, name))
    return pieces


def get_fitness_for_generation(chromosomes):
    param_fitnesses = {}
    for member in chromosomes:
        params = [member['recalg'],
                  member['d'],
                  member['rrt']]

        if member['ct'] != '':
            params.extend([member['ct'],
                           switch_mngr.ct_min_comp_prefix,
                           member['cta'],
                           switch_mngr.ct_max_comp_prefix,
                           member['ctb']
                           ])
        else:
            params.extend([member['ct'],
                           '',  # ct_min_comp_prefix
                           '',  # cta
                           '',  # ct_max_comp_prefix
                           ''])  # ctb

        if member['rsd'] != '':
            params.extend([member['rsd'],
                           switch_mngr.r_count_prefix,
                           member['r']])
        else:
            params.extend([member['rsd'],
                           '',  # r_count_prefix
                           ''])  # r

        call_args = [switch_mngr.algorithm_prefix,
                     switch_mngr.algorithm,
                     switch_mngr.input_file_prefix,
                     switch_mngr.input_file]

        call_args.extend(params)
        filtered_call_args = []
        for param in call_args:
            if param != '':
                filtered_call_args.append(param)
        print((len(filtered_call_args)))
        print('<' * 100)
        caller = JarCall('omnisia3.jar')
        fitness = caller.make_call(filtered_call_args)
        param_fitnesses[params] = fitness
    pprint.pprint(param_fitnesses)
    return param_fitnesses


def get_compression_from_output(file=''):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=str, default="COSIATEC",
                        help="Base algorithm to start the evolution with.")
    parser.add_argument("--data", type=str, default="Fugues",
                        help="Base algorithm to start the evolution with.")
    # parser.add_argument("--port", type=int, default=9559,
    #                     help="Naoqi port number")
    # parser.add_argument("--plot", action="store_true",
    #                     help="Plotting recorded variable lists")
    args = parser.parse_args()

    population_size = 50

    pieces = parse_samples(os.path.join('samples', args.data))
    elapsed_times = []
    all_start = time.time()

    for piece in pieces:
        start_t = time.time()
        print('Evolving for piece: %s' % piece)
        print('#' * 50)
        # >>>>>
        switch_mngr = Switches(str(args.base), piece)

        onoff_switches = {'recalg': switch_mngr.recursia,
                          'd': switch_mngr.pitch,
                          'ct': switch_mngr.comp_trawler,
                          'rsd': switch_mngr.r_superdiags,
                          'rrt': switch_mngr.rrt}

        multi_switches = {'cta': switch_mngr.ct_min_comp,
                          'ctb': switch_mngr.ct_max_comp,
                          'r': switch_mngr.r_count}

        if args.base == 'Forth':
            forth_onoff_sw = {'bbcomp': switch_mngr.bbcomp}
            forth_multi_sw = {'crlow': switch_mngr.crlow,
                              'comlow': switch_mngr.comlow,
                              'cmin': switch_mngr.cmin}

        artificially_selected = []
        chromosomes = gh.make_population(onoff_switches, multi_switches, population_size)

        param_fitness_dict = get_fitness_for_generation(chromosomes)

    print('\n')
    print('#' * 50)
    print('#' * 50, '\n')
    print('Tested: %d' % len(elapsed_times))
    print('Time outline: avg: %.5f, min: %.5f, max: %.5f' %
          (np.average(elapsed_times), min(elapsed_times), max(elapsed_times)))
    print('\nAll time passed: %.3f' % (time.time()-all_start))
