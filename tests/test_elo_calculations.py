import pytest
from src.elo_calculations import ELO
import os
import pandas as pd

@pytest.fixture
def elo():
    """
    Created ELO class for testing
    """
    return ELO(initial_elo_rating=1500, current_year = 2023)

@pytest.fixture
def df():
    """
    Mock dataframe with arbitrary player names.
    """
    data = {
        'tourney_name': ['Australian Open', 'French Open', 'Wimbledon', 'US Open', 
                        'French Open', 'French Open', 'Australian Open', 'Wimbledon', 
                        'Wimbledon', 'US Open'],
        'surface': ['Hard', 'Clay', 'Grass', 'Hard', 'Clay', 'Clay', 'Hard', 'Grass', 'Hard', 'Hard'],
        'draw_size': [128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
        'tourney_level': ['Grand Slam', 'Grand Slam', 'Grand Slam', 'Grand Slam', 
                        'Grand Slam', 'Grand Slam', 'Grand Slam', 'Grand Slam', 
                        'Grand Slam', 'Grand Slam'],
        'best_of': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'winner_name': ['Player_1', 'Player_3', 'Player_2', 'Player_4', 
                        'Player_1', 'Player_3', 'Player_2', 'Player_4', 
                        'Player_1', 'Player_3'],
        'winner_age': [26, 24, 27, 31, 26, 24, 27, 31, 26, 24],
        'loser_name': ['Player_2', 'Player_4', 'Player_3', 'Player_1', 
                    'Player_4', 'Player_2', 'Player_1', 'Player_3', 
                    'Player_2', 'Player_4'],
        'loser_age': [28, 30, 25, 29, 30, 27, 29, 25, 28, 30],
        'Year': [2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023]}

    final_df = pd.DataFrame(data)
    
    return final_df

@pytest.fixture
def elo_df():
    """
    Mock elo scores dataframes for the 4 arbitrary players, random elo scores and ages.
    """
    elo_data = {
        'Player_Name': ['Player_1', 'Player_2', 'Player_3', 'Player_4' ],
        'Hard_ELO': [1505.12, 1492.34, 1510.75, 1489.90],
        'Clay_ELO': [1489.56, 1503.67, 1490.85, 1500.12],
        'Grass_ELO': [1502.23, 1487.90, 1506.12, 1493.40],
        'Player_age': [26, 28, 24, 30]}

    elo_df = pd.DataFrame(elo_data)

    elo_df = elo_df.set_index('Player_Name')
    
    return elo_df
    
class Test_elo_calculations():
    """
    Class to test the elo_calculations script.
    """
    def test_initial_elos(self, elo):
        """
        Tests the inital elos function to return a dataframe
        """
        surfaces = ['Clay', 'Hard']
        names = ['Player', 'Player_2']
        elo_df = elo.initial_elos(surfaces, names)
        assert isinstance(elo_df, pd.DataFrame), f"elo_df should return a dataframe, instead returned {type(elo_df)}"

    def test_get_names(self, elo, df):
        """
        Tests the get names function to return a set
        """
        names = elo.get_names(df)
        assert isinstance(names, set), f"get_names should return a set, instead returned {type(names)}"

    def test_logistic(self, elo):
        """
        Tests the logistic function to return a float
        """
        log = elo.logistic(1)
        assert isinstance(log, float), f"Logistic function should return a float, instead returned {type(log)}"

    def test_expected_game_score(self, elo):
        """
        Tests the inital elos function to return a float
        """
        game_score = elo.expected_game_score(float(1500), float(1500))
        assert isinstance(game_score, float), f"Logistic function should return a float, instead returned {type(game_score)}"

    def test_decay_factor(self, elo):
        """
        Tests the decay factor function to return a float
        """
        decay_rate = elo.decay_factor(2)
        assert isinstance(decay_rate, float), f"Decay factor should return a float, instead returned {type(decay_rate)}"

    def test_elo_calculation(self, elo, df, elo_df):
        """
        Tests the elo calculation function to return a dataframe
        """
        elo_calc = elo.elo_calculation(df, elo_df)
        assert isinstance(elo_calc, pd.DataFrame), f"Elo calculation should return a dataframe, instead returned {type(elo_calc)}"

    def test_get_most_recent_age(self, elo, df):
        """
        Tests the get most recent age function to return a series
        """
        recent_age = elo.get_most_recent_age(df)
        assert isinstance(recent_age, pd.Series), f"Get most recent age should return a series, instead returned {type(recent_age)}"

    def test_final_elo_csv(self, elo, tmp_path, df):
        """
        Tests the final elo csv function to create a csv in data.
        """
        file_path = tmp_path / "player_elos.csv"

        elo.final_elo_csv(df, file_path=str(file_path))

        assert file_path.exists(), "The player_elos.csv file was not created"