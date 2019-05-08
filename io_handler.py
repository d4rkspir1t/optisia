import csv
import os
import shutil

extension_map = {'COSIATEC': '.cos',
                 'SIATECCompress': '.SIATECCompress',
                 'Forth': '.Forth',
                 'RecurSIA': '.RecurSIA'}


def parse_samples(path=''):
    pieces = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            pieces.append(os.path.join(root, name))
    return pieces


def log_times(path, t_type, time, gen, idx):
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            header = ['timed', 'gen', 'idx', 'min', 'sec']
            writer.writerow(header)
            c_min, c_sec = divmod(time, 60)

            c_min_str = '%02d' % c_min
            c_sec_str = '%.3f' % c_sec
            line = [t_type, gen, idx, c_min_str, c_sec_str]
            writer.writerow(line)
    else:
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            c_min, c_sec = divmod(time, 60)

            c_min_str = '%02d' % c_min
            c_sec_str = '%.3f' % c_sec
            line = [t_type, gen, idx, c_min_str, c_sec_str]
            writer.writerow(line)


def save_param_fitnesses(path_fitness, gen, param_fitness_dict, param_table):
    if not os.path.exists(path_fitness):
        with open(path_fitness, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            header = ['generation', 'idx', 'fitness']
            for x in range(0, len(param_table[0])):
                header.append('param%d' % x)
            writer.writerow(header)
            for idx, fit in enumerate(param_fitness_dict):
                line = [str(gen), str(idx), str(fit)]
                for param in param_table[idx]:
                    line.append(param)
                writer.writerow(line)
    else:
        with open(path_fitness, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for idx, fit in enumerate(param_fitness_dict):
                line = [str(gen), str(idx), str(fit)]
                for param in param_table[idx]:
                    line.append(param)
                writer.writerow(line)


def read_compression_from_file(f_path):
    with open(f_path) as f:
        for line in f:
            if 'compressionRatio' in line:
                cr_str = line.split(' ')[1]
                cr_float = float(cr_str)
                print(cr_float)
                return cr_float


def get_path_for_results(base_path, algorithm):
    extension = extension_map[algorithm]
    for item in os.listdir(base_path):
        new_path = os.path.join(base_path, item)
        if os.path.isdir(new_path):
            for file in os.listdir(new_path):
                file_path = os.path.join(new_path, file)
                if extension == os.path.splitext(file)[1]:
                    compression_ratio = read_compression_from_file(file_path)
                    shutil.rmtree(new_path)
                    # exit(417)
                    return compression_ratio
            exit(999)
