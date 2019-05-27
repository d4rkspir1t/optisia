import argparse
from datetime import datetime
import numpy as np
import os
import time

import gene_handler as gh
import io_handler as ioh
from jar_handler import JarCall
from switch_handler import Switches

tested_params = []
tested_param_compression = {}


def get_fitness_for_generation(chromosomes, folder, algo, recalgo, path_time_log, gen):
    param_fitnesses = []
    param_table = {}
    table_idx = 0
    for member in chromosomes:
        start_t_chrom = time.time()
        params = [member['d'],
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

        if algo == 'Forth' or recalgo == 'Forth':
            forth_params = [switch_mngr.crlow_prefix,
                            member['crlow'],
                            switch_mngr.crhi_1,
                            switch_mngr.crhi_2,
                            switch_mngr.comlow_prefix,
                            member['comlow'],
                            switch_mngr.comhi_1,
                            switch_mngr.comhi_2,
                            switch_mngr.cmin_prefix,
                            member['cmin'],
                            member['bbcomp']]
            params.extend(forth_params)

        call_args = [switch_mngr.algorithm_prefix,
                     switch_mngr.algorithm,
                     switch_mngr.recursia,
                     switch_mngr.recalg_alg,
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
        if filtered_call_args not in tested_params:
            tested_params.append(filtered_call_args)
            caller.make_call(filtered_call_args)

            compression_ratio = ioh.get_path_for_results(folder, algo)
            tested_param_compression[tested_params.index(filtered_call_args)] = compression_ratio
            print('CACHING CALL AND CALCULATED COMPRESSION RATIO')
        else:
            print('READING CACHED CR. INSTEAD')
            compression_ratio = tested_param_compression[tested_params.index(filtered_call_args)]

        param_table[table_idx] = params
        param_fitnesses.append(compression_ratio)
        table_idx += 1

        elapsed_time_chrom = time.time()-start_t_chrom
        ioh.log_times(path_time_log, 'chrom', elapsed_time_chrom, gen, str(table_idx-1))

    return param_fitnesses, param_table


def check_stagnation(param_fit_dict, best_fit):
    stagnating = True
    for fitness in param_fit_dict:
        if fitness > best_fit:
            best_fit = fitness
            stagnating = False
            break
    return best_fit, stagnating


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=str, default="COSIATEC",
                        help="Base algorithm to start the evolution with.")
    parser.add_argument("--recalg", type=str, default="COSIATEC",
                        help="Base algorithm to start the evolution with.")
    parser.add_argument("--data", type=str, default="Fugues",
                        help="Base algorithm to start the evolution with.")
    parser.add_argument("--pop", type=int, default=50,
                        help="Population size")
    parser.add_argument("--gen", type=int, default=100,
                        help="Generation count")
    parser.add_argument("--sta", type=int, default=50,
                        help="Generation count")
    parser.add_argument("--stac", type=int, default=30,
                        help="Generation count")
    parser.add_argument("--sel", type=float, default="0.34",
                        help="Artificial selection cutoff on each generation.")
    args = parser.parse_args()

    population_size = args.pop
    folder_path = os.path.join('samples', args.data)
    pieces = ioh.parse_samples(folder_path)
    elapsed_times = []
    all_start = time.time()

    for piece in pieces:
        start_t_piece = time.time()
        print('Evolving for piece: %s' % piece)
        print('#' * 50)

        switch_mngr = Switches(str(args.base), piece, str(args.recalg))

        onoff_switches = {'d': switch_mngr.pitch,
                          'ct': switch_mngr.comp_trawler,
                          'rsd': switch_mngr.r_superdiags,
                          'rrt': switch_mngr.rrt}

        multi_switches = {'cta': switch_mngr.ct_min_comp,
                          'ctb': switch_mngr.ct_max_comp,
                          'r': switch_mngr.r_count}

        if args.base == 'Forth' or args.recalg == 'Forth':
            forth_onoff_sw = {'bbcomp': switch_mngr.bbcomp}
            forth_multi_sw = {'crlow': switch_mngr.crlow,
                              'comlow': switch_mngr.comlow,
                              'cmin': switch_mngr.cmin}
        else:
            forth_onoff_sw = {}
            forth_multi_sw = {}

        chromosomes = gh.make_population(onoff_switches, multi_switches, population_size,
                                         args.base, args.recalg, forth_onoff_sw, forth_multi_sw)

        ts = datetime.now().strftime('%d%m%y%H%M%S')
        pn = os.path.basename(piece).split('.')[0]
        path_file_name_format = '%s%s-%s-%s-%s' % (args.base, args.recalg, args.data, pn, ts)
        path_time_log = os.path.join('results', path_file_name_format + '.log')
        path_fitness = os.path.join('results', path_file_name_format + '.csv')

        best_fitness = 0
        stagnating_for_count = 0
        for generation in range(1, args.gen+1):
            start_t_gen = time.time()

            param_fitness_dict, param_table = get_fitness_for_generation(chromosomes, folder_path, args.base,
                                                                         args.recalg, path_time_log, str(generation))
            ioh.save_param_fitnesses(path_fitness, generation, param_fitness_dict, param_table)
            happy_few = gh.artificial_selection(param_fitness_dict, param_table, args.sel)
            chromosomes = gh.cross_breeding(happy_few, population_size, onoff_switches, multi_switches, forth_onoff_sw,
                                            forth_multi_sw, args.base, args.recalg)

            elapsed_time_gen = time.time()-start_t_gen
            ioh.log_times(path_time_log, 'gen', elapsed_time_gen, str(generation), '')

            best_fitness, stagnating_pop = check_stagnation(param_fitness_dict, best_fitness)
            if stagnating_pop and generation > args.sta:
                if stagnating_for_count < args.stac:
                    stagnating_for_count += 1
                else:
                    print('POPULATION CEASED TO GET BETTER')
                    break

        elapsed_time_piece = time.time()-start_t_piece
        ioh.log_times(path_time_log, 'piece', elapsed_time_piece, '', '')
        print('\n'*20)

        tested_params = []
        tested_param_compression = {}
        elapsed_times.append(elapsed_time_piece)
        # exit(417)

    print('\n')
    print('#' * 50)
    print('#' * 50, '\n')
    print('Tested: %d' % len(elapsed_times))
    print('Time outline: avg: %.5f, min: %.5f, max: %.5f' %
          (np.average(elapsed_times), min(elapsed_times), max(elapsed_times)))
    print('\nAll time passed: %.3f' % (time.time()-all_start))
