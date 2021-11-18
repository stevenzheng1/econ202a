from Settings import *

def Bellman(Par,b,A,logY,Ap):
    '''
    Evaluate the RHS of the Bellman equation.

    Inputs:
    Par     parameter dict
    b       6x1 coefficeints in polynomial
    A       nx1 vector of time t savings A_t
    Y       nx1 vector of output Y_t
    Ap      nx1 vector of time t+1 savings A_t+1 or A'

    Outputs:
    V   nx1 value function

    Copied from Alisdair McKay's matlab code.
    '''
    
    ## Consumption
    C = np.exp(logY) + A - np.power(Ap/Par['Z'],1/Par['alpha'])
    
    ## Utility
    u = np.power(C,1.0-Par['gamma']) / (1.0-Par['gamma'])

    ## Value function
    V = u + Par['beta']*np.dot(PolyBasis(X=Ap,Y=np.exp(logY)),b)

    ## Out
    return(V)
