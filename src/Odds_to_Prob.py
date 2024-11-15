import pandas as pd

class InvalidTournamentError(ValueError):
        pass

class Odds():
    def __init__(self):
        pass

    def american_odds_to_probability(self,odds):
        """
        Creates function to convert odds to probabilities

        Args:
            odds (float): number input for the given odds

        Returns:
            Final calculation of probability given american odds as a float.
        """
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return -odds / (-odds + 100)

    def convert_odds(self, year, tournament):
        """
        Converts odds to probabilities based on the year and tournament.

        Args:
            year (int): year of tournament
            tournament (str): Name of tournament

        Returns:
            Final calculation of log function with given number

        Raises:
            TypeError: Inputs must both be floats, true and pred, raises error if not.
            InvalidTournamentError: Tournament must be a grand slam tournament.
        """
        if not isinstance(year, int):
            raise TypeError(f"Year must be of type int, it is {type(year)}")
        if not isinstance(tournament, str):
            raise TypeError(f"The tournament must be a string, it is {type(tournament)}")
        
        grand_slams = ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open']
        if tournament not in grand_slams:
            raise InvalidTournamentError(f'Invalid tournament, must be a Grand Slam: One of ', {grand_slams})
        
        tournament = tournament.replace(' ', '_')
        odds_df = pd.read_csv(f'../data/{year}_{tournament}_Odds.csv')

        odds_df['winning_probability'] = odds_df['Betting Odds'].apply(self.american_odds_to_probability) * 100

        total_probability = odds_df['winning_probability'].sum()
        odds_df['normalized_winning_probability'] = (odds_df['winning_probability'] / total_probability)

        odds_df.to_csv(f'../data/{year}_{tournament}_Prob.csv', index=False)
