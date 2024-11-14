import pytest
import pandas as pd
import numpy as np
from simulation import Simulation, InvalidTournamentError

@pytest.fixture
def player_elo_df():
    data = {
        'Player_Name': ['Player A', 'Player B', 'Player C', 'Player D'],
        'Hard_ELO': [1500, 1600, 1400, 1550],
        'Grass_ELO': [1520, 1580, 1380, 1560],
        'Clay_ELO': [1480, 1540, 1350, 1530],
        'Player_age': [25, 28, 22, 30]
    }
    return pd.DataFrame(data).set_index('Player_Name')

@pytest.fixture
def simulation(player_elo_df):
    return Simulation(player_elos=player_elo_df)

def test_compute_prob_using_elo(simulation):
    prob = simulation.compute_prob_using_ELO(1600, 1500)
    assert 0 <= prob <= 1, "Winning probability should be between 0 and 1"
    assert prob > 0.5, "Higher ELO should result in a higher winning probability"

def test_adjusted_win_probability(simulation):
    prob_adjusted = simulation.adjusted_win_probability(0.6, 0.65, 15)
    assert 0 <= prob_adjusted <= 1, "Adjusted probability should be between 0 and 1"
    assert prob_adjusted > 0.6, "Adjusted probability should increase with favorable head-to-head"

def test_compute_prob_in_sets(simulation):
    win_probs = simulation.compute_prob_in_sets(0.8, 30, 5, 'Clay')
    assert len(win_probs) == 5, "Should compute probabilities for the number of sets"
    assert all(0 <= p <= 1 for p in win_probs), "Probabilities should be between 0 and 1"

def test_simulating_game(simulation):
    winner = simulation.simulating_game("Player A", 1600, 25, "Player B", 1400, 30, 3, "Hard")
    assert winner == "Player A", "Higher ELO player should win with a large ELO gap"

def test_find_initial_draw(simulation):
    data = pd.DataFrame({'Year': [2023] * 127, 'tourney_name': ['Wimbledon'] * 127,
                         'winner_name': ['Player A'] * 64 + ['Player B'] * 63,
                         'loser_name': ['Player C'] * 64 + ['Player D'] * 63})
    draw_df = simulation.find_initial_draw(data, 2023, 'Wimbledon')
    assert len(draw_df) == 64, "Initial draw should contain 64 matchups"

def test_invalid_tournament_error(simulation):
    with pytest.raises(InvalidTournamentError):
        simulation.find_initial_draw(pd.DataFrame(), 2023, "Harvard")

def test_simulate_round(simulation):
    matchups = pd.DataFrame({'Player_1': ['Player A', 'Player C'], 'Player_2': ['Player B', 'Player D']})
    results = pd.DataFrame(0, index=['Player A', 'Player B', 'Player C', 'Player D'], columns=range(8))
    winners = simulation.simulate_round(matchups, results, "Hard", 1, 5)
    assert len(winners) == 2, "There should be two winners from two matchups"
    assert set(winners).issubset(['Player A', 'Player B', 'Player C', 'Player D']), "Winners should be from the original players"
