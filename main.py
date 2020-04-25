#!/usr/bin/python

import os

N_LINES = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
N_FEATURES = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
print "Making serial outfile file"
os.system('touch output_file_serial.txt')
    
with open('output_file_serial.txt', 'w') as f:
    f.write("")

print "Will start serial code now: "
for n_lines in N_LINES:
    for n_features in N_FEATURES:
        print "Generating features for: " + str(n_features) + " and lines: " + str(n_lines)
        os.system('python generate_data.py ' + str(n_lines) + ' ' + str(n_features))
        print "Compiling serial code: "
        os.system('g++ -std=c++11 serial_measurement.cpp -fopenmp -o serial')
        print "Running serial code: "
        os.system('./serial data_file.txt')

print "Making parallel output file"
os.system('touch output_file_parallel.txt')

with open('output_file_parallel.txt', 'w') as f:
    f.write("")

for p in range(1, 3):
    
    for n_lines in N_LINES:
        for n_features in N_FEATURES:
            
            with open("output_file_parallel.txt", "a") as f:
                f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_features)+"\n\n")
            print "Generating features for: " + str(n_features) + " and lines: " + str(N_LINES) + " and processors: " + str(p)
            os.system('python generate_data.py '+str(N_LINES)+' '+str(n_features))
            print "Compiling parallel code: "
            os.system('g++ -std=c++11 parallel_measurement.cpp -fopenmp -o parallel')
            print "Running parallel code: "
            os.system('./parallel '+str(p)+' data_file.txt')
        with open('output_file_parallel.txt', 'a') as f:
            f.write('\n\n\n')


