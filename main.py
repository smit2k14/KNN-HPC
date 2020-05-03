#!/usr/bin/python
import os

N_LINES = [4, 8, 16, 32, 64, 128, 256, 512]
N_FEATURES = [4, 8, 16, 32, 64, 128, 256, 512]

print "Making serial outfile file"
os.system('touch output_file_serial.txt')
 
with open('output_file_serial.txt', 'w') as f:
    f.write("")

print "Compiling serial code =>"
os.system('gcc serial_measurement.c -fopenmp -lm -o serial')

print "Running serial code =>"
for n_lines in N_LINES:        
    with open('output_file_serial.txt', 'a') as f:    
        f.write('\n\nNumber of lines: ' + str(n_lines) + ' Number of features: ' + str(n_lines)+'\n\n')
    print "Running serial code for N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
    os.system('./serial '+str(n_lines)+' '+str(n_lines))
    print("-------------------------------")

print "========================================="
print "Serial done. Will do normal parallel now!"
print "========================================="

print "Making parallel output file"
os.system('touch output_file_parallel.txt')

with open('output_file_parallel.txt', 'w') as f:
    f.write("")

print "Compiling parallel code =>"
os.system('gcc parallel_measurement.c -fopenmp -lm -o parallel')

print "Running parallel code now =>"
for p in range(1, 17):
    for n_lines in N_LINES:
        with open("output_file_parallel.txt", "a") as f:
            f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_lines)+"\n\n")
        print "Running parallel code: for N_Processors: " + str(p) + " N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
        os.system('./parallel '+str(p)+' '+str(n_lines)+' '+str(n_lines))
        print("-------------------------------")
    with open('output_file_parallel.txt', 'a') as f:
        f.write('\n\n')

print "=================================================="
print "Normal parallel done. Will do static parallel now!"
print "=================================================="

print "Making parallel static output file"
os.system('touch output_file_parallel_static.txt')

with open('output_file_parallel_static.txt', 'w') as f:
    f.write("")

print "Compiling static parallel code =>"
os.system('gcc parallel_measurement_static.c -fopenmp -lm -o parallel_static')

print "Running static parallel code now =>"
for p in range(1, 17):
    for n_lines in N_LINES:
        with open("output_file_parallel_static.txt", "a") as f:
            f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_lines)+"\n\n")
        print "Running parallel code: for N_Processors: " + str(p) + " N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
        os.system('./parallel_static '+str(p)+' '+str(n_lines)+' '+str(n_lines))
        print("-------------------------------")
    with open('output_file_parallel_static.txt', 'a') as f:
        f.write('\n\n')

print "=================================================="
print "Static parallel done. Will do guided parallel now!"
print "=================================================="

print "Making parallel guided output file"
os.system('touch output_file_parallel_guided.txt')

with open('output_file_parallel_guided.txt', 'w') as f:
    f.write("")

print "Compiling guided parallel code =>"
os.system('gcc parallel_measurement_guided.c -fopenmp -lm -o parallel_guided')

print "Running guided parallel code now =>"
for p in range(1, 17):
    for n_lines in N_LINES:
        with open("output_file_parallel_guided.txt", "a") as f:
            f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_lines)+"\n\n")
        print "Running parallel code: for N_Processors: " + str(p) + " N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
        os.system('./parallel_guided '+str(p)+' '+str(n_lines)+' '+str(n_lines))
        print("-------------------------------")
    with open('output_file_parallel_guided.txt', 'a') as f:
        f.write('\n\n')

print "================================================="
print "Guided parallel done. Will do dynamic parallel now!"
print "================================================="

print "Making parallel dynamic output file"
os.system('touch output_file_parallel_dynamic.txt')

with open('output_file_parallel_dynamic.txt', 'w') as f:
    f.write("")

print "Compiling dynamic parallel code =>"
os.system('gcc parallel_measurement_dynamic.c -fopenmp -lm -o parallel_dynamic')

print "Running dynamic parallel code now =>"
for p in range(1, 17):
    for n_lines in N_LINES:
        with open("output_file_parallel_dynamic.txt", "a") as f:
            f.write("Processors: "+str(p)+" N_LINES: "+str(n_lines)+" N_FEATURES: "+str(n_lines)+"\n\n")
        print "Running parallel code: for N_Processors: " + str(p) + " N_Lines: " + str(n_lines) + " N_Features: " + str(n_lines)
        os.system('./parallel_dynamic '+str(p)+' '+str(n_lines)+' '+str(n_lines))
        print("-------------------------------")
    with open('output_file_parallel_dynamic.txt', 'a') as f:
        f.write('\n\n')
