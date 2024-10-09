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

    def get_data(self, year_lower = 2000, year_upper = 2025):
        """
        Reads data from github url and creates dataframe for each url.

        Args:
        url_list: List of url's to use in dataframe.

        Returns:
        Final dataframe across every github url
        """
        df_list = []
        for year in range(year_lower, year_upper):  

            url = self.base_url.format(year)

            response = requests.get(url)

            df = pd.read_csv(StringIO(response.text))

            df['Year'] = year

            df_list.append(df)

        final_df = pd.concat(df_list)

        final_df = final_df[['tourney_name', 'surface', 'draw_size', 'tourney_level', 'best_of', 
                   'winner_name', 'winner_age', 'loser_name', 'loser_age', 'Year']]
        
        final_df = final_df[final_df['surface'] != 'Carpet']
        
        final_df = final_df.dropna()

        file_path = f'../data/tennis_data.csv'

        final_df.to_csv(file_path, index=0)
