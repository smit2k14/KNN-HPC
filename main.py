#!/usr/bin/python

import os

N_LINES = 10000
N_FEATURES = [4, 8, 16, 32, 64, 128]
print "Making serial outfile file"
os.system('touch output_file_serial.txt')
    
with open('output_file_serial.txt', 'w') as f:
    f.write("")

print "Will start serial code now: "

for n_features in N_FEATURES:
    print "Generating features for: " + str(n_features) + "and lines: " + str(N_LINES)
    os.system('python generate_data.py ' + str(N_LINES) + ' ' + str(n_features))
    print "Compiling serial code: "
    os.system('g++ -std=c++11 serial_measurement.cpp -fopenmp -o serial')
    print "Running serial code: "
    os.system('./serial data_file.txt')

print "Making parallel output file"
os.system('touch output_file_parallel.txt')

with open('output_file_parallel.txt', 'w') as f:
    f.write("")

for p in range(1, 3):
    
    #with open("output_file_parallel.txt", "a") as f:
    #    f.write("Processors: "+str(p)+"\n")
    for n_features in N_FEATURES:
        print "Generating features for: " + str(n_features) + " and lines: " + str(N_LINES) + " and processors: " + str(p)
        os.system('python generate_data.py '+str(N_LINES)+' '+str(n_features))
        print "Compiling parallel code: "
        os.system('g++ -std=c++11 parallel_measurement.cpp -fopenmp -o parallel')
        print "Running parallel code: "
        os.system('./parallel '+str(p)+' data_file.txt')
    with open('output_file_parallel.txt', 'a') as f:
        f.write('\n\n\n')


