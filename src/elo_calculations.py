import pandas as pd

class ELO:
    def __init__(self):
        """
        Initializer for ELO class
        """
        self.initial_rating = float(1500)
        self.current_year = 2023
        self.tennis_data = pd.read_csv('../data/tennis_data.csv')
        self.elo_dataframe = None

    def initial_elos(self, surfaces, names):
        """
        Reads list of surfaces and names of players/teams and creates the initial ELO dataframe across all surfaces.

        Args:
            surfaces (list): A list of surfaces players are playing on. (Tennis could include Clay or Grass, Basketball could include Home or Away court)
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
        Creates logistic function used for ELO calculation.

        Args:
            x (float): number input for the log function

        Returns:
            Final calculation of log function with given number
        """
        return 1 / (1 + 10**-x)
    
    def expected_game_score(self, first_elo, second_elo, S=400):
        """
        Calculates expected game score based on logistic function

        Args:
            first_elo (float): The first elo for a given team/player
            second_elo (float): The second elo for a given team/player
            S (int): Scaling factor

        Returns:
            Final calculation for an expected game score.
        """
        return self.logistic((first_elo - second_elo)/S)
    
    def elo_calculation(self, data, elo_df, K = 20):
        """
        Calculates ELO scores for each tennis player based on previous match history

        Args:
            data (pandas dataframe): Dataframe for previous match history for each tennis tournament and professional match.
            elo_df (pandas dataframe): Dataframe of ELO scores for players on all surfaces.
            K (int): Sensitivity Constant

        Returns:
            New Elo dataframe for players updated ELO scores.
        """
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
            if row['Year'] <= 2017:
                K = K * 0.05
            elif (row['Year'] > 2017 and row['Year'] <= 2020):
                K = K * 0.1
            elif (row['Year'] == 2021):
                K = K  * 0.5
            else:
                K = K
    
            p_winner = self.expected_game_score(winner_surface_elo, loser_surface_elo)
            p_loser = self.expected_game_score(loser_surface_elo, winner_surface_elo)

            new_elo_winner = winner_surface_elo + K * (1 - p_winner)
            new_elo_loser = loser_surface_elo + K * (0 - p_loser)

            elo_df.loc[winner, f'{surface}_ELO'] = new_elo_winner
            elo_df.loc[loser, f'{surface}_ELO'] = new_elo_loser

            for s in surfaces:
                if s != surface:
                    elo_df.loc[winner, f'{s}_ELO'] = elo_df.loc[winner][f'{s}_ELO'] + K * 0.5 * (1 - p_winner)
                    elo_df.loc[loser, f'{s}_ELO'] = elo_df.loc[loser][f'{s}_ELO'] + K * 0.5 * (0 - p_loser)

            K = 20
            
            
        return elo_df
    
    def get_most_recent_age(self, data):
        """
        Calculates an estimated current age for each player in the dataset.

        Args:
            data (pandas dataframe): Dataframe for previous match history for each tennis tournament and professional match.

        Returns:
            Series for the estimated current age of a given tennis player.
        """
        # Creates a new dataframe sorted on year
        df_sorted = data.sort_values(by = 'Year', ascending=False)

        # Create a dataframe of each of the winners last ages in the dataset, keeping only the first in drop duplicates.
        winner_ages = df_sorted[['winner_name', 'winner_age', 'Year']].drop_duplicates('winner_name', keep='first')

        # Renames columns for proper naming. The winner name is the players name, and the most recent winning age.
        winner_ages.rename(columns={'winner_name': 'Player_name', 'winner_age': 'most_recent_age'}, inplace=True)
        winner_ages['Result'] = 'Match_winner'

        # Create a dataframe of each of the losers last ages in the dataset, keeping only the first in drop duplicates.
        loser_ages = df_sorted[['loser_name', 'loser_age', 'Year']].drop_duplicates('loser_name',keep='first')
        
        # Renames the columns similar to winners_ages for similar naming convention.
        loser_ages.rename(columns={'loser_name': 'Player_name', 'loser_age': 'most_recent_age'}, inplace=True)
        loser_ages['Result'] = 'Match_loser'

        recent_ages = pd.concat([winner_ages, loser_ages])

        # Use pivot to create new dataframe using Player_name as the index, the column being the result of the match, and the values
        # being their most recent age.
        recent_ages = recent_ages.pivot(index ='Player_name', columns = 'Result', values = 'most_recent_age').reset_index()

        # Fills NaN values with 0 as placeholder, won't be used since the players age will be larger for either a win or loss.
        recent_ages.fillna(0)

        # Takes most recent year a player has played, used for age calculation
        recent_years = pd.concat([winner_ages[['Player_name', 'Year']], loser_ages[['Player_name', 'Year']]])

        # Drops duplicates on player names, keeping only the most recent year a player has played (The dataframe is already sorted on year)
        recent_years = recent_years.drop_duplicates(subset='Player_name', keep='first')

        # Merges most recent ages alongside the most recent year a match was played, based off the players name.
        recent_ages = recent_ages.merge(recent_years, on='Player_name')

        # Calculate the maximum current age for each player based off both columns.
        recent_ages['Player_age'] = recent_ages[['Match_winner', 'Match_loser']].max(axis=1)

        recent_ages['Player_age'] = recent_ages['Player_age'] + (self.current_year - recent_ages['Year'])
        
        recent_ages.set_index('Player_name', inplace=True)

        return recent_ages['Player_age']
    
    def games_played(self, data):
        """
        Calculates the number of games a player has played

        Args:
            data: Dataframe for previous match history for each tennis tournament and professional match.

        Returns:
            Series for the number of games a player has played.
        """
        # Counts all values for each winner and loser names in the dataframe, indicating how many matches played
        games_played_winner = pd.DataFrame(data['winner_name'].value_counts())
        games_played_loser = pd.DataFrame(data['loser_name'].value_counts())

        # Concats both dataframe together for all players, winners or losers.
        games_played = pd.concat([games_played_winner, games_played_loser])
        return games_played.groupby(games_played.index).sum()['count']
    
    def final_elo_csv(self):
        """
        Creates the final elo csv which has ELO calculations for all surfaces

        Args:
            data: Dataframe for previous match history for each tennis tournament and professional match.

        Returns:
            Series for the number of games a player has played.
        """
        names = self.get_names(self.tennis_data)
        surfaces = self.tennis_data['surface'].unique()[0:3]
        elo_df = self.initial_elos(surfaces, list(names))
        player_elos = self.elo_calculation(self.tennis_data[self.tennis_data['Year'] < 2024], elo_df)
        player_elos['Player_age'] = self.get_most_recent_age(self.tennis_data)
        player_elos['Games_played'] = self.games_played(self.tennis_data)

        file_path = f'../data/player_elos.csv'
        player_elos.to_csv(file_path, index_label='Player_Name', index=True)
    
