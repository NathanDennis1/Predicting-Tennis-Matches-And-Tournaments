import pandas as pd
import math

class ELO:
    """
    ELO class which is used to calculate ELO scores and gets the most recent age of each player in the tennis dataset.
    Creates the CSV for the elo calculations,
    """
    def __init__(self, initial_elo_rating, current_year):
        """
        Initializer for ELO class

        Args:
            initial_elo_rating(float): The initial ELO rating given to players
            current_year (int): The current year that data was obtained from.
        """
        self.initial_rating = float(initial_elo_rating)
        self.current_year = current_year
        self.tennis_data = pd.read_csv('../data/tennis_data.csv')
        self.elo_dataframe = None

    def initial_elos(self, surfaces, names):
        """
        Reads list of surfaces and names of players/teams and creates the initial ELO dataframe across all surfaces.

        Args:
            surfaces (list): A list of surfaces players are playing on. (Clay, Grass, Hard)
            names (list): Names of all teams/players for the sport.

        Returns:
            Final dataframe across all surfaces and players and their respective ELO scores.
        """

        # Creates initial elo dictionary
        elo_dict = {}
        for surface in surfaces:
            elo_dict[f"{surface}_ELO"] = [self.initial_rating] * len(names)    

        # Makes the dictionary a dataframe
        elo_df = pd.DataFrame(elo_dict, index=names)    

        self.elo_dataframe = elo_df

        return elo_df
    
    def get_names(self, data):
        """
        Gets the names of all players in a dataframe. Creates a set of the unique names in
        the winners and losers columns, then combines the set using union.

        Args:
            data (pandas dataframe): Dataframe for given tennis dataset

        Returns:
            List of player names from the tennis dataset
        """
        # First set for winner names
        winner_names = set(data['winner_name'].unique())

        # Second set for loser names
        loser_names = set(data['loser_name'].unique())

        names = winner_names.union(loser_names)

        return names
    
    def logistic(self, x):
        """
        Creates logistic function used for ELO calculation. Uses the common logistic equation

        Args:
            x (float): number input for the log function

        Returns:
            Final calculation of log function with given number as a float
        """
        return 1 / (1 + 10**-x)
    
    def expected_game_score(self, first_elo, second_elo, S=400):
        """
        Calculates expected game score based on logistic function.

        Args:
            first_elo (float): The first elo for a given team/player
            second_elo (float): The second elo for a given team/player
            S (int): Scaling factor

        Returns:
            Final calculation for an expected game score.
        """
        return self.logistic((first_elo - second_elo)/S)
    
    def decay_factor(self, year_diff, decay_rate = 0.3):
        """
        Calculates the decay factor based off the year difference from the present to calculate ELO scores.

        Args:
            year_diff (int): The calculated difference in years (Earlier year minus furthest year)
            decay_rate (float): Rate of decay for year difference equation

        Returns:
            Decay factor for the year difference as a float.
        """
        return math.exp(-decay_rate * abs(year_diff))

    def elo_calculation(self, data, elo_df, K = 20):
        """
        Calculates ELO scores for each tennis player based on previous match history

        Args:
            data (pandas dataframe): Dataframe for previous match history for each tennis tournament and professional match.
            elo_df (pandas dataframe): Dataframe of ELO scores for players on all surfaces.
            K (int): Sensitivity constant for ELO calculation.

        Returns:
            New Elo dataframe for players updated ELO scores.
        """
        # Train ELO scores based off all past data besides current year.
        data_training = data[data['Year'] < self.current_year]

        surfaces = ['Hard', 'Clay', 'Grass']

        for _, row in data_training.iterrows():
            winner = row['winner_name']
            loser = row['loser_name']
    
            surface = row['surface']
    
            winner_surface_elo = elo_df.loc[winner][f'{surface}_ELO']
            loser_surface_elo = elo_df.loc[loser][f'{surface}_ELO']


            # Adjusts ELO calculation rating based off tournament level.
            if row['tourney_level'] == 'G':
                K = K * 4 # Worth double ATP 1000 matches, so multipled by 4.
            elif (row['tourney_level'] == 'A' or row['tourney_level'] == 'M'):
                K = K * 2 # Worth half grand slams, double lower level tournaments.
            elif row['tourney_level'] == 'F':
                K = K
            elif row['tourney_level'] == 'D':
                K = K * 0.5 # Davis Cup has little effect on ELO scores.

            # Adjusts ELO calculation rating based off given years.
            year_diff = self.current_year - row['Year']
            decay_factor_year = self.decay_factor(year_diff)

            K = K * decay_factor_year

    
            p_winner = self.expected_game_score(winner_surface_elo, loser_surface_elo)
            p_loser = self.expected_game_score(loser_surface_elo, winner_surface_elo)

            new_elo_winner = winner_surface_elo + K * (1 - p_winner)
            new_elo_loser = loser_surface_elo + K * (0 - p_loser)

            elo_df.loc[winner, f'{surface}_ELO'] = new_elo_winner
            elo_df.loc[loser, f'{surface}_ELO'] = new_elo_loser

            # Slightly adjusts other surfaces ELO scores based on results on this surface.
            for s in surfaces:
                if s != surface:
                    elo_df.loc[winner, f'{s}_ELO'] = elo_df.loc[winner][f'{s}_ELO'] + K * 0.8 * (1 - p_winner)
                    elo_df.loc[loser, f'{s}_ELO'] = elo_df.loc[loser][f'{s}_ELO'] + K * 0.8 * (0 - p_loser)

            K = 20
            
        return elo_df
    
    def get_most_recent_age(self, data):
        """
        Calculates an estimated current age for each player in the dataset. This approach takes the last age a player lost and won
        at and adjusts depending on the year the match was played in. 

        Args:
            data (pandas dataframe): Dataframe for previous match history for each tennis tournament and professional match.

        Returns:
            Series for the estimated current age of a given tennis player.
        """
        # Creates a new dataframe sorted on year
        df_sorted = data.sort_values(by = 'Year', ascending=False)

        # Creates a dataframe of each of the winners last ages in the dataset. This keeps only the first in drop duplicates.
        winner_ages = df_sorted[['winner_name', 'winner_age', 'Year']].drop_duplicates('winner_name', keep='first')

        # Renames columns for proper naming. The winner name is the players name, and the most recent winning age.
        winner_ages.rename(columns={'winner_name': 'Player_name', 'winner_age': 'most_recent_age'}, inplace=True)
        winner_ages['Result'] = 'Match_winner'

        # Use similar strategy from winner_ages to obtain loser_ages
        loser_ages = df_sorted[['loser_name', 'loser_age', 'Year']].drop_duplicates('loser_name',keep='first')
        
        loser_ages.rename(columns={'loser_name': 'Player_name', 'loser_age': 'most_recent_age'}, inplace=True)
        loser_ages['Result'] = 'Match_loser'

        recent_ages = pd.concat([winner_ages, loser_ages])

        # Use pivot to create new dataframe using Player_name as the index, the column being the result of the match, and the values
        # being their most recent age.
        recent_ages = recent_ages.pivot(index ='Player_name', columns = 'Result', values = 'most_recent_age').reset_index()

        recent_ages.fillna(0)

        # Takes most recent year a player has played, used for age calculation
        recent_years = pd.concat([winner_ages[['Player_name', 'Year']], loser_ages[['Player_name', 'Year']]])

        recent_years = recent_years.drop_duplicates(subset='Player_name', keep='first')

        recent_ages = recent_ages.merge(recent_years, on='Player_name')

        # Calculate the maximum current age for each player based off both columns.
        recent_ages['Player_age'] = recent_ages[['Match_winner', 'Match_loser']].max(axis=1)

        recent_ages['Player_age'] = recent_ages['Player_age'] + (self.current_year - recent_ages['Year'])
        
        recent_ages.set_index('Player_name', inplace=True)

        return recent_ages['Player_age']
    
    
    def final_elo_csv(self):
        """
        Creates the final elo csv which has ELO calculations for all surfaces. Saves file to a csv titled
        player_elos.csv, saved in the data folder.

        Returns:
            Series for the number of games a player has played.
        """
        names = self.get_names(self.tennis_data)
        surfaces = self.tennis_data['surface'].unique()[0:3]
        elo_df = self.initial_elos(surfaces, list(names))
        player_elos = self.elo_calculation(self.tennis_data[self.tennis_data['Year'] < 2024], elo_df)
        player_elos['Player_age'] = self.get_most_recent_age(self.tennis_data)

        file_path = f'../data/player_elos.csv'
        player_elos.to_csv(file_path, index_label='Player_Name', index=True)