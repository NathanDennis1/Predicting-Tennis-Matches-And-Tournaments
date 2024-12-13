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
    Mock dataframe with arbitrary player names for tennis data in a given year.
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
        'loser_age': [27, 31, 24, 26, 30, 27, 26, 24, 27, 31],
        'Year': [2022, 2022, 2022, 2023, 2023, 2023, 2023, 2023, 2023, 2023]}

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
        Tests the inital elos function to return a dataframe.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        surfaces = ['Clay', 'Hard']
        names = ['Player', 'Player_2']
        elo_df = elo.initial_elos(surfaces, names)
        assert isinstance(elo_df, pd.DataFrame), f"elo_df should return a dataframe, instead returned {type(elo_df)}"

    def test_get_names(self, elo, df):
        """
        Tests the get names function to return a set.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
            df (pandas dataframe): Mock dataframe of tennis match history data.
        """
        names = elo.get_names(df)
        assert isinstance(names, set), f"get_names should return a set, instead returned {type(names)}"

    def test_logistic(self, elo):
        """
        Tests the logistic function to return a float

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        log = elo.logistic(1)
        assert isinstance(log, float), f"Logistic function should return a float, instead returned {type(log)}"

    def test_expected_game_score(self, elo):
        """
        Tests the inital elos function to return a float

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        game_score = elo.expected_game_score(float(1500), float(1500))
        assert isinstance(game_score, float), f"Logistic function should return a float, instead returned {type(game_score)}"

    def test_decay_factor(self, elo):
        """
        Tests the decay factor function to return a float

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        decay_rate = elo.decay_factor(2)
        assert isinstance(decay_rate, float), f"Decay factor should return a float, instead returned {type(decay_rate)}"

    def test_elo_calculation(self, elo, df, elo_df):
        """
        Tests the elo calculation function to return a dataframe

        Parameters:
            elo (class): An instance of the ELO class to be tested.
            df (pandas dataframe): Mock dataframe of tennis match history data.
            elo_df (pandas dataframe): Mock dataframe of player elo ratings.
        """
        elo_calc = elo.elo_calculation(df, elo_df)
        assert isinstance(elo_calc, pd.DataFrame), f"Elo calculation should return a dataframe, instead returned {type(elo_calc)}"

    def test_get_most_recent_age(self, elo, df):
        """
        Tests the get most recent age function to return a series

        Parameters:
            elo (class): An instance of the ELO class to be tested.
            df (pandas dataframe): Mock dataframe of tennis match history data.
        """
        recent_age = elo.get_most_recent_age(df)
        assert isinstance(recent_age, pd.Series), f"Get most recent age should return a series, instead returned {type(recent_age)}"

    def test_final_elo_csv(self, elo, tmp_path, df):
        """
        Tests the final elo csv function to create a csv in data.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
            tmp_path: A temporary directory path provided by pytest to store the generated CSV file.
            df (pandas dataframe): Mock dataframe of tennis match history data.
        """
        file_path = tmp_path / "player_elos.csv"

        elo.final_elo_csv(df, file_path=str(file_path))

        assert file_path.exists(), "The player_elos.csv file was not created"

    def test_expected_game_score_first_elo_type_error(self, elo):
        """
        Test that a TypeError is raised if first_elo is not a float.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="First ELO is not a float"):
            elo.expected_game_score(first_elo="2000", second_elo=1800.0, S=400)


    def test_expected_game_score_second_elo_type_error(self, elo):
        """
        Test that a TypeError is raised if second_elo is not a float.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="Second ELO is not a float"):
            elo.expected_game_score(first_elo=2000.0, second_elo="1800", S=400)


    def test_expected_game_score_scaling_factor_type_error(self, elo):
        """
        Test that a TypeError is raised if S is not an int.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="Scaling factor S must be an int"):
            elo.expected_game_score(first_elo=2000.0, second_elo=1800.0, S="400")

    def test_decay_factor_year_difftype_error(self, elo):
        """
        Test that a TypeError is raised if year_diff is not an int.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="The difference in years must be an int"):
            elo.decay_factor(year_diff="5", decay_rate=0.3)

    def test_decay_factor_decay_ratetype_error(self, elo):
        """
        Test that a TypeError is raised if year_diff is not an int.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="Decay rate must be an float"):
            elo.decay_factor(year_diff=5, decay_rate="0.3")

    def test_elo_calculation_invalid_data_type(self, elo):
        """
        Test that a TypeError is raised if 'data' is not a pandas DataFrame.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="data must be an pandas dataframe"):
            elo.elo_calculation(data="invalid_data", elo_df=pd.DataFrame(), K=20)


    def test_elo_calculation_invalid_elo_df_type(self, elo):
        """
        Test that a TypeError is raised if 'elo_df' is not a pandas DataFrame.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="ELO dataframe must be a pandas dataframe"):
            elo.elo_calculation(data=pd.DataFrame(), elo_df="invalid_elo_df", K=20)


    def test_elo_calculation_invalid_K_type(self, elo):
        """
        Test that a TypeError is raised if 'K' is not an integer.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
        """
        with pytest.raises(TypeError, match="Scaling factor K must be an int"):
            elo.elo_calculation(data=pd.DataFrame(), elo_df=pd.DataFrame(), K="invalid_K")

    def test_get_most_recent_age(self, elo, df):
        """
        Tests that the get_most_recent_age method returns a pandas Series with the correct player ages.

        Parameters:
            elo (class): An instance of the ELO class to be tested.
            df (pandas dataframe): Mock dataframe of tennis match history data.
        """
        recent_age = elo.get_most_recent_age(df)

        # Test that the result is a pandas Series
        assert isinstance(recent_age, pd.Series), f"Expected a pandas Series, but got {type(recent_age)}"
        
        expected_ages = {
            'Player_1': 26,
            'Player_3': 24,
            'Player_2': 27,
            'Player_4': 31, 
        }

        for player, expected_age in expected_ages.items():
            assert recent_age[player] == expected_age, f"Expected age for {player} is {expected_age}, but got {recent_age[player]}"

        