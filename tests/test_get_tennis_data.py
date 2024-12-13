import pytest
import pandas as pd
from src.get_tennis_data import GetTennisData

@pytest.fixture
def tennis_data():
    """
    Class of tennis data to run tests. Returns tennis data class.
    """
    return GetTennisData()

def test_get_data_type_error(tennis_data):
    """
    Tests raising the type error of the lower year is not an integer.

    Parameters:
        tennis_data (class): An instance of the tennis_data class to be tested.
    """
    with pytest.raises(Exception):
        tennis_data.get_data(year_lower="2000", year_upper=2024)

def test_get_data_value_error(tennis_data):
    """
    Tests raising the type error of the upper year is not an integer.

    Parameters:
        tennis_data (class): An instance of the tennis_data class to be tested.
    """
    with pytest.raises(SystemExit):
        tennis_data.get_data(year_lower=1960, year_upper=1970)

def test_get_data_returns_dataframe(tennis_data):
    """
    Tests that the tennis class returns a dataframe for the get_data function.

    Parameters:
        tennis_data (class): An instance of the tennis_data class to be tested.
    """
    result_df = tennis_data.get_data(year_lower=2000, year_upper=2024)
    
    assert isinstance(result_df, pd.DataFrame), "The result is not a pandas DataFrame"

