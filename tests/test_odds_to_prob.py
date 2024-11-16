import pytest
from src.Odds_to_Prob import Odds
import os

@pytest.fixture
def odds():
    return Odds()

class Test_odds_to_prob():
    """
    Class to test the Odds_to_Prob python script
    """

    def test_american_odds_to_probability_positive(self, odds):
        """
        Tests to ensure that given positive odds, the resulting probability is between 0 and 1
        """
        probability = odds.american_odds_to_probability(150)
        assert 0 < probability < 1, "Probability should be between 0 and 1 for positive odds"

    def test_american_odds_to_probability_negative(self, odds):
        """
        Tests to ensure that given negative odds, the resulting probability is between 0 and 1
        """
        probability = odds.american_odds_to_probability(-150)
        assert 0 < probability < 1, "Probability should be between 0 and 1 for negative odds"

    def test_convert_odds(self, odds):
        """
        Tests to check that a file is created for the convert_odds function. Since it doesn't specifically return a dataframe,
        we check to ensure the csv file it should create is created.
        """
        year = 2023
        tournament = 'Wimbledon'
        odds.convert_odds(year, tournament)

        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'{year}_{tournament.replace(" ", "_")}_Prob.csv')

        assert os.path.exists(file_path), f"File {file_path} does not exist."

