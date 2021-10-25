from Settings import *

def logxy(X,Y):
    '''
    This is the function log(x+y).
    '''
    return(np.log(X+Y))

def fx(X):
    '''
    This is the piecewise function in part m.
    '''
    if X < 2:
        f=0
    if X >=2:
        f=np.sqrt(X-2.0)

    return(f)