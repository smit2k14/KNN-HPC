import os

N_LINES = 10000
N_FEATURES = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
os.system('touch output_file_serial.txt')
    
for n_features in N_FEATURES:
    os.system('python generate_data.py '+str(N_LINES)+' '+str(n_features))
    os.system('g++ -std=c++11 serial_measurement.cpp -fopenmp -o serial')
    os.system('./serial data_file.txt')

os.system('touch output_file_parallel.txt')
for p in range(1, 5):    
    for n_features in N_FEATURES:
        os.system('python generate_data.py '+str(N_LINES)+' '+str(n_features))
        os.system('g++ -std=c++11 parallel_measurement.cpp -fopenmp -o parallel')
        os.system('./parallel '+str(p)+' data_file.txt')
    with open('output_file_parallel.txt', 'a') as f:
        f.write('\n\n\n')


