import requests
import pandas as pd
from io import StringIO

class GetTennisData():
    """
    Class to create dataframe from a dataset on github.
    """
    def __init__(self):
        """
        Initialize the GetTennisData class
        """
        self.base_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{}.csv"

    def get_data(self):
        """
        Reads data from github url and creates dataframe for each url.

        Args:
        url_list: List of url's to use in dataframe.

        Returns:
        Final dataframe across every github url
        """
        df_list = []
        for year in range(2000, 2024):  

            url = self.base_url.format(year)

            response = requests.get(url)

            df = pd.read_csv(StringIO(response.text))

            df['Year'] = year

            df_list.append(df)

        final_df = pd.concat(df_list)
        return final_df
    
    # TODO
    def save_data(self):
        pass


def main():
    
    tennisdata = GetTennisData()

    tennis_df = tennisdata.get_data()

    # Select relevent columns for analysis
    tennis_df = tennis_df[['tourney_name', 'surface', 'draw_size', 'tourney_level', 'best_of', 'winner_name', 'winner_hand', 'winner_ht', 'winner_age', 'loser_name', 'loser_hand', 'loser_ht', 'loser_age', 'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points', 'Year']]

    tennis_df = tennis_df.dropna()

    tennis_df = tennis_df[tennis_df['surface'] != 'Carpet']

    tennis_df.to_csv('tennis_data.csv', index=0)


if __name__ == "__main__":
    main()