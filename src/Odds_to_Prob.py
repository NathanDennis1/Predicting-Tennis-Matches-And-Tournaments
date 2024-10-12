import pandas as pd

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
        """
        tournament = tournament.replace(' ', '_')
        odds_df = pd.read_csv(f'../data/{year}_{tournament}_Odds.csv')

        odds_df['winning_probability'] = odds_df['Betting Odds'].apply(self.american_odds_to_probability) * 100

        total_probability = odds_df['winning_probability'].sum()
        odds_df['normalized_winning_probability'] = (odds_df['winning_probability'] / total_probability)

        odds_df.to_csv(f'../data/{year}_{tournament}_Prob.csv', index=False)
