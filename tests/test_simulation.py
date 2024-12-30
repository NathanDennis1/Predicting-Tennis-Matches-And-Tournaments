import pytest
import pandas as pd
import numpy as np
from src.simulation import Simulation
import os

# We begin by reading the ORIGINAL data from the csv files to test the simulate full tournament code.

@pytest.fixture
def original_tennis_data():
    """
    Obtains original tennis data.

    Returns:
        Dataframe of tennis data.

    Raises:
        FileNotFoundError: File was not found in data folder.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tennis_data.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")

    tennis_df = pd.read_csv(data_path)

    return tennis_df

@pytest.fixture
def original_player_elo_df():
    """
    Obtains original player elo dataframe.

    Returns:
        Dataframe of player elos data.

    Raises:
        FileNotFoundError: File was not found in data folder.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'player_elos.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")

    elo_df = pd.read_csv(data_path, index_col = 'Player_Name')

    return elo_df

@pytest.fixture
def original_player_skillo_df():
    """
    Obtains original player SkillO dataframe.

    Returns:
        Dataframe of player SkillO ratings data.

    Raises:
        FileNotFoundError: File was not found in data folder.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'skillo_2.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")

    skillo_df = pd.read_csv(data_path, index_col = 'Player_Name')

    return skillo_df

@pytest.fixture
def original_win_pct_df():
    """
    Obtains original win percentage dataframe.

    Returns:
        Dataframe of win percentage for players in original data.

    Raises:
        FileNotFoundError: File was not found in data folder.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'win_percentage.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")

    Pct_df = pd.read_csv(data_path, index_col = 'Player_Name')

    return Pct_df

@pytest.fixture
def original_games_played_df():
    """
    Obtains original games played dataframe.

    Returns:
        Dataframe of games played for players in original data.

    Raises:
        FileNotFoundError: File was not found in data folder.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'games_played_opponents.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")

    games_play_df = pd.read_csv(data_path, index_col = 'Player_Name')

    return games_play_df

@pytest.fixture
def original_simulation(original_player_elo_df):
    """
    Initializes original simulation class with original players.
    """
    return Simulation(rating_df=original_player_elo_df, rating_system = 'ELO')

@pytest.fixture
def original_simulation_skillO(original_player_skillo_df):
    """
    Initializes original simulation class with original players.
    """
    return Simulation(rating_df=original_player_skillo_df, rating_system = 'SkillO')


# This is for the mock data.

@pytest.fixture
def tennis_data():
    """
    Creates mock tennis dataset.

    Returns:
        Mock dataframe of fake tennis players.
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
        'loser_age': [28, 30, 25, 29, 30, 27, 29, 25, 28, 30],
        'Year': [2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023]}

    final_df = pd.DataFrame(data)

    return final_df

@pytest.fixture
def player_elo_df():
    """
    Creates mock player elo dataset.

    Returns:
        Mock dataframe of tennis players elo ratings, given random elo ratings and ages.
    """
    elo_data = {
        'Player_Name': ['Player_1', 'Player_2', 'Player_3', 'Player_4' ],
        'Hard_ELO': [1505.12, 1492.34, 1510.75, 1489.90],
        'Clay_ELO': [1489.56, 1503.67, 1490.85, 1500.12],
        'Grass_ELO': [1502.23, 1487.90, 1506.12, 1493.40],
        'Player_age': [26, 28, 24, 30]
    }

    elo_df = pd.DataFrame(elo_data)

    elo_df = elo_df.set_index('Player_Name')

    return elo_df

@pytest.fixture
def player_skillo_df():
    """
    Creates mock player skillo dataset.

    Returns:
        Mock dataframe of tennis players skillo ratings, given random skillo ratings and ages.
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

@pytest.fixture
def win_pct_df():
    """
    Creates mock tennis dataset for win percentage, using random values for players.

    Returns:
        Mock dataframe of tennis players win percentages
    """
    players = ['Player_1', 'Player_2', 'Player_3', 'Player_4']

    win_pct_data = {
        'Player_1': [0, 0.2, 0.4, 0.6],
        'Player_2': [0.8, 0, 0, 0.4],
        'Player_3': [0.6, 1, 0, 0.5],
        'Player_4': [0.4, 0.6, 0.5, 0]}


    Pct_df = pd.DataFrame(win_pct_data, index=players)

    return Pct_df

@pytest.fixture
def games_played_df():
    """
    Creates mock tennis dataset for games played

    Returns:
        Mock dataframe of tennis players games played
    """
    players = ['Player_1', 'Player_2', 'Player_3', 'Player_4']

    games_played_data = {
        'Player_1': [0, 5, 5, 5],
        'Player_2': [5, 0, 2, 5],
        'Player_3': [5, 2, 0, 4],
        'Player_4': [5, 5, 4, 0]}

    gp_df = pd.DataFrame(games_played_data, index=players)

    return gp_df

@pytest.fixture
def simulation(player_elo_df):
    """
    Creates simulation class for mock player elo ratings.
    """
    return Simulation(rating_df=player_elo_df, rating_system = 'ELO')

@pytest.fixture
def simulation_skillo(player_skillo_df):
    """
    Creates simulation class for mock player skillo ratings.
    """
    return Simulation(rating_df=player_skillo_df, rating_system = 'skillO')

class Test_simulation():
    """
    Test simulation class to test various simulation functions.
    """
    def test_compute_prob_using_elo(self, simulation):
        """
        Tests compute probability using elo function, checks probability is between 0 and 1 and higher ELO has higher win probability.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        prob = simulation.compute_prob_using_ELO(1600, 1500)
        assert 0 <= prob <= 1, "Winning probability should be between 0 and 1"
        assert prob > 0.5, "Higher ELO should result in a higher winning probability"

    def test_adjusted_win_probability(self, simulation):
        """
        Tests adjusted win probability function, probability is between 0 and 1 and adjusted probability is higher for favorite based on head-to-head.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        prob_adjusted = simulation.adjusted_win_probability(0.6, 0.65, 15)
        assert 0 <= prob_adjusted <= 1, "Adjusted probability should be between 0 and 1"
        assert prob_adjusted > 0.6, "Adjusted probability should increase with favorable head-to-head"

    def test_compute_prob_in_sets(self, simulation):
        """
        Tests compute probability in sets, ensures it returns a list of length 5 and all probabilities are between 0 and 1.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        win_probs = simulation.compute_prob_in_sets(0.8, 30, 5, 'Clay')
        assert len(win_probs) == 5, "Should compute probabilities for the number of sets"
        assert all(0 <= p <= 1 for p in win_probs), "Probabilities should be between 0 and 1"

    def test_simulating_game_elo(self, simulation, win_pct_df, games_played_df):
        """
        Tests simulating game function, ensures a string is returned for the winner alongside incorporating win percentage and games played.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
            win_pct_df (pd dataframe): Win percentage dataframe.
            games_played_df (pd dataframe): Games played dataframe.
        """
        simulation.simulation_params(win_pct_df, games_played_df)
        winner = simulation.simulating_game("Player_1", float(25), "Player_2", float(30), 3, "Hard")
        assert isinstance(winner, str), "Returns string"

    def test_simulating_game_skillo(self, simulation_skillo):
        """
        Tests simulating game function, ensures a string is returned for the winner.

        Parameters:
            simulation_skillo (class): An instance of the Simulation class to be tested using SkillO.
        """
        winner = simulation_skillo.simulating_game("Player_1", float(25), "Player_2", float(30), 3, "Hard")
        assert isinstance(winner, str), "Returns string"

    def test_find_initial_draw(self, simulation):
        """
        Tests finding initial draw, ensures initial draw is of length 64 for grand slam tournaments.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        data = pd.DataFrame({'Year': [2023] * 127, 'tourney_name': ['Wimbledon'] * 127,
                            'winner_name': ['Player A'] * 64 + ['Player B'] * 63,
                            'loser_name': ['Player C'] * 64 + ['Player D'] * 63})
        draw_df = simulation.find_initial_draw(data, 2023, 'Wimbledon')
        assert len(draw_df) == 64, "Initial draw should contain 64 matchups"

    def test_simulate_round(self, simulation, win_pct_df, games_played_df):
        """
        Tests simulate round function. Ensures the length of winners is correct and the set of winners is a subset of the original players.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
            win_pct_df (pd dataframe): Win percentage dataframe.
            games_played_df (pd dataframe): Games played dataframe.
        """
        matchups = pd.DataFrame({'Player_1': ['Player_2', 'Player_3'], 'Player_2': ['Player_3', 'Player_4']})
        results = pd.DataFrame(0, index=['Player_1', 'Player_2', 'Player_3', 'Player_4'], columns=range(8))
        simulation.simulation_params(win_pct_df, games_played_df)
        winners = simulation.simulate_round(matchups, results, "Hard", 1, 5)
        assert len(winners) == 2, "There should be two winners from two matchups"
        assert set(winners).issubset(['Player_1', 'Player_2', 'Player_3', 'Player_4']), "Winners should be from the original players"

    def test_simulate_tournament(self, original_simulation, original_win_pct_df, original_games_played_df, original_tennis_data):
        """
        Tests simulate tournament functin with original data. Ensures output is a dataframe.

        Parameters:
            original_simulation (class): An instance of the Simulation class to be tested.
            original_win_pct_df (pd dataframe): Original in percentage dataframe.
            original_games_played_df (pd dataframe): Original games played dataframe.
            original_tennis_data (pd dataframe): Original tennis dataframe.
        """
        original_simulation.simulation_params(original_win_pct_df, original_games_played_df)
        draw = original_simulation.find_initial_draw(original_tennis_data, 2023, 'Wimbledon')
        tournament = original_simulation.simulate_tournament(draw, 'Grass', 1, False)
        assert isinstance(tournament, pd.DataFrame), "Not df"

    def test_simulating_game_type_error_player_1_string(self, simulation):
        """
        Test that TypeError is raised when player 1's name is not a string.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The first player has to be a string"):
            simulation.simulating_game(1, float(25), "Player_2", float(30), 3, "Hard")

    def test_simulating_game_type_error_player_2_string(self, simulation):
        """
        Test that TypeError is raised when player 2's name is not a string.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The second player has to be a string"):
            simulation.simulating_game("Player_1", float(25), 2, float(30), 3, "Hard")

    def test_simulating_game_type_error_player_1_age(self, simulation):
        """
        Test that TypeError is raised when player 1's age is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The first players age has to be a float"):
            simulation.simulating_game("Player_1", 'Age', "Player_2", float(30), 3, "Hard")

    def test_simulating_game_type_error_player_2_age(self, simulation):
        """
        Test that TypeError is raised when player 2's age is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The second players age has to be a float"):
            simulation.simulating_game("Player_1", float(25), "Player_2", 'age', 3, "Hard")

    def test_simulate_round_skillo(self, simulation_skillo):
        """
        Tests simulate round function. Ensures the length of winners is correct and the set of winners is a subset of the original players.

        Parameters:
            simulation_skillo (class): An instance of the Simulation class to be tested using SkillO.
        """
        matchups = pd.DataFrame({'Player_1': ['Player_2', 'Player_3'], 'Player_2': ['Player_3', 'Player_4']})
        results = pd.DataFrame(0, index=['Player_1', 'Player_2', 'Player_3', 'Player_4'], columns=range(8))
        winners = simulation_skillo.simulate_round(matchups, results, "Hard", 1, 5)
        assert len(winners) == 2, "There should be two winners from two matchups"
        assert set(winners).issubset(['Player_1', 'Player_2', 'Player_3', 'Player_4']), "Winners should be from the original players"

    def test_simulating_mock_game_type_error_player_1_elo_float(self, simulation):
        """
        Test that TypeError is raised when player 1's elo rating is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The first player's elo rating has to be a float"):
            simulation.simulating_mock_game_ELO("2312.2", float(25), 1253.0, float(30), 3, "Hard")

    def test_simulating_mock_game_type_error_player_1_elo_float(self, simulation):
        """
        Test that TypeError is raised when player 2's elo rating is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The second player's elo rating has to be a float"):
            simulation.simulating_mock_game_ELO(1235.2, float(25), "2351.2", float(30), 3, "Hard")

    def test_simulating_mock_game_type_error_player_1_age(self, simulation):
        """
        Test that TypeError is raised when player 1's age is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The first players age has to be a float"):
            simulation.simulating_mock_game_ELO(1234.2, 'Age', 2352.5, float(30), 3, "Hard")

    def test_simulating_mock_game_type_error_player_2_age(self, simulation):
        """
        Test that TypeError is raised when player 2's age is not a float.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        with pytest.raises(TypeError, match="The second players age has to be a float"):
            simulation.simulating_mock_game_ELO(1234.2, float(25), 2345.6, 'age', 3, "Hard")

    def test_simulating_mock_game_elo(self, simulation):
        """
        Tests simulating mock game function, ensures a string is returned for the winner.

        Parameters:
            simulation (class): An instance of the Simulation class to be tested.
        """
        winner = simulation.simulating_mock_game_ELO(1234.2, float(25), 2352.2, float(30), 3, "Hard")
        assert isinstance(winner, str), "Returns string"