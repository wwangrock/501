import numpy as np

#def compute_P(A):
    #c = 0
    #for i in A[0:1]:
        #print (i)
A = np.mat( [[0., 1., 1.],
             [1., 0., 0.],
             [1., 1., 0.],
             [2., 3., 4.]
             ])
#print(A.shape[0]) #number of rows
#print(A.shape[1]) #number of columns
#print(A[0:]) #all elements of row0
#print(A[:,1]) #all elements of column0


for x in range(A.shape[1]):
    n = 0
    for i in (A[:,x]):
        n = n + i;
    A[:,x] = A[:,x]/n
print(A)
