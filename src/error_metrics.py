import numpy as np


# Given numpy-like input vectors x and y, compute mean square error
def RMSE(x,y):
    return np.sqrt( np.sum( np.square(x-y) ) )

# Computes the maximal element difference (L_inf)
def Linf(x,y):
    return np.max( np.absolute( x-y ) )

# Computes the average of absolute differences (L_1)
def L1(x,y):
    return np.average( np.absolute( x-y ) )
