import random
import math
import sys

n_lines = int(sys.argv[1])
n_features = int(sys.argv[2])

with open('data_file.txt', 'w') as f:
    for i in range(n_lines):
        for j in range(n_features):
            f.write(str(random.random()))
            if j != n_features-1:
                f.write(',')
        f.write('\n')
    