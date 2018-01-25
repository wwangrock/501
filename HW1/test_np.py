import numpy as np
from problem3 import random_walk,compute_P
from problem4 import compute_S
from problem5 import compute_G

A = np.mat( [ [0., 0.],
              [1., 0.]])

alpha = 0
S = compute_S(A)
L = np.asmatrix(np.ones((A.shape[0],A.shape[1]))) * 1/float(A.shape[0])
G = S * alpha + L * (1-alpha)

print(G)
