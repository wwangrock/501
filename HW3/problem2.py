import numpy as np
import math
#-------------------------------------------------------------------------
'''
    Problem 2: optimization-based recommender systems
    In this problem, you will implement a version of the recommender system using optimization-based method.
    You could test the correctness of your code by typing `nosetests test2.py` in the terminal.
'''

#--------------------------
def update_U(R, V, U, beta=.001, mu=1.):
    '''
        Update the matrix U (movie factors) by fixing matrix V using gradient descent. 
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0. 
            V: the user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users. 
            U: the current item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            beta: step parameter for gradient descent, a float scalar 
            mu: the parameter for regularization term, a float scalar 
        Output:
            U: the updated item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
    '''

    #########################################
    ## INSERT YOUR CODE HERE
    B = np.where(R > 0, 1, 0)
    L = np.multiply((np.subtract(R, np.dot(U, V))), B)

    Vt = np.transpose(V)
    m1 = np.dot(-2, L)
    m2 = np.dot(m1, Vt)
    m3 = np.dot(2, mu)
    m4 = np.dot(m3, U)
    dU = np.add(m2, m4)

    U = np.subtract(U, np.dot(beta, dU))
    #########################################
    return U

#--------------------------
def update_V(R, U, V, beta=.001, mu=1.):
    '''
        Update the matrix V (user factors) by fixing matrix U using gradient descent. 
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0. 
            U: the item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            V: the current user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users. 
            beta: step parameter for gradient descent, a float scalar 
            mu: the parameter for regularization term, a float scalar 
        Output:
            V: the updated item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    B = np.where(R > 0, 1, 0)
    L = np.multiply((np.subtract(R, np.dot(U, V))), B)

    Ut = np.transpose(U)
    m1 = np.dot(-2, Ut)
    m2 = np.dot(m1, L)
    m3 = np.dot(2, mu)
    m4 = np.dot(m3, V)
    dV = np.add(m2, m4)

    V = np.subtract(U, np.dot(beta, dV))
    #########################################
    return V 
 

#--------------------------
def matrix_decoposition(R, k=5, max_steps=1000000, beta=.01, mu=.01):
    '''
        Compute the matrix decomposition for optimization-based recommender system.  
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0. 
            k: the number of latent factors for users and items.
            max_steps: the maximium number of steps for gradient descent.
            beta: step parameter for gradient descent, a float scalar 
        Output:
            U: the item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            V: the user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users. 
    '''
    
    # initialize U and V with random values
    n_movies, n_users = R.shape
    U = np.random.rand(n_movies, k)
    V = np.random.rand(k, n_users)
    
    # gradient descent
    for _ in xrange(max_steps): 
        # fix U, update V
        U_new = update_U(R, V, U, beta, mu)
        # fix V, update U
        V_new = update_V(R, U, V, beta, mu)
        if np.allclose(U_new, U) and np.allclose(V_new,  V):
            break
        else:
            U = U_new
            V = V_new
    return U, V 


