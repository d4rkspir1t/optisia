# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:23:39 2019

@author: David Meredith
"""

import argparse
import os
import re
import sys
import subprocess


def get_list_of_result_file_paths(optisia_results_directory, p0, p1):
    result_file_paths = []
    for root, dirs, files in os.walk(optisia_results_directory, topdown=False):
        for name in files:
            if name.endswith('.csv') and (p0 in name or p1 in name):
                result_file_paths.append(os.path.join(root, name))
    print('RESULT FILE PATH LEN: ', len(result_file_paths))
    return result_file_paths


def get_complexity(chromosome):
    return len([f for f in chromosome if f != ''])


def get_best_chromosome(csv_file_path):
    chrom_list = []
    f = open(csv_file_path, 'r')
    f.readline()
    x = f.readline()
    best_chromosome = x.split(';')
    best_fitness = 0
    for l in f:
        a = l.split(';')
        fitness = float(a[2])
        if fitness > best_fitness:
            #print ("  best " + a[2] +">" + best_chromosome[2])
            chrom_list = []
            chrom_list.append(a)
            best_fitness = fitness
        elif fitness == best_fitness:
            chrom_list.append(a)
        # elif int(a[0]) == int(best_chromosome[0]) and float(a[2]) == float(best_chromosome[2]) and get_complexity(a) < get_complexity(best_chromosome):
        #     #print ("  best " + str(get_complexity(a)) + "<" + str(get_complexity(best_chromosome)))
        #     best_chromosome = a
    return chrom_list


def get_list_of_best_chromosomes(list_of_result_file_paths):
    candidate_chromosomes = {}
    best_chromosomes = {}
    res_path = ''
    for file_path in list_of_result_file_paths:
        if 'COSIATEC' in file_path:
            algorithm = 'COSIATEC'
        elif 'SIATECCompress' in file_path:
            algorithm = 'SIATECCompress'
        elif 'Forth' in file_path:
            algorithm = 'Forth'
        best_chroms = get_best_chromosome(file_path)
        if algorithm not in candidate_chromosomes.keys():
            candidate_chromosomes[algorithm] = []
        candidate_chromosomes[algorithm].append(best_chroms)
    for val in candidate_chromosomes.values():
        key_wise_best = []
        for chrom in val[0]:
            if chrom in val[1]:
                key_wise_best.append(chrom)
        if len(key_wise_best) == 0:
            least_complex = 100
            least_comp_chrom = None
            for chrom in val[0]:
                complexity = get_complexity(chrom)
                if complexity < least_complex:
                    least_complex = complexity
                    least_comp_chrom = chrom
            for chrom in val[1]:
                complexity = get_complexity(chrom)
                if complexity < least_complex:
                    least_complex = complexity
                    least_comp_chrom = chrom
            key_wise_best = least_comp_chrom
        else:
            for chrom in key_wise_best:
                least_complex = 100
                least_comp_chrom = None
                complexity = get_complexity(chrom)
                if complexity < least_complex:
                    least_complex = complexity
                    least_comp_chrom = chrom
            key_wise_best = least_comp_chrom
        # print('KEY\'s BEST: ', key_wise_best)
        best_chromosomes[algorithm] = key_wise_best
    print('BEST CHROM LENGTH: ', len(best_chromosomes.keys()))
        # best_chromosomes.append(get_best_chromosome(file_path))
    return best_chromosomes


def call_omnisia_with_chromosome(input_file_name, algo, chromosome, mode=""):
    test_subdir = "NLB pair files"
    input_file_suffix = '.opnd'

    if 'COSIATEC' in algo:
        algorithm = 'COSIATEC'
        output_file_suffix = '.cos'
    elif 'SIATECCompress' in algo:
        algorithm = 'SIATECCompress'
        output_file_suffix = '.SIATECCompress'
    elif 'Forth' in algo:
        algorithm = 'Forth'
        output_file_suffix = '.Forth'
    
    output_file_path = 'output\\' + test_subdir + '\\' + algorithm + mode + '\\' + input_file_name + output_file_suffix
    input_file_path = 'samples\\' + test_subdir + "\\" + input_file_name + input_file_suffix
    cmd_file_path = 'output\\' + test_subdir + '\\' + algorithm + mode + '\\' + input_file_name + '.log'
    cmd = ['java', '-jar', 'omnisia3.jar', mode, '-i', input_file_path, '-a', algorithm, '-out', output_file_path]
    cmd += chromosome[3:]
    cmd = [x for x in cmd if x != '']
    for idx, val in enumerate(cmd):
        if '\n' in val:
            param = re.sub('\\n', '', val)
            cmd[idx] = param
    print(cmd)
    with open(cmd_file_path, "w") as cmd_file:
        print(cmd, file=cmd_file)
    subprocess.call(cmd)


def parse_samples(path=''):
    pieces = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            pieces.append(os.path.join(root, name))
    return pieces


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="NLB pair files",
                        help="Base algorithm to start the evolution with.")
    # parser.add_argument("--plot", action="store_true",
    #                     help="Plotting recorded variable lists")
    args = parser.parse_args()
    folder_path = os.path.join('samples', args.data)
    pieces = parse_samples(folder_path)

    for piece in pieces:
        pn = os.path.basename(piece).split('.')[0]
        sub_pcs = pn.split('+')
        p0 = sub_pcs[0]
        p1 = sub_pcs[1]

        list_of_result_file_paths = get_list_of_result_file_paths('results', p0, p1)

        list_of_best_chromosomes = get_list_of_best_chromosomes(list_of_result_file_paths)

        for algo, chromosome in list_of_best_chromosomes.items():
            print (pn + ": " + str(chromosome))
            call_omnisia_with_chromosome(pn, algo, chromosome)
#        call_omnisia_with_chromosome(result_file, chromosome, '-bbmode')
#    print(get_best_chromosome('results\Fugues\Forth\Forth-Fugues-bwv864b-done-310319012301.csv'))
