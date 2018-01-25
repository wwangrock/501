import numpy as np

import math
#--------------------------
def compute_EA(RA, RB):
    '''
        compute the expected probability of player A to win in a game with player B.
        Input:
            RA: the rating of player A, a float scalar value
            RB: the rating of player B, a float scalar value
        Output:
            EA: the expected probability of A wins, a float scalar value between 0 and 1.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    EA = 1/(1+math.pow(10,(RB-RA)/400))
    #########################################
    return EA

#--------------------------
def update_RA(RA, SA, EA, K = 16.):
    '''
        compute the new rating of player A after playing a game.
        Input:
            RA: the current rating of player A, a float scalar value
            SA: the game result of player A, a float scalar value.
                if A wins in a game, SA = 1;if A loses, SA =0.
            EA: the expected probability of player A to win in the game, a float scalar between 0 and 1.
             K: k-factor, a contant number which controls how fast to correct the ratings
        Output:
            RA_new: the new rating of player A, a float scalar value
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    RA_new = RA + K*(SA-EA)
    #########################################
    return RA_new
#from problem1 import *

W = [[0, 1]]
R = 2 * [400.]
for (A,B) in W:
    EA = compute_EA(R[A],R[B])
    #EB = compute_EA(R[B],R[A])
    R[A] = update_RA(R[A],1,EA, K = 16.)
    #R[B] = update_RA(R[B],0,EB, K = 16.)
    #print(EA,EB)
print(R)
