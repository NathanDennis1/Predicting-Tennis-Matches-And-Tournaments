import pandas as pd
import os

class InvalidTournamentError(ValueError):
        pass

class Odds():
    def __init__(self):
        pass

    def american_odds_to_probability(self, odds):
        """
        Creates function to convert odds to probabilities.

        Args:
            odds (float): number input for the given odds

        Returns:
            Final calculation of probability given american odds as a float.
        """
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return -odds / (-odds + 100)
    def get_project_root(self):
        """
        Returns the root directory of the project, which in our case is team_19. This was done
        so that the test_odds_to_prob.py test code would work.
        """
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def convert_odds(self, year, tournament):
        """
        Converts odds to probabilities based on the year and tournament. Creates the probability dataframe based on the given
        odds for a tournament in a year.

        Args:
            year (int): year of tournament
            tournament (str): Name of tournament

        Raises:
            TypeError: Inputs must both be floats, true and pred, raises error if not.
            InvalidTournamentError: Tournament must be a grand slam tournament, Australian Open, Roland Garros, Wimbledon, or US Open.
        """
        if not isinstance(year, int):
            raise TypeError(f"Year must be of type int, it is {type(year)}")
        if not isinstance(tournament, str):
            raise TypeError(f"The tournament must be a string, it is {type(tournament)}")
        
        grand_slams = ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open']
        if tournament not in grand_slams:
            raise InvalidTournamentError(f'Invalid tournament, must be a Grand Slam: One of ', {grand_slams})
        
        project_root = self.get_project_root()

        tournament = tournament.replace(' ', '_')

        odds_file = os.path.join(project_root, 'data', f'{year}_{tournament}_Odds.csv')

        # Check for the odds file
        if not os.path.exists(odds_file):
            raise FileNotFoundError(f"The odds file {odds_file} does not exist")
        
    
        odds_df = pd.read_csv(odds_file)

        odds_df['winning_probability'] = odds_df['Betting Odds'].apply(self.american_odds_to_probability) * 100

        total_probability = odds_df['winning_probability'].sum()
        odds_df['normalized_winning_probability'] = (odds_df['winning_probability'] / total_probability)

        data_directory = os.path.join(project_root, 'data')

        output_file = os.path.join(data_directory, f'{year}_{tournament}_Prob.csv')
        odds_df.to_csv(output_file, index=False)
