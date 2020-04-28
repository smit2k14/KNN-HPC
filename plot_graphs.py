import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import time

line_proc_end = []
line_proc_alg = []

temp_line_1 = []
temp_line_2 = []

temp_p_count = 0
temp_line_count = 0

cnt1 = 0
cnt2 = 0

with open('output_file_parallel.txt', 'r') as f:
    for line in f:       
        if line[0]=='P':
            v = line.split(' ')
            n_proc = int(v[1])
            n_line = int(v[3])
            n_feat = int(v[5])
            if n_line != temp_line_count:
                print(n_proc, n_line, n_feat)
                temp_line_count = n_line
                if len(temp_line_1) != 0:
                    line_proc_end.append(temp_line_1)
                if len(temp_line_2) != 0:
                    line_proc_alg.append(temp_line_2)
                temp_line_1 = []
                temp_line_2 = []
            
        elif line[0]=='\n':
            continue
        else:
            cnt1 += 1
            v = line.split(',')
            temp_line_1.append(float(v[1])-float(v[0]))
            temp_line_2.append(float(v[3])-float(v[2]))

if len(temp_line_1) != 0:
    line_proc_end.append(temp_line_1)
if len(temp_line_2) != 0:
    line_proc_alg.append(temp_line_2)

t1 = []
t2 = []
for i in range(len(line_proc_alg)):
    t2.append(line_proc_alg[i])
    if (i+1)%8 == 0:
        t1.append(t2)
        t2 = []

line_proc_alg = np.array(t1)
print(line_proc_alg.shape)
t1 = []
t2 = []
for i in range(len(line_proc_end)):
    t2.append(line_proc_end[i])
    if (i+1)%8 == 0:
        t1.append(t2)
        t2 = []

line_proc_end = np.array(t1)
print(line_proc_end.shape)

with open('Alg.pkl', 'wb') as f:
    pickle.dump(line_proc_alg, f)

with open('End.pkl', 'wb') as f:
    pickle.dump(line_proc_end, f)

# (processor, line, feature)
temp = [4, 8, 16, 32, 64, 128, 256, 512]#, 1024, 2048]
for i in range(len(temp)):
    plt.figure(i+1, figsize = (20, 20))
    for j in range(8):
        plt.plot([_ for _ in range(1, 16)], line_proc_alg[:,i,j])
    plt.legend(['N_Features 4', 'N_Features number 8', 'N_Features number 16', 'N_Features number 32', 'N_Features number 64', \
        'N_Features number 128', 'N_Features number 256', 'N_Features number 512'])
    plt.title('N_Lines {}'.format(temp[i]))
    plt.xlabel('No of Processors')
    plt.ylabel('Time')
    plt.savefig('plots/line_'+str(i+1)+'.png')
