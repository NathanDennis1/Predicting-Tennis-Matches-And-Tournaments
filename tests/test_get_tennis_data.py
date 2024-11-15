import pytest
from src.get_tennis_data import GetTennisData

@pytest.fixture
def tennis_data():
    return GetTennisData()

def test_get_data_type_error(tennis_data):
    with pytest.raises(Exception):
        tennis_data.get_data(year_lower="2000", year_upper=2024)

def test_get_data_value_error(tennis_data):
    with pytest.raises(SystemExit):
        tennis_data.get_data(year_lower=1960, year_upper=1970)
