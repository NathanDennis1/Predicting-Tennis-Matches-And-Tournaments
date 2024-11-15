import pytest
from src.elo_calculations import ELO
import os
import pandas as pd

@pytest.fixture
def elo():
    return ELO(initial_elo_rating=1500, current_year = 2023)

@pytest.fixture
def df():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tennis_data.csv')
    print(f"Looking for data at: {data_path}")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")
    
    df = pd.read_csv(data_path)
    
    return df

@pytest.fixture
def elo_df():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'player_elos.csv')
    print(f"Looking for data at: {data_path}")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")
    
    elo_df = pd.read_csv(data_path, index_col = 'Player_Name')
    
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
        game_score = elo.expected_game_score(1500, 1500)
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