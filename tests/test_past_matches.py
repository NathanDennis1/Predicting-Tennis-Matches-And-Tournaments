import pytest
import pandas as pd
from src.past_matches import past_match_data  # Replace with the actual import path

@pytest.fixture
def sample_data():
    """
    Creates a sample dataset to test the win_percentage_common_opponents method.

    Returns:
        Sample data as a dataframe.
    """
    # Create a simple dataframe with match data
    data = {
        'winner_name': ['Player_1', 'Player_2', 'Player_1', 'Player_3', 'Player_3'],
        'loser_name': ['Player_2', 'Player_3', 'Player_3', 'Player_1', 'Player_2'],
    }
    return pd.DataFrame(data)

class TestPastMatchData:
    
    @pytest.fixture
    def past_match(self):
        """
        Fixture to create an instance of past_match_data for each test function.
        """
        return past_match_data()
    
    def test_return_type(self, past_match, sample_data):
        """
        Test that the return type is a tuple of two DataFrames.

        Parameters:
            past_match (class): An instance of the past_match_data class to be tested.
        """
        win_percentage_df, games_played_df = past_match.win_percentage_common_opponents(sample_data)
        
        assert isinstance(win_percentage_df, pd.DataFrame), f"Expected win_percentage_df to be a DataFrame, but got {type(win_percentage_df)}"
        assert isinstance(games_played_df, pd.DataFrame), f"Expected games_played_df to be a DataFrame, but got {type(games_played_df)}"
    
    def test_index_names(self, past_match, sample_data):
        """
        Test that both dataframes have 'Player_Name' as the index name.

        Parameters:
            past_match (class): An instance of the past_match_data class to be tested.
            sample_data (pd dataframe): Mock pandas dataframe to be tested.
        """
        win_percentage_df, games_played_df = past_match.win_percentage_common_opponents(sample_data)
        
        assert 'Player_Name' in win_percentage_df.index.names, "win_percentage_df should have 'Player_Name' as index name"
        assert 'Player_Name' in games_played_df.index.names, "games_played_df should have 'Player_Name' as index name"

    def test_data_integrity(self, past_match, sample_data):
        """
        Test that the values in the dataframes are correct given mock data ensuring that win percentages and games played are right.

        Parameters:
            past_match (class): An instance of the past_match_data class to be tested.
            sample_data (pd dataframe): Mock pandas dataframe to be tested.
        """
        win_percentage_df, games_played_df = past_match.win_percentage_common_opponents(sample_data)
        
        assert win_percentage_df['Player_1']['Player_2'] == 1.0, "Expected Player_1 to have 100% win rate against Player_2"
        assert win_percentage_df.loc['Player_2', 'Player_3'] == 0.5, "Expected Player_2 to have 50% win rate against Player_3"
        
        assert games_played_df.loc['Player_1', 'Player_2'] == 1, "Expected Player_1 and Player_2 to have played 2 games"
        assert games_played_df.loc['Player_2', 'Player_3'] == 2, "Expected Player_2 and Player_3 to have played 1 game"

