import os

N_LINES = 10000
N_FEATURES = [4, 8, 16, 32, 64, 128]
for n_features in N_FEATURES:
    os.system('touch output_file.txt')
    os.system('python generate_data.py '+str(N_LINES)+' '+str(n_features))
    os.system('g++ serial_measurement.cpp -fopenmp -o serial')
    os.system('./serial data_file.txt')

