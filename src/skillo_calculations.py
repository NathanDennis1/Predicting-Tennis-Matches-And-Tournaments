import pandas as pd
import numpy as np
import math
from elo_calculations import ELO

class skillO:
    """
    SkillO class to calculate player skill and uncertainty updates for tennis matches.
    """

    def __init__(self, initial_mean, initial_variance, current_year):
        """
        Initializer for skillO class

        Args:
            initial_mean (float): Initial skill level of players.
            initial_variance (float): Initial uncertainty in the skill level, their variance
            current_year (int): The current year that data was obtained from.
        """
        self.initial_mean = float(initial_mean)
        self.initial_variance = float(initial_variance)
        self.current_year = current_year
        self.skill_dataframe = None

        # Initializes mock ELO class to import functions over
        self.elo_instance = ELO(1500, current_year)

    def initial_skills(self, surfaces, names):
        """
        Creates initial skill dataframe with skill mean and variance for each player.
        
        Args:
            surfaces (list): A list of surfaces players are playing on. (Clay, Grass, Hard)
            names (list): Names of all players.

        Returns:
            Dataframe containing initial skill (mean) and uncertainty (variance) for each player as a pandas dataframe.
        """
        # Create dictionary for player skills and uncertainties (mean, variance)
        skill_dict = {}
        for surface in surfaces:
            skill_dict[f"{surface}_mean"] = [self.initial_mean] * len(names)
            skill_dict[f"{surface}_variance"] = [self.initial_variance] * len(names)

        # Create dataframe
        skill_df = pd.DataFrame(skill_dict, index=names)
        self.skill_dataframe = skill_df
        return skill_df

    def expected_game_score(self, mean_1, mean_2, variance_1, variance_2, beta=0.1):
        """
        Calculates the expected outcome of a match between two players based on their skill and uncertainty.
        
        Args:
            mean_1 (float): Skill of player 1, their mean.
            mean_2 (float): Skill of player 2, their mean.
            variance_1 (float): Uncertainty of player 1, their variance.
            variance_2 (float): Uncertainty of player 2, their variance.
            beta (float): Noise factor that controls the degree of uncertainty in performance.
        
        Returns:
            float: Expected probability that player 1 wins.
        """
        # Calculate expected score using a logistic function
        skill_diff = mean_1 - mean_2
        uncertainty = np.sqrt(variance_1 + variance_2 + beta**2)
        return 1 / (1 + np.exp(-skill_diff / uncertainty))
