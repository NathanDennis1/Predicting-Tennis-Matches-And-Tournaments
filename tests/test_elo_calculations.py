import pytest
from elo_calculations import ELO

@pytest.fixture
def elo():
    return ELO(initial_elo_rating=1500)

def test_calculate_elo(elo):
    new_elo = elo.calculate_elo(elo_old=1500, opponent_elo=1600, result=1)
    assert new_elo > 1500, "ELO should increase when winning against a higher-rated opponent"

def test_simulate_elo(elo):
    elo.simulate_elo("Player A", "Player B", result=1)
    assert "Player A" in elo.elo_ratings and "Player B" in elo.elo_ratings, "Both players should be added to ratings"

def test_final_elo_csv(elo, tmp_path):
    elo.final_elo_csv()
    assert tmp_path.joinpath("player_elos.csv").exists(), "CSV file should be created with final ELO scores"
