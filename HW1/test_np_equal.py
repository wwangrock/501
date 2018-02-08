from problem3 import *
import numpy as np

P = np.mat([[ 0. ,  0.5,  1. ],
            [ 0.5,  0. ,  0. ],
            [ 0.5,  0.5,  0. ]] )

P1 = np.mat([[ 0. ,  0.5,  1. ],
            [ 0.5,  0. ,  0. ],
            [ 0.5,  0.5,  0. ]] )

if (P == P1).all():
    print("yes")
else:
    print("no")
