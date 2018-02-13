import numpy as np

R = np.array([[2., 2.],
              [2., 2.]])

V = np.array([[1., 1.]])  # k=1
U = np.array([[1.],
              [1.]])  # k=1
mu = 1
beta=.001


B = np.where(R > 0, 1, 0)
L = np.multiply((np.subtract(R, np.dot(U, V))), B)

Vt = np.transpose(V)
m1 = np.dot(-2, L)
m2 = np.dot(m1, Vt)
m3 = np.dot(2, mu)
m4 = np.dot(m3, U)
dU = np.add(m2, m4)

U = np.subtract(U, np.dot(beta, dU))

print (U)
