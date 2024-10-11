import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error

# Each method takes in numpy-like input vectors x and y

class Errors():
    def __init__(self):
        pass

    # Compute mean square error
    def RMSE(self, x,y):
        return np.sqrt( np.mean( np.square(x-y) ) )

    # Computes the maximal element difference (L_inf)
    def Linf(self, x,y):
        return np.max( np.abs( x-y ) )

    # Computes the average of absolute differences (L_1)
    def L1(self, x,y):
        return np.mean( np.absolute( x-y ) )



    def displayErrors(self, tournament_name, display=True):
        """ Given prediction probabilities, returns all the above error metrics.

        Input:
        preds (array-like): predicted probabilities
        actual (array-like): probabilities (from betting odds)
        display (boolean): whether to directly display metrics
        Output:
        (double) (x3): RMSE, Linf, and L1 metrics
        """

        tournament_name = tournament_name.replace(' ', '_')
        odds = pd.read_csv(f'../data/2023_{tournament_name}_Prob.csv', index_col=0)

        model = pd.read_csv(f'../data/tournament_results_{tournament_name}.csv', index_col = 0)

        odds_comparison = odds[['Normalized Winning Probability']].join(model['Champion'], how='inner')
        odds_comparison = odds_comparison.dropna()

        actual = odds_comparison['Normalized Winning Probability']

        preds = odds_comparison['Champion']
        rmse = self.RMSE(preds, actual)
        linf = self.Linf(preds, actual)
        l1 = self.L1(preds, actual)

        if display:
            print("RMSE: {:0.5f} \nL_inf: {:0.5f}\nL_1: {:0.5f}".format(rmse, linf, l1))
        
        return rmse
