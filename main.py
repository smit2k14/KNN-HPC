#!/usr/bin/python
import os

N_LINES = [4, 8, 16, 32, 64, 128, 256, 512]
N_FEATURES = [4, 8, 16, 32, 64, 128, 256, 512]

print "Making serial outfile file"
os.system('touch output_file_serial.txt')
 
with open('output_file_serial.txt', 'w') as f:
    f.write("")

print "Will start serial code now: "
for n_lines in N_LINES:        
    with open('output_file_serial.txt', 'a') as f:    
        f.write('\n\nNumber of lines: ' + str(n_lines) + ' Number of features: ' + str(n_lines)+'\n\n')
    print "Compiling serial code for N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
    os.system('gcc serial_measurement.c -fopenmp -lm -o serial')
    print "Running serial code: "
    os.system('./serial '+str(n_lines)+' '+str(n_lines))

print "Making parallel output file"
os.system('touch output_file_parallel.txt')

with open('output_file_parallel.txt', 'w') as f:
    f.write("")

for p in range(1, 5):
    for n_lines in N_LINES:
        with open("output_file_parallel.txt", "a") as f:
            f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_lines)+"\n\n")
        print "Compiling parallel code: for N_Processors: " + str(p) + " N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
        os.system('gcc parallel_measurement.c -fopenmp -lm -o parallel')
        print "Running parallel code: "
        os.system('./parallel '+str(p)+' '+str(n_lines)+' '+str(n_lines))
    with open('output_file_parallel.txt', 'a') as f:
        f.write('\n\n')


