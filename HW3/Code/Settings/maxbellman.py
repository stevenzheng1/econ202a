from Settings import *

def MaxBellman(Par,b,Grid,MAXIT=1000):
    '''
    Maximizes the RHS of the Bellman equation using golden
    section search.

    Inputs:
    Par     parameter dict
    b       6x1 coefficeints in polynomial
    Grid    grid dict
    MAXIT   max number of iterations
    e       convergence epsilon

    Outputs:
    V       nx1 value function
    Ap      nx1 vector of time t+1 savings A_t+1 or A'
    '''

    ## Golden ratio
    p = (np.sqrt(5.0)-1.0)/2.0

    ## Subintervals
    ## Note, we have -1e10 to have positive consumption
    A = Grid['LB_A'] * np.ones(len(Grid['AA']))

    D_1 = Par['Z'] * np.power(np.exp(Grid['logYY'])+Grid['AA'],
                              Par['alpha']) \
          - 1e-10
    D_2 = Grid['A'][-1] * np.ones(len(D_1))
    D = np.minimum(D_1,D_2)

    B = p*A + (1-p)*D
    C = (1.0-p)*A + p*D
    fB = Bellman(Par=Par,
                 b=b,
                 A=Grid['AA'],
                 logY=Grid['logYY'],
                 Ap=B)
    fC = Bellman(Par=Par,
                 b=b,
                 A=Grid['AA'],
                 logY=Grid['logYY'],
                 Ap=C)
    
    ## Loop
    for it_inner in range(0,MAXIT):
        if np.max(D-A)<1e-6:
            break
            
        I = fB>fC

        D[I] = C[I]
        C[I] = B[I]
        fC[I] = fB[I]
        B[I] = p*C[I] + (1-p)*A[I]
        fB[I] = Bellman(Par=Par,
                        b=b,
                        A=Grid['AA'][I],
                        logY=Grid['logYY'][I],
                        Ap=B[I])

        A[~I] = B[~I]
        B[~I] = C[~I]
        fB[~I] = fC[~I]
        C[~I] = p*B[~I] + (1-p)*D[~I]
        fC[~I] = Bellman(Par=Par,
                         b=b,
                         A=Grid['AA'][~I],
                         logY=Grid['logYY'][~I],
                         Ap=C[~I])

    ## At this stage, A, B, C, and D are all within a small epsilon
    ## of one another. We will use the average of B and C as the 
    ## optimal level of savings.
    Ap = (B+C)/2.0

    ## Evaluate the Bellman equation at the optimal policy to find the
    ## new value function
    V = Bellman(Par=Par,
                b=b,
                A=Grid['AA'],
                logY=Grid['logYY'],
                Ap=Ap)

    ## Out
    return(V,Ap)