import pytest
from src.Odds_to_Prob import Odds
import os

@pytest.fixture
def odds():
    """
    Class of odds to probability to run tests. Returns Odds class.
    """
    return Odds()

class Test_odds_to_prob():
    """
    Class to test the Odds_to_Prob python script.
    """
    def test_american_odds_to_probability_positive(self, odds):
        """
        Tests to ensure that given positive odds, the resulting probability is between 0 and 1.

        Parameters:
            odds (class): An instance of the Odds class to be tested.
        """
        probability = odds.american_odds_to_probability(150)
        assert 0 < probability < 1, "Probability should be between 0 and 1 for positive odds"

    def test_american_odds_to_probability_negative(self, odds):
        """
        Tests to ensure that given negative odds, the resulting probability is between 0 and 1.

        Parameters:
            odds (class): An instance of the Odds class to be tested.
        """
        probability = odds.american_odds_to_probability(-150)
        assert 0 < probability < 1, "Probability should be between 0 and 1 for negative odds"

    def test_convert_odds(self, odds):
        """
        Tests to check that a file is created for the convert_odds function. Since it doesn't specifically return a dataframe,
        we check to ensure the csv file it should create is created.

        Parameters:
            odds (class): An instance of the Odds class to be tested.
        """
        year = 2023
        tournament = 'Wimbledon'
        odds.convert_odds(year, tournament)

        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'{year}_{tournament.replace(" ", "_")}_Prob.csv')

        assert os.path.exists(file_path), f"File {file_path} does not exist."

    def test_invalid_year_type(self, odds):
        """
        Test that TypeError is raised when year is not an integer for convert_odds function.

        Parameters:
            odds (class): An instance of the Odds class to be tested.
        """
        with pytest.raises(TypeError):
            odds.convert_odds("2022", "Australian Open")  # passing a string instead of an integer for year

    def test_invalid_tournament_type(self, odds):
        """
        Test that TypeError is raised when tournament is not a string for convert_odds function.

        Parameters:
            odds (class): An instance of the Odds class to be tested.
        """
        with pytest.raises(TypeError):
            odds.convert_odds(2022, 1234)  # passing an integer instead of a string for tournament

