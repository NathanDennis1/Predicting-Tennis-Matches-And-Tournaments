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
