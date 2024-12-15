import numpy as np
import pandas as pd

class Errors():
    """
    Class to calculate error metrics based on the models predicted probabilities and the given winning probabilities based on the odds.
    """
    def __init__(self):
        """
        Initializer for Errors class.
        """
        pass

    def RMSE(self, true, pred):
        """ 
        Calculates RMSE score, the root mean squared error between the true and predicted values.

        Args:
            true (pandas series): Series of true values (betting odds probability)
            pred (pandas series): Series of predicted values (model output probability)

        Return:
            RMSE score as a float.

        Raises:
            TypeError: Inputs must both be series, true and pred, raises error if not.
        """
        if not isinstance(true, pd.Series):
            raise TypeError(f"The true value is not a series, it has to be of type series, it is {type(true)}")
        if not isinstance(pred, pd.Series):
            raise TypeError(f"The predicted value is not a series, it has to be of type series, it is {type(pred)}")
        
        return np.sqrt(np.mean(np.square(true-pred)))

    def Linf(self, true, pred):
        """ 
        Calculates L-Infinity Norm score, the maximum absolute error between the true and predicted values.

        Args:
            true (pandas series): Series of true values (betting odds probability)
            pred (pandas series): Series of predicted values (model output probability)

        Output:
            L-Infinity Norm score as a float

        Raises:
            TypeError: Inputs must both be series, true and pred, raises error if not.
        """
        if not isinstance(true, pd.Series):
            raise TypeError(f"The true value is not a series, it has to be of type series, it is {type(true)}")
        if not isinstance(pred, pd.Series):
            raise TypeError(f"The predicted value is not a series, it has to be of type series, it is {type(pred)}")
        return np.max(np.abs(true-pred))

    def L1(self, true, pred):
        """ 
        Calculates L-1 Norm score, the average absolute difference between the true and predicted values.

        Args:
            true (pandas series): True values (betting odds probability)
            pred (pandas series): Predicted values (model output probability)

        Output:
            L-1 Norm score as a float

        Raises:
            TypeError: Inputs must both be series, true and pred, raises error if not.
        """
        if not isinstance(true, pd.Series):
            raise TypeError(f"The true value is not a series, it has to be of type series, it is {type(true)}")
        if not isinstance(pred, pd.Series):
            raise TypeError(f"The predicted value is not a series, it has to be of type series, it is {type(pred)}")
        return np.mean(np.absolute(true-pred))

    def MAPE(self, true, pred):
        """ 
        Calculates the Mean Absolute Percentage Error (MAPE) between the true and predicted values.

        Args:
            true (pandas series): True values (betting odds probability)
            pred (pandas series): Predicted values (model output probability)

        Returns:
            MAPE score as a float

        Raises:
            TypeError: Inputs must both be series, true and pred, raises error if not.
        """
        if not isinstance(true, pd.Series):
            raise TypeError(f"The true value is not a series, it has to be of type series, it is {type(true)}")
        if not isinstance(pred, pd.Series):
            raise TypeError(f"The predicted value is not a series, it has to be of type series, it is {type(pred)}")
        
        # Avoid division by zero or invalid percentage error
        return np.mean(np.abs((true - pred) / true)) * 100

    def R_squared(self, true, pred):
        """ 
        Calculates the R-squared (coefficient of determination) between the true and predicted values.

        Args:
            true (pandas series): True values (betting odds probability)
            pred (pandas series): Predicted values (model output probability)

        Returns:
            R-squared score as a float

        Raises:
            TypeError: Inputs must both be series, true and pred, raises error if not.
        """
        if not isinstance(true, pd.Series):
            raise TypeError(f"The true value is not a series, it has to be of type series, it is {type(true)}")
        if not isinstance(pred, pd.Series):
            raise TypeError(f"The predicted value is not a series, it has to be of type series, it is {type(pred)}")

        # Compute the residual sum of squares (RSS) and total sum of squares (TSS)
        ss_res = np.sum((true - pred) ** 2)
        ss_tot = np.sum((true - np.mean(true)) ** 2)
        
        r2 = 1 - (ss_res / ss_tot)
        
        return r2




    def displayErrors(self, rating_system, tournament_name, simulation_number = None, k_list = None):
        """ 
        Given prediction probabilities, returns all the utilized error metrics including RMSE, L-Infinity Norm,
        L-1, MAPE and R-squared score.

        Args:
            rating_system (str): Name of given rating system, either ELO or SkillO.
            tournament_name (str): Name of tennis tournament. (Ex: Wimbledon, Roland Garros, Australian Open)
            simulation_number (None or str): Optional imput for simulation number to display errors for certain simulation number csv files created. Default set to None
            k_list (None or list): The list (max length 3) of different k factors used in the H2H model to calculate error rates for. 
                                   This can be none if the H2H model is not being used, which is the default.

        Returns:
            Dataframe across all 5 error metrics for given rating system.
        
        Raises:
            ValueError: k_list has to be either None or a list of at most 3 elements.
            ValueError: rating_system must be 'ELO' or 'SkillO'.
        """
        if rating_system not in ['ELO', 'SkillO']:
            raise ValueError("rating_system must be 'ELO' or 'SkillO'.")

        self.rating_system = rating_system
        self.k_list = k_list
        self.bar_width = 0.3
        # Only stores k if the k_list was given, if it is None there are no k's
        if self.k_list is not None:
            if not isinstance(k_list, list):
                raise ValueError("k_list must be a list")
            
            if len(k_list) > 3:
                raise ValueError("k_list must have at most 3 elements")
            
            for i, k in enumerate(self.k_list):
                setattr(self, f'k{i + 1}', k)
            self.hth = True
            self.bar_width = 0.15
        else:
            self.hth = False

        tournament_name_underscore = tournament_name.replace(' ', '_')
        odds = pd.read_csv(f'../data/2023_{tournament_name_underscore}_Prob.csv', index_col=0)
        if simulation_number is not None:
            model = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}_{self.rating_system}_{simulation_number}.csv', index_col = 0)
        else:
            model = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}_{self.rating_system}.csv', index_col = 0)

        csv_dict_k = {}
        csv_dict_k['original'] = model
        if self.k_list is not None:
            for k in self.k_list:
                if simulation_number is not None:
                    csv_dict_k[k] = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}_head_to_head_{k}_{self.rating_system}_{simulation_number}.csv', index_col=0)
                else:
                    csv_dict_k[k] = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}_head_to_head_{k}_{self.rating_system}.csv', index_col=0)

        odds_comparison = odds[['normalized_winning_probability']].copy()
        actual = odds_comparison['normalized_winning_probability']

        error_metrics = []

        for model_name, model_df in csv_dict_k.items():
            # Take the Champion column corresponding to the current model to append to odds
            champion_column = model_df[f'Champion']
            odds_comparison[f'Champion_{model_name}'] = champion_column

            # Calculate error metrics
            rmse_value = self.RMSE(actual, champion_column)
            linf_value = self.Linf(actual, champion_column)
            l1_value = self.L1(actual, champion_column)
            mape_value = self.MAPE(actual, champion_column)
            r2_value = self.R_squared(actual, champion_column)

            error_metrics.append({
                'Model': self.rating_system,
                'RMSE': rmse_value,
                'Linf': linf_value,
                'L1': l1_value,
                'MAPE': mape_value,
                'R-squared': r2_value
            })

        error_df = pd.DataFrame(error_metrics)

        return error_df