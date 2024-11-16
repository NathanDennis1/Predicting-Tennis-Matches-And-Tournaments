import pandas as pd


class past_match_data():
    """
    Class to obtain past match data between players
    """
    def __init__(self):
        """
        Initializer for past_match_data class
        """
        pass


    def win_percentage_common_opponents(self, data):
        """
        Function for obtaining the winning percentage and number of games played for every player in the tennis
        dataset. Creates a csv file for both win percentage and games played between every player in the dataset.

        Args:
            data (pandas Dataframe): Dataframe for all of the past tennis match data.

        Raises:
            TypeError: data must be of type dataframe.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data input must be of type pandas dataframe")
        games_played = {}
        wins = {}

        for _, row in data.iterrows():
            winner = row['winner_name']
            loser = row['loser_name']
            
            # Inserts games played counter for new players not in the data dictionary
            if winner not in games_played:
                games_played[winner] = {}
                wins[winner] = {}
                
            if loser not in games_played:
                games_played[loser] = {}
                wins[loser] = {}
                
            # Update games played and wins for both winner and loser against each other
            if loser not in games_played[winner]:
                games_played[winner][loser] = 0
                wins[winner][loser] = 0
            if winner not in games_played[loser]:
                games_played[loser][winner] = 0
                wins[loser][winner] = 0
        
            games_played[winner][loser] += 1
            games_played[loser][winner] += 1
            wins[winner][loser] += 1

        # Calculate win percentages
        win_percentages = {}
        for player in games_played:
            win_percentages[player] = {}
            for opponent in games_played[player]:
                total_games = games_played[player][opponent]
                total_wins = wins[player][opponent]
                win_percentage = total_wins / total_games if total_games > 0 else 0
                win_percentages[player][opponent] = win_percentage

        # Make into dataframe, fill the NA values with 0 which means players never played each other
        win_percentage_df = pd.DataFrame(win_percentages).fillna(0)

        games_played_df = pd.DataFrame(games_played).fillna(0)

        file_path_games = f'../data/games_played_opponents.csv'

        file_path_win_percent = f'../data/win_percentage.csv'

        games_played_df.index.name = 'Player_Name'

        win_percentage_df.index.name = 'Player_Name'

        games_played_df.to_csv(file_path_games)

        win_percentage_df.to_csv(file_path_win_percent)

