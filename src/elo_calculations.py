import pandas as pd

class ELO:
    def __init__(self):
        self.initial_rating = float(1500)
        self.current_year = 2024

    def initial_elos(self, surfaces, names):
        """
        Reads dataframe and calculates initial ELO ratings.

        Args:
        surfaces: A list of surfaces players are playing on. (Tennis could include Clay or Grass, Basketball could include Home or Away court)
        names: Names of all teams/players for the sport.

        Returns:
        Final dataframe across all surfaces and players.
        """

        elo_dict = {}
        for surface in surfaces:
            elo_dict[f"{surface}_ELO"] = [self.initial_rating] * len(names)    

        player_elos = pd.DataFrame(elo_dict, index=names)    

        return player_elos
    
    def get_names(self, data):
        winner_names = set(data['winner_name'].unique())

        loser_names = set(data['loser_name'].unique())

        names = winner_names.union(loser_names)

        return names
    
    def logistic(self, x):
        """
        Creates logistic function used for ELO calculation.

        Args:
        x: some number used for the log function

        Returns:
        Final calculation of log function with given number
        """
        return 1 / (1 + 10**-x)
    
    def expected_game_score(self, first_elo, second_elo, S=400):
        """
        Calculates expected game score based on logistic function

        Args:
        first_elo: The first elo for a given team/player
        second_elo: The second elo for a given team/player
        S = Scaling factor

        Returns:
        Final calculation for an expected game score.
        """
        return self.logistic((first_elo - second_elo)/S)
    
    def elo_calculation(self, data, elo_df, K = 20):
        """
        Calculates ELO scores for each tennis player based on previous match history

        Args:
        data: Dataframe for previous match history for each tennis tournament and professional match.
        elo_df: Dataframe of ELO scores for players on all surfaces.
        K: Sensitivity Constant

        Returns:
        New Elo dataframe for players updated ELO scores.
        """
        for index, row in data.iterrows():
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


            if row['Year'] <= 2015:
                K = K * 0.02 + (row['Year']-2000) / 20
            elif (row['Year'] > 2015 and row['Year'] <= 2020):
                K = K * 0.05 + (row['Year']-2015) / 15
            elif (row['Year'] > 2020 and row['Year'] <= 2022):
                K = K  * 0.5 + (row['Year'] - 2020) * 5
            else:
                K = K
    
            p_winner = self.expected_game_score(winner_surface_elo, loser_surface_elo)
            p_loser = self.expected_game_score(loser_surface_elo, winner_surface_elo)

            new_elo_winner = winner_surface_elo + K * (1 - p_winner)
            new_elo_loser = loser_surface_elo + K * (0 - p_loser)

            elo_df.loc[winner, f'{surface}_ELO'] = new_elo_winner
            elo_df.loc[loser, f'{surface}_ELO'] = new_elo_loser

            K = 20
            
            
        return elo_df
    
    def get_most_recent_age(self, data):
        """
        Calculates an estimated current age for each player in the dataset.

        Args:
        data: Dataframe for previous match history for each tennis tournament and professional match.

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
        games_played_winner = pd.DataFrame(data['winner_name'].value_counts())
        games_played_loser = pd.DataFrame(data['loser_name'].value_counts())
        games_played = pd.concat([games_played_winner, games_played_loser])
        return games_played.groupby(games_played.index).sum()['count']
    
def main():
    
    tennis_data = pd.read_csv('tennis_data.csv')

    elo = ELO()

    names = elo.get_names(tennis_data)

    surfaces = tennis_data['surface'].unique()[0:3]

    surfaces = list(surfaces)

    elo_df = elo.initial_elos(surfaces, list(names))

    player_elos = elo.elo_calculation(tennis_data[tennis_data['Year'] < 2024], elo_df)

    player_elos['Player_age'] = elo.get_most_recent_age(tennis_data)

    player_elos['Games_played'] = elo.games_played(tennis_data)

    player_elos.to_csv('player_elos.csv', index_label='Player_Name', index=True)

if __name__ == "__main__":
    main()
