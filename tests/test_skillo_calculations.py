import pytest
from src.skillo_calculations import skillO
import os
import pandas as pd

@pytest.fixture
def skillo():
    """
    Created SkillO class for testing

    Returns:
        Instance of SkillO class.
    """
    return skillO(initial_mean=25, initial_variance = 8.333, current_year = 2023)

@pytest.fixture
def df():
    """
    Mock dataframe with arbitrary player names.

    Returns:
        Mock dataframe as a pandas dataframe.
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
        'Year': [2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023, 2023, 2023]}

    final_df = pd.DataFrame(data)
    
    return final_df

@pytest.fixture
def player_skillo_df():
    """
    Creates mock player SkillO dataset

    Returns:
        Mock dataframe of tennis players SkillO ratings, given random SkillO ratings and ages.
    """
    skillo_data = {
        'Player_Name': ['Player_1', 'Player_2', 'Player_3', 'Player_4' ],
        'Hard_mean': [25, 24.5, 25.4, 25.8],
        'Clay_mean': [24.5, 25.5, 25.2, 25.9],
        'Grass_mean': [24.9, 23.9, 25.1, 26.1],
        'Hard_variance': [2.33, 1.5, 1.8, 1.7],
        'Clay_variance': [2.33, 1.5, 1.8, 1.7],
        'Grass_variance': [2.33, 1.5, 1.8, 1.7],
        'Player_age': [26, 28, 24, 30]
    }

    skillo_df = pd.DataFrame(skillo_data)

    skillo_df = skillo_df.set_index('Player_Name')
    
    return skillo_df
    
class Test_skillo_calculations():
    """
    Class to test the SkillO_calculations script.
    """
    def test_initial_skillO(self, skillo):
        """
        Tests the inital skillo function to return a dataframe.

        Parameters:
            skillo (class): An instance of the SkillO class to be tested.
        """
        surfaces = ['Clay', 'Hard']
        names = ['Player', 'Player_2']
        skillo_df = skillo.initial_skills(surfaces, names)
        assert isinstance(skillo_df, pd.DataFrame), f"skillo_df should return a dataframe, instead returned {type(skillo_df)}"

    def test_expected_game_score(self, skillo):
        """
        Tests the expected game score function to return a float.

        Parameters:
            skillo (class): An instance of the SkillO class to be tested.
        """
        game_score = skillo.expected_game_score(float(25), float(24.5), float(5.2), float(5.4))
        assert isinstance(game_score, float), f"Logistic function should return a float, instead returned {type(game_score)}"

    def test_skillo_calculation(self, skillo, df, player_skillo_df):
        """
        Tests the skillo calculation function to return a dataframe.

        Parameters:
            skillo (class): An instance of the SkillO class to be tested.
        """
        skillo_calc = skillo.skillO_calculation(df, player_skillo_df)
        assert isinstance(skillo_calc, pd.DataFrame), f"SkillO calculation should return a dataframe, instead returned {type(skillo_calc)}"

    def test_final_skillo_csv(self, skillo, tmp_path, df):
        """
        Tests the final skillo csv function to create a csv in data..

        Parameters:
            skillo (class): An instance of the SkillO class to be tested.
            tmp_path: A temporary directory path provided by pytest to store the generated CSV file.
            df (pandas dataframe): Mock dataframe of tennis match history data.
        """
        file_path = tmp_path / "skillo.csv"

        skillo.final_csv(df, file_path=str(file_path))

        assert file_path.exists(), "The skillo.csv file was not created"
