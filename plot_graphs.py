import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import time

def get_array_parallel(fname):
    line_proc_end = []
    line_proc_alg = []

    temp_line_1 = []
    temp_line_2 = []

    temp_p_count = 0
    temp_line_count = 0

    with open(fname, 'r') as f:
        for line in f:       
            if line[0]=='P':
                v = line.split(' ')
                n_proc = int(v[1])
                n_line = int(v[3])
                n_feat = int(v[5])
                if n_proc != temp_p_count:
                    temp_p_count = n_proc
                    if len(temp_line_1) != 0:
                        line_proc_end.append(temp_line_1)
                    if len(temp_line_2) != 0:
                        line_proc_alg.append(temp_line_2)
                    temp_line_1 = []
                    temp_line_2 = []
                    
            elif line[0]=='\n':
                continue
            else:
                v = line.split(',')
                temp_line_1.append(float(v[1])*1e-9 + float(v[0]))
                temp_line_2.append(float(v[3])*1e-9 + float(v[2]))

    if len(temp_line_1) != 0:
        line_proc_end.append(temp_line_1)

    if len(temp_line_2) != 0:
        line_proc_alg.append(temp_line_2)

    line_proc_alg = np.array(line_proc_alg)
    line_proc_end = np.array(line_proc_end)
    return line_proc_alg, line_proc_end

def get_array_serial(fname):
    line_proc_end = []
    line_proc_alg = []

    temp_line_1 = []
    temp_line_2 = []

    temp_line_count = 0

    with open(fname, 'r') as f:
        for line in f:       
            if line[0]=='N':
                v = line.split(' ')
                n_line = int(v[1])
                n_feat = int(v[3])
                    
            elif line[0]=='\n':
                continue
            
            else:
                v = line.split(',')
                temp_line_1.append(float(v[1])*1e-9 + float(v[0]))
                temp_line_2.append(float(v[3])*1e-9 + float(v[2]))

    if len(temp_line_1) != 0:
        line_proc_end.append(temp_line_1)

    if len(temp_line_2) != 0:
        line_proc_alg.append(temp_line_2)

    line_proc_alg = np.array(line_proc_alg)
    line_proc_end = np.array(line_proc_end)
    return line_proc_alg, line_proc_end

line_proc_alg_dynamic, line_proc_end_dynamic = get_array_parallel('output_file_parallel_dynamic.txt')
line_proc_alg_guided, line_proc_end_guided = get_array_parallel('output_file_parallel_guided.txt')
line_proc_alg_normal, line_proc_end_normal = get_array_parallel('output_file_parallel_normal.txt')
line_proc_alg_static, line_proc_end_static = get_array_parallel('output_file_parallel_static.txt')
line_proc_alg_serial, line_proc_end_serial = get_array_serial('output_file_serial.txt')

# Time Curve
def time_curve(line_proc_alg, fname):
    plt.figure(figsize=(30, 30))
    problem_size = [2**i for i in range(2, 10)]
    plt.plot(problem_size, line_proc_end_serial[0, :])
    for i in range(line_proc_alg.shape[0]):
        plt.plot(problem_size, line_proc_alg[i, :])
    plt.xlabel('Problem Size')
    plt.ylabel('Time')
    plt.legend([f'No Processors : {i}' for i in range(17)])
    plt.savefig(f'plots_outer/time/{fname}.png')

time_curve(line_proc_alg_dynamic, 'dynamic')
time_curve(line_proc_alg_guided, 'guided')
time_curve(line_proc_alg_normal, 'normal')
time_curve(line_proc_alg_static, 'static')

# Time Curve
def speedup_curve(line_proc_alg, fname):
    plt.figure(figsize=(30, 30))
    problem_size = [2**i for i in range(2, 10)]
    res = [xj / xi for xi, xj in zip(line_proc_alg_serial[0, :], line_proc_alg_serial[0, :])]
    plt.plot(problem_size, res)
    for i in range(line_proc_alg.shape[0]):
        res = [xj / xi for xi, xj in zip(line_proc_alg[i, :], line_proc_alg_serial[0, :])]
        plt.plot(problem_size, res)
    plt.xlabel('Problem Size')
    plt.ylabel('Speedup')
    plt.legend([f'No Processors : {i}' for i in range(17)])
    plt.savefig(f'plots_outer/speedup/{fname}.png')

speedup_curve(line_proc_alg_dynamic, 'dynamic')
speedup_curve(line_proc_alg_guided, 'guided')
speedup_curve(line_proc_alg_normal, 'normal')
speedup_curve(line_proc_alg_static, 'static')
