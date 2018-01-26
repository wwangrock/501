from problem1 import *
import numpy as np
#-------------------------------------------------------------------------
'''
    Problem 2:
    In this problem, you will use the Elo rating algorithm in problem 1 to rank the NCAA teams.
    You could test the correctness of your code by typing `nosetests test2.py` in the terminal.
'''

#--------------------------
def import_W(filename ='ncaa_results.csv'):
    '''
        import the matrix W of game results from a CSV file
        Input:
                filename: the name of csv file, a string
        Output:
                W: the game result matrix, a numpy integer matrix of shape (n by 2)
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    W = np.loadtxt(filename, delimiter = ",",dtype = 'int')
    #W = np.matrix(A)
    #########################################
    return W

#--------------------------
def import_team_names(filename ='ncaa_teams.txt'):
    '''
        import a list of team names from a txt file. Each line of text in the file is a team name.
        Input:
                filename: the name of txt file, a string
        Output:
                team_names: the list of team names, a python list of string values, such as ['team a', 'team b','team c'].
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    team_names = content
    #########################################
    return team_names

W = import_W('ncaa_results2.csv')
AW = [[1, 0], # Game1: player 1 wins player 0
     [2, 1], # Game2: player 2 wins player 1
     [3, 0]] # Game3: player 3 wins player 0
W2 = list(W)
N = import_team_names('ncaa_teams.txt')
#print(len(N))
teams = list()
A = elo_rating(W, 8)
B = sorted(A, reverse = True)
C = sorted(range(len(A)),reverse = True,key=lambda x:A[x])
for i in C:
    teams.append(N[i])
print (A)
print (B)
print (C)
print(teams)
