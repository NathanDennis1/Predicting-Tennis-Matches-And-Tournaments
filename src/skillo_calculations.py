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

    def trueskill_calculation(self, data, trueskill_df, tau=0.1, gamma = 0.1, beta=0.4):
        """
        Calculates TrueSkill for each player based on match history.

        Args:
            data (pd.DataFrame): Match data containing winner, loser, surface, and year of match.
            trueskill_df (int): Adjustment factor for skill update.
            beta (float): Noise factor for performance uncertainty.

        Returns:
            pd.DataFrame: Updated player skill dataframe after all matches.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"data must be a pandas dataframe, it is type {type(data)}")

        surfaces = ['Hard', 'Clay', 'Grass']

        # Train SkillO scores based off all past data besides current year.
        data_training = data[data['Year'] < self.current_year]
        
        for _, row in data_training.iterrows():
            winner = row['winner_name']
            loser = row['loser_name']
            surface = row['surface']

            # Adjusts SkillO calculation rating based off tournament level.
            if row['tourney_level'] == 'G':
                gamma = gamma * 4 # Worth double ATP 1000 matches, so multipled by 4.
            elif (row['tourney_level'] == 'A' or row['tourney_level'] == 'M'):
                gamma = gamma * 2 # Worth half grand slams, double lower level tournaments.
            elif row['tourney_level'] == 'F':
                gamma = gamma
            elif row['tourney_level'] == 'D':
                gamma = gamma * 0.5 # Davis Cup has little effect on ELO scores.

            year_diff = self.current_year - row['Year']

            # Calculates decay factor based on the difference in years
            decay_factor_year = self.elo_instance.decay_factor(year_diff, 0.7)

            gamma = gamma * decay_factor_year

            # Player skills, mean and variance
            winner_mean = trueskill_df.loc[winner, f"{surface}_mean"]
            loser_mean = trueskill_df.loc[loser, f"{surface}_mean"]
            winner_variance = trueskill_df.loc[winner, f"{surface}_variance"]
            loser_variance = trueskill_df.loc[loser, f"{surface}_variance"]

            # Calculate expected probabilities
            p_winner = self.expected_game_score(winner_mean, loser_mean, winner_variance, loser_variance, beta)
            p_loser = 1 - p_winner

            # Update skill (mean) based on match outcome
            gamma_scale = abs(np.random.normal(0, gamma))
            winner_new_mean = winner_mean + gamma_scale * (1 - p_winner)
            loser_new_mean = loser_mean + gamma_scale * (0 - p_loser)

            # Update uncertainty (variance) after the match
            if p_winner > 0.5:
                # Expected win
                winner_new_variance = winner_variance * (1 - gamma * (1 - p_winner))  # Expected win, decrease variance
                loser_new_variance = loser_variance * (1 - gamma * p_loser)  # Expected loss, decrease variance
            else:
                # Unexpected win
                winner_new_variance = winner_variance * (1 + gamma * p_winner)  # Unexpected win, increase more
                loser_new_variance = loser_variance * (1 + gamma * (1 - p_loser))  # Unexpected loss, increase more

            # Apply updated skill and uncertainty to the dataframe
            trueskill_df.loc[winner, f"{surface}_mean"] = winner_new_mean
            trueskill_df.loc[loser, f"{surface}_mean"] = loser_new_mean
            trueskill_df.loc[winner, f"{surface}_variance"] = winner_new_variance
            trueskill_df.loc[loser, f"{surface}_variance"] = loser_new_variance
        
            for s in surfaces:
                if s != surface:
                    trueskill_df.loc[winner, f"{s}_mean"] = trueskill_df.loc[winner, f"{s}_mean"] + gamma_scale * 0.8 * (1 - p_winner)
                    trueskill_df.loc[loser, f"{s}_mean"] = trueskill_df.loc[loser, f"{s}_mean"] + gamma_scale * 0.8 * (0 - p_loser)

                    if p_winner > 0.5:
                        # Expected win
                        trueskill_df.loc[winner, f"{s}_variance"] = trueskill_df.loc[winner, f"{s}_variance"] * (1 - gamma * 0.8 * (1 - p_winner))  # Expected win, decrease variance
                        trueskill_df.loc[loser, f"{s}_variance"] = trueskill_df.loc[loser, f"{s}_variance"] * (1 - gamma * 0.8 * p_loser)  # Expected loss, decrease variance
                    else:
                        # Unexpected win
                        trueskill_df.loc[winner, f"{s}_variance"] = trueskill_df.loc[winner, f"{s}_variance"] * (1 + gamma * 0.8 * p_winner)  # Unexpected win, increase variance
                        trueskill_df.loc[loser, f"{s}_variance"] = trueskill_df.loc[loser, f"{s}_variance"] * (1 + gamma * 0.8 * (1 - p_loser))  # Unexpected loss, increase variance

            gamma = 0.1
        return trueskill_df

