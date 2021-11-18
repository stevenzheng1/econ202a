from Settings import *

def Simulate(Par,bAp,Mode,T):
    '''
    Simulates the model.

    Inputs:
    Par     parameter dict
    bAp     Polynominal coefficients
    Mode    'random' to draw shocks, 'irf' for impulse response function
    T       number of draws
    '''

    ## Set up
    A = np.zeros(T)
    logY = np.zeros(T)
    C = np.zeros(T)

    ## Start at steady state
    A[0] = Par['A_bar']

    if Mode=='irf':
        logY[0] = Par['sigma']
        Eps = np.zeros(T)

    if Mode=='random':
        logY[0] = np.log(Par['mu'])
        Eps = Par['sigma'] * np.random.normal(loc=0,scale=1,size=T)

    for t in range(1,T):
        A[t] = np.dot(PolyBasis(X=A[t-1],
                                Y=np.exp(logY[t-1]),
                                scalar='yes'),
                      bAp)
        logY[t] = (1.0-Par['rho']) * np.log(Par['mu']) +\
                   Par['rho']*logY[t-1] + Eps[t]
        C[t-1] = np.exp(logY[t-1]) + A[t-1] - \
                 np.power(A[t]/Par['Z'],1.0/Par['alpha'])

    ## Compute quantities from state variables
    Ti = range(1,T-1)
    A = A[Ti]
    logY = logY[Ti]
    C = C[Ti]

    ## Out
    Sim = {'A':A,
           'logY':logY,
           'C':C}
    return(Sim)