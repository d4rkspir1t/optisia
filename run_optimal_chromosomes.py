# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:23:39 2019

@author: David Meredith
"""

import os
import re
import sys
import subprocess


def get_list_of_result_file_paths(optisia_results_directory):
    result_file_paths = []
    for root, dirs, files in os.walk(optisia_results_directory, topdown=False):
        for name in files:
            if name.endswith('.csv'):
                result_file_paths.append(os.path.join(root, name))
    return result_file_paths


def get_complexity(chromosome):
    return len([f for f in chromosome if f != ''])


def get_best_chromosome(csv_file_path):
    best_chromosome = []
    f = open(csv_file_path, 'r')
    f.readline()
    x = f.readline();
    best_chromosome = x.split(';')
    for l in f:
        a = l.split(';')
        #print(a)
        if int(a[0]) > int(best_chromosome[0]):
            #print ("  best " + a[0] + ">" + best_chromosome[0])
            best_chromosome = a
        elif int(a[0]) == int(best_chromosome[0]) and float(a[2]) > float(best_chromosome[2]):
            #print ("  best " + a[2] +">" + best_chromosome[2])
            best_chromosome = a
        elif int(a[0]) == int(best_chromosome[0]) and float(a[2]) == float(best_chromosome[2]) and get_complexity(a) < get_complexity(best_chromosome):
            #print ("  best " + str(get_complexity(a)) + "<" + str(get_complexity(best_chromosome)))
            best_chromosome = a
    return best_chromosome


def get_list_of_best_chromosomes(list_of_result_file_paths):
    best_chromosomes = []
    for file_path in list_of_result_file_paths:
        best_chromosomes.append(get_best_chromosome(file_path))
    return best_chromosomes


def call_omnisia_with_chromosome(result_file, chromosome, mode=""):
    #print('result_file is ', result_file)
    #print('chromosome is ', chromosome)
    if 'JKU-PDD' in result_file:
        test_subdir = "JKU-PDD"
        input_file_suffix = '.txt'
    elif 'Fugues' in result_file:
        test_subdir = "Fugues"
        input_file_suffix = '.opnd'
    elif 'NLB single' in result_file:
        test_subdir = "NLB individual files"
        input_file_suffix = '.mid'

    if 'COSIATEC' in result_file:
        algorithm = 'COSIATEC'
        output_file_suffix = '.cos'
    elif 'SIATECCompress' in result_file:
        algorithm = 'SIATECCompress'
        output_file_suffix = '.SIATECCompress'
    elif 'Forth' in result_file:
        algorithm = 'Forth'
        output_file_suffix = '.Forth'
    
    start = result_file.rfind(test_subdir) + len(test_subdir) + 1
    end = result_file.rfind('-')
    #print(start, end)
    input_file_name = result_file[start:end]
    
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
    
        
if __name__ == '__main__':
    list_of_result_file_paths = get_list_of_result_file_paths('results')
    #for path in list_of_result_file_paths:
    #    print(path)
    #print("best chromosome is " + str(get_best_chromosome(list_of_result_file_paths[0])))
    list_of_best_chromosomes = get_list_of_best_chromosomes(list_of_result_file_paths)
    result_chromosome_pairs = zip(list_of_result_file_paths,list_of_best_chromosomes)
    for result_file, chromosome in result_chromosome_pairs:
        print (result_file + ": " + str(chromosome))
        call_omnisia_with_chromosome(result_file, chromosome)
#        call_omnisia_with_chromosome(result_file, chromosome, '-bbmode')
#    print(get_best_chromosome('results\Fugues\Forth\Forth-Fugues-bwv864b-done-310319012301.csv'))
