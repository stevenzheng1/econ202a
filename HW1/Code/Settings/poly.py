from Settings import *


def PolyBasis(X,Y):
    ''' 
    Polynomial basis functions, using 2nd order polynomial

    Inputs
    X   n x 1 points for X
    Y   n x 1 points for Y

    Outputs
    B   n x 6 array of basis functions: 1, X, Y, X^2, X*Y, Y^2
    '''

    if Y.isna().all():
        B = np.column_stack((np.ones(len(X)),
                             X,
                             np.power(X,2)))
    else:
        B = np.column_stack((np.ones(len(X)),
                            X,
                            Y,
                            np.power(X,2),
                            np.multiply(X,Y),
                            np.power(Y,2)))

    return(B)


def PolyGetCoef(X,Y,Z):
    '''
    Fits the polynomial from PolyBasis to the function(s) in column(s) of Z, where
        Z=log(X+Y)
    
    Inputs
    X   n x 1 points for X
    Y   n x 1 points for Y
    Z   n x 1 values for function at (X,Y)

    Outputs
    b   6 x 1 basis coefficients
    '''
       
    B = PolyBasis(X=X,
                  Y=Y)
    #BT = B.T
    #b = ((np.linalg.inv((BT @ B)) @ BT) @ Z)
    b = sm.OLS(endog=Z,
               exog=B)\
           .fit()\
           .params\
           .values

    return(b)


def PolyApprox(X,Y,b):
    '''
    Returns an approximation of Z using X, Y and b. X,Y and b not necessarily from the same
    data. E.g., X,Y are from the "evaluation" data and b from the "training" data.
    '''

    ## Training B
    B = PolyBasis(X=X,
                  Y=Y)

    ## Evaluation
    Z_hat = np.dot(B,b)

    return(Z_hat)