import pandas as pd
import numpy as np
import math
import sys
import os

# Add the src directory to the Python path so imports work during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from elo_calculations import ELO

class skillO:
    """
    SkillO class to calculate player skill and uncertainty updates for tennis matches.
    """

    def __init__(self, initial_mean, initial_variance, current_year, beta = 2, year_decay = 0.7, gamma = 0.1):
        """
        Initializer for skillO class

        Args:
            initial_mean (float): Initial skill level of players.
            initial_variance (float): Initial uncertainty in the skill level, their variance
            current_year (int): The current year that data was obtained from.
            beta (float): Beta scaling parameter used in SkillO calculations. Default set to 2.
            year_decay (float): Year decay factor determining how much past years are weighted. Default set to 0.7
            gamma (float): Weight factor to determine how much players SkillO ratings change after a given match. Default set to 0.1.
        """
        self.initial_mean = float(initial_mean)
        self.initial_variance = float(initial_variance)
        self.current_year = current_year
        self.skill_dataframe = None
        self.beta = beta
        self.year_decay = year_decay
        self.gamma = gamma

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

    def expected_game_score(self, mean_1, mean_2, variance_1, variance_2):
        """
        Calculates the expected outcome of a match between two players based on their skill and uncertainty.
        
        Args:
            mean_1 (float): Skill of player 1, their mean.
            mean_2 (float): Skill of player 2, their mean.
            variance_1 (float): Uncertainty of player 1, their variance.
            variance_2 (float): Uncertainty of player 2, their variance.
        
        Returns:
            float: Expected probability that player 1 wins.
        """
        # Calculate expected score using a logistic function
        skill_diff = mean_1 - mean_2
        uncertainty = np.sqrt(variance_1 + variance_2 + self.beta**2)
        return 1 / (1 + np.exp(-skill_diff / uncertainty))

    def skillO_calculation(self, data, SkillO_df, tau=0.1, gamma = 0.1):
        """
        Calculates SkillO for each player based on match history.

        Args:
            data (pd.DataFrame): Match data containing winner, loser, surface, and year of match.
            SkillO_df (pd.DataFrame): Dataframe of SkillO ratings.
            gamma (float): SkillO adjustment factor
            beta (float): Noise factor for performance uncertainty.

        Returns:
            pd.DataFrame: Updated player skill dataframe after all matches.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"data must be a pandas dataframe, it is type {type(data)}")

        surfaces = ['Hard', 'Clay', 'Grass']

        # Train skillO scores based off all past data besides current year.
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
            decay_factor_year = self.elo_instance.decay_factor(year_diff, self.year_decay)

            gamma = gamma * decay_factor_year

            # Player skills, mean and variance
            winner_mean = SkillO_df.loc[winner, f"{surface}_mean"]
            loser_mean = SkillO_df.loc[loser, f"{surface}_mean"]
            winner_variance = SkillO_df.loc[winner, f"{surface}_variance"]
            loser_variance = SkillO_df.loc[loser, f"{surface}_variance"]

            # Calculate expected probabilities
            p_winner = self.expected_game_score(winner_mean, loser_mean, winner_variance, loser_variance)
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
            SkillO_df.loc[winner, f"{surface}_mean"] = winner_new_mean
            SkillO_df.loc[loser, f"{surface}_mean"] = loser_new_mean
            SkillO_df.loc[winner, f"{surface}_variance"] = winner_new_variance
            SkillO_df.loc[loser, f"{surface}_variance"] = loser_new_variance

            for s in surfaces:
                if s != surface:
                    SkillO_df.loc[winner, f"{s}_mean"] = SkillO_df.loc[winner, f"{s}_mean"] + gamma_scale * 0.8 * (1 - p_winner)
                    SkillO_df.loc[loser, f"{s}_mean"] = SkillO_df.loc[loser, f"{s}_mean"] + gamma_scale * 0.8 * (0 - p_loser)

                    if p_winner > 0.5:
                        # Expected win
                        SkillO_df.loc[winner, f"{s}_variance"] = SkillO_df.loc[winner, f"{s}_variance"] * (1 - gamma * 0.8 * (1 - p_winner))  # Expected win, decrease variance
                        SkillO_df.loc[loser, f"{s}_variance"] = SkillO_df.loc[loser, f"{s}_variance"] * (1 - gamma * 0.8 * p_loser)  # Expected loss, decrease variance
                    else:
                        # Unexpected win
                        SkillO_df.loc[winner, f"{s}_variance"] = SkillO_df.loc[winner, f"{s}_variance"] * (1 + gamma * 0.8 * p_winner)  # Unexpected win, increase variance
                        SkillO_df.loc[loser, f"{s}_variance"] = SkillO_df.loc[loser, f"{s}_variance"] * (1 + gamma * 0.8 * (1 - p_loser))  # Unexpected loss, increase variance

            gamma = self.gamma
        return SkillO_df

    def simulate_multiple_runs(self, data, num_simulations, surfaces, names):
        """
        Run the skillO calculation multiple times and take the average mean and variance for each player.

        Args:
            data (pd.DataFrame): Match data containing winner, loser, surface, and year of match.
            num_simulations (int): Number of times to run the simulation.
            surfaces (list): List of surfaces (Hard, Clay, Grass)
            names (list): List of player names.

        Returns:
            pd.DataFrame: Dataframe with average mean and variance across all simulations.
        """
        # Initialize a list to store the skill results after each simulation.
        all_means = []
        all_variances = []
        
        for _ in range(num_simulations):
            # Reset the initial skill dataframe for each simulation to the initial skill level.
            skill_df = self.initial_skills(surfaces, names)
            
            updated_df = self.skillO_calculation(data, skill_df, gamma = self.gamma)
            
            # Store the means and variances from the current simulation.
            all_means.append(updated_df[[f"{s}_mean" for s in surfaces]])
            all_variances.append(updated_df[[f"{s}_variance" for s in surfaces]])
        
        # Calculate the average mean and variance for each player across all simulations.
        mean_df = pd.concat(all_means, axis=0)
        mean_df = mean_df.groupby(mean_df.index).mean()
        variance_df = pd.concat(all_variances, axis=0)
        variance_df = variance_df.groupby(variance_df.index).mean()
        final_df = pd.concat([mean_df, variance_df], axis=1)
        final_df.columns = [f"{s}_mean" for s in surfaces] + [f"{s}_variance" for s in surfaces]
        
        return final_df

    def final_csv(self, tennis_data, file_path='../data/skillo.csv'):
        """
        Creates the final csv.

        Args:
            tennis_data (pandas dataframe): The dataframe containing all tennis match data
            file_path (str): Path of the file to save, default player_elos.csv

        Returns:
            Series for the number of games a player has played.
        """
        names = self.elo_instance.get_names(tennis_data)
        surfaces = tennis_data['surface'].unique()[0:3]
        updated_df = self.simulate_multiple_runs(tennis_data, 30, surfaces, list(names))
        updated_df['Player_age'] = self.elo_instance.get_most_recent_age(tennis_data)

        updated_df.to_csv(file_path, index_label='Player_Name', index=True)