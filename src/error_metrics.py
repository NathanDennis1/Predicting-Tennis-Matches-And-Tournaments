import numpy as np
import matplotlib.pyplot as plt

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


def barPlot(names, preds, actual):
    """ Plots a bar-plot comparing predicted probabilities to those
    obtained via betting odds.

    Input:
    names (list): list of names for each player
    preds (list): predicted probabilities
    actual (list): actual probabilities
    """
    # Create plots
    fig, ax = plt.subplots(figsize=(16,8), layout='constrained')
    bar_width = 0.4
    idx = np.arange(len(names))

    # Plot values
    b1 = ax.bar(idx,             preds, bar_width, label='Predictions')
    b2 = ax.bar(idx + bar_width, actual, bar_width, label='Actual')

    # Touch-up plot labels
    ax.set_title('Predicted Prob. vs. Betting Odds')
    ax.set_xlabel('Name')
    ax.set_ylabel('Probabilities')
    ax.set_xticks(idx + bar_width/2)
    ax.set_xticklabels(names, rotation=55)
    ax.legend()
    ax.grid(alpha=0.4)

    plt.show()


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
