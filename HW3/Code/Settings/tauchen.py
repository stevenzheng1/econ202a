from Settings import *

def tauchen(N,mu,rho,sigma,m):
    '''
    Purpose:    Finds a Markov chain whose sample paths
                approximate those of the AR(1) process
                z(t+1) = (1-rho)*mu + rho * z(t) + eps(t+1)
                where eps are normal with stddev sigma

    Format:     {Z, Zprob} = Tauchen(N,mu,rho,sigma,m)

    Input:      N       scalar, number of nodes for Z
                mu      scalar, unconditional mean of process
                rho     scalar
                sigma   scalar, std. dev. of epsilons
                m       max +- std. devs.

    Output:     Z       N*1 vector, nodes for Z
                Zprob   N*N matrix, transition probabilities

    Martin Floden
    Fall 1996

    This procedure is an implementation of George Tauchen's algorithm
    described in Ec. Letters 20 (1986) 177-181.

    Translated from Alisdair McKay's matlab code.
    '''

    Z = np.zeros(N)
    Zprob = np.zeros((N,N))
    a = (1.0-rho)*mu

    Z[-1] = m * np.sqrt(np.power(sigma,2) / (1.0-np.power(rho,2)))
    Z[0] = -Z[-1]
    zstep = (Z[-1] - Z[0]) / (N-1)

    for i in range(1,N-1):
        Z[i] = Z[0] + zstep * i

    Z = Z + a / (1.0-rho)

    for j in range(0,N):
        for k in range(0,N):
            if k==0:
                Zprob[j,k] = norm.cdf((Z[0] - a - rho*Z[j] + zstep/2.0) / sigma)
            elif k==N-1:
                Zprob[j,k] = 1.0 - norm.cdf((Z[-1] - a - rho*Z[j] - zstep/2.0) / sigma)
            else:
                Zprob[j,k] = norm.cdf((Z[k] - a - rho*Z[j] + zstep/2.0) / sigma) -\
                            norm.cdf((Z[k] - a - rho*Z[j] - zstep/2.0) / sigma)
                            
    return(Z,Zprob)