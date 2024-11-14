import pytest
from Odds_to_Prob import Odds

@pytest.fixture
def odds():
    return Odds()

def test_american_odds_to_probability_positive(odds):
    probability = odds.american_odds_to_probability(150)
    assert 0 < probability < 1, "Probability should be between 0 and 1 for positive odds"

def test_american_odds_to_probability_negative(odds):
    probability = odds.american_odds_to_probability(-150)
    assert 0 < probability < 1, "Probability should be between 0 and 1 for negative odds"
