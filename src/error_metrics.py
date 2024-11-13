import numpy as np
import pandas as pd

class Errors():
    """
    Class to calculate error metrics based on the models predicted probabilities and the given winning probabilities based on the odds.
    """
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


    def displayErrors(self, tournament_name, k_list = None, display=True):
        """ 
        Given prediction probabilities, returns all the utilized error metrics including RMSE, L-Infinity Norm,
        and L-1 Norm.

        Input:
            tournament_name (str): Name of tennis tournament
            k_list (None or list): The list of different k factors used in the H2H model to calculate error rates for. This can be none if the H2H model is not being used.
            display (boolean): Display calculated error metric values, default is True to display errors, False to not display errors.

        Output:
            Printed RMSE, Linf, and L1 metrics for given model(s).
        """
        self.k_list = k_list
        self.bar_width = 0.3
        # Only stores k if the k_list was given, if it is None there are no k's
        if self.k_list is not None:
            for i, k in enumerate(self.k_list):
                setattr(self, f'k{i + 1}', k)
            self.hth = True
            self.bar_width = 0.15
        else:
            self.hth = False

        tournament_name_underscore = tournament_name.replace(' ', '_')
        odds = pd.read_csv(f'../data/2023_{tournament_name_underscore}_Prob.csv', index_col=0)

        model = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}.csv', index_col = 0)

        csv_dict_k = {}
        csv_dict_k['original'] = model
        if self.k_list is not None:
            for k in self.k_list:
                csv_dict_k[k] = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}_head_to_head_{k}.csv', index_col=0)

        odds_comparison = odds[['normalized_winning_probability']]
        actual = odds_comparison['normalized_winning_probability']

        for model_name, model_df in csv_dict_k.items():
            # Take the Champion column corresponding to the current model to append to odds.
            champion_column = model_df[f'Champion']
            
            odds_comparison[f'Champion_{model_name}'] = champion_column

        # Display only if display is True.
        if display:
            for model_name, model_df in csv_dict_k.items():
                champion_column = odds_comparison[f'Champion_{model_name}']
                    
                rmse_value = self.RMSE(actual, champion_column)
                linf_value = self.Linf(actual, champion_column)
                l1_value = self.L1(actual, champion_column)

                # Print results for the current model
                print(f"Model: {model_name}")
                print(f"  RMSE: {rmse_value}")
                print(f"  Linf: {linf_value}")
                print(f"  L1: {l1_value}")
                print('-' * 20)  # Used to separate the output
