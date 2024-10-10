import numpy as np

# Each method takes in numpy-like input vectors x and y

# Compute mean square error
def RMSE(x,y):
    return np.sqrt( np.sum( np.square(x-y) ) )

# Computes the maximal element difference (L_inf)
def Linf(x,y):
    return np.max( np.absolute( x-y ) )

# Computes the average of absolute differences (L_1)
def L1(x,y):
    return np.average( np.absolute( x-y ) )


def displayErrors(preds, actual, display=True):
    """ Given prediction probabilities, returns all the above error metrics.

    Input:
    preds (array-like): predicted probabilities
    actual (array-like): probabilities (from betting odds)
    display (boolean): whether to directly display metrics
    Output:
    (double) (x3): RMSE, Linf, and L1 metrics
    """

    rmse = RMSE(preds, actual)
    linf = Linf(preds, actual)
    l1   = L1(preds, actual)

    if display:
        print("RMSE: {:0.3f} \nL_inf: {:0.3f}\nL_1: {:0.3f}".format(rmse, linf, l1))
    
    return rmse, linf, l1
