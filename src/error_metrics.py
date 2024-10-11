import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error

# Each method takes in numpy-like input vectors x and y

class Errors():
    def __init__(self):
        pass

    def RMSE(self, true, pred):
        """ 
        Calculates RMSE score

        Input:
            true (float): True value (betting odds probability)
            pred (float): Predicted value (model output probability)

        Return:
            RMSE score as a float
        """
        return np.sqrt(np.mean(np.square(true-pred)))

    def Linf(self, true, pred):
        """ 
        Calculates L-Infinity Norm score, the maximum absolute error between the true and predicted values.

        Input:
            true (float): True value (betting odds probability)
            pred (float): Predicted value (model output probability)

        Output:
            L-Infinity Norm score as a float
        """
        return np.max(np.abs(true-pred))

    def L1(self, true, pred):
        """ 
        Calculates L-1 Norm score, the average absolute difference between the true and predicted values

        Input:
            true (float): True value (betting odds probability)
            pred (float): Predicted value (model output probability)

        Output:
            L-1 Norm score as a float
        """
        return np.mean(np.absolute(true-pred))



    def displayErrors(self, tournament_name, display=True):
        """ 
        Given prediction probabilities, returns all the utilized error metrics including RMSE, L-Infinity Norm,
        and L-1 Norm.

        Input:
            tournament_name (str): Name of tennis tournament
            display (boolean): Display calculated error metric values, default is True.

        Output:
            (double) (x3): RMSE, Linf, and L1 metrics
        """

        tournament_name = tournament_name.replace(' ', '_')
        odds = pd.read_csv(f'../data/2023_{tournament_name}_Prob.csv', index_col=0)

        model = pd.read_csv(f'../data/tournament_results_{tournament_name}.csv', index_col = 0)

        odds_comparison = odds[['normalized_winning_probability']].join(model['Champion'], how='inner')
        odds_comparison = odds_comparison.dropna()

        actual = odds_comparison['normalized_winning_probability']

        preds = odds_comparison['Champion']
        rmse = self.RMSE(preds, actual)
        linf = self.Linf(preds, actual)
        l1 = self.L1(preds, actual)

        if display:
            print("RMSE: {:0.5f} \nL_inf: {:0.5f}\nL_1: {:0.5f}".format(rmse, linf, l1))
