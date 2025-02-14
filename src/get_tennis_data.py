import requests
import pandas as pd
from io import StringIO
import os
import sys

class GetTennisData():
    """
    Class to create dataframe from a dataset on github.
    """
    def __init__(self):
        """
        Initialize the GetTennisData class.
        """
        self.base_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{}.csv"

    def get_data(self, year_lower = 2000, year_upper = 2025):
        """
        Reads data from github url and creates dataframe across all the years input.

        Args:
            year_lower (int): The lower bound for the years you want data for. Default set to 2000
            year_upper (int): The upper bound (Exclusive) for the years you want data for. Default set to 2025

        Returns:
            Final dataframe across every github url for given years.

        Raises:
            Exception: Years must be integers
            ValueError: Year must be in specified range of possible data. Between 1968 to 2024 to lower year, 1969 to 2025 for upper.
        """

        if (type(year_lower) != int or type(year_upper) != int):
            raise Exception("This is not of type int (integer), you must input an int for years")

        try:
            if not (1968 <= year_lower <= 2024) or not (1969 <= year_upper <= 2025):
                raise ValueError("Year must be between 1968 and 2024 for the lower year, and between 1969 and 2025 for the upper year")
        except ValueError as e:
            print(e)
            sys.exit(1)

        df_list = []
        for year in range(year_lower, year_upper):  

            url = self.base_url.format(year)

            response = requests.get(url)

            df = pd.read_csv(StringIO(response.text))

            df['Year'] = year

            df_list.append(df)

        final_df = pd.concat(df_list)

        # Saved only columns we deemed relevant for analysis.
        final_df = final_df[['tourney_name', 'surface', 'draw_size', 'tourney_level', 'best_of', 
                   'winner_name', 'winner_age', 'loser_name', 'loser_age', 'Year']]
        
        final_df = final_df[final_df['surface'] != 'Carpet']
        
        final_df = final_df.dropna()

        output_dir = '../data'

        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        
        file_path = os.path.join(output_dir, 'tennis_data.csv')

        final_df.to_csv(file_path, index=0)

        return final_df
