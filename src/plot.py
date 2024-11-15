import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class Plot():
    """
    Plot class to plot models predicted tournament winner probabilities vs the betting odds probabilities.
    """
    def __init__(self, k_list = None):
        """
        Initializer for Plot class.

        Args:
            k_list (None or list): The list of different k factors used in the H2H model to calculate error rates for. This can be none if the H2H model is not being used.
        """
        self.bar_width = 0.3
        self.k_list = k_list
        if self.k_list is not None:
            for i, k in enumerate(self.k_list):
                setattr(self, f'k{i + 1}', k)
            self.hth = True
            self.bar_width = 0.15
        else:
            self.hth = False


    def plots(self, tournament_name, year):
        """
        Creates the plotting function comparing the model's winning probabilities against the betting odds.
        A side by side bar plot comparing the top 10 players according to the betting odds is plot against the 
        models probabilities. Saves plot to a png.

        Args:
            tournament_name (str): Name of tournament.
            year (int): Year tournament was played in.

        Outputs:
            A png file for the given tournament and probabilities of winning for top 10 players.

        Raises:
            ValueError: Year must be between 1968 and 2024.
            FileNotFoundError: One of the dataframes for the plotting function does not exist.
        """
        if not (1968 <= year <= 2024):
            raise ValueError(f"Invalid year: {year}. Year must be between 1968 and 2024.")

        tournament_name_underscore = tournament_name.replace(' ', '_')

        odds_file = f'../data/2023_{tournament_name_underscore}_Prob.csv'
        model_file = f'../data/tournament_results_{tournament_name_underscore}.csv'
        
        # Check for the odds file
        if not os.path.exists(odds_file):
            raise FileNotFoundError(f"Error: The odds file {odds_file} does not exist")
        
        # Check for the model file
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Error: The model results file {model_file} does not exist")
        
        # If files exist, proceed with the function logic
        odds_df = pd.read_csv(odds_file, index_col=0)
        model_df = pd.read_csv(model_file, index_col=0)
        
        csv_dict_k = {}
        if self.k_list is not None:
            for k in self.k_list:
                hth_file = f'../data/tournament_results_{tournament_name_underscore}_head_to_head_{k}.csv'
                
                # Check if head-to-head CSV exists for each k
                if not os.path.exists(hth_file):
                    raise FileNotFoundError(f"Error: The head-to-head file {hth_file} does not exist")
                csv_dict_k[k] = pd.read_csv(hth_file, index_col=0)

        # Renames incorrect player name from csv file.
        odds_df = odds_df.rename(index={'Felix Auger-Aliassime': 'Felix Auger Aliassime'})
    
        if tournament_name == 'Australian Open' and year == 2023:
            # He was injured hence did not play in the 2023 Australian Open
            odds_df = odds_df.drop(index='Nick Kyrgios')

        top_players = odds_df.nlargest(10, 'normalized_winning_probability')
        top_champions = top_players[['normalized_winning_probability']].join(model_df['Champion'], how='inner')

        x = np.arange(len(top_champions.index))  # The label locations, arranges based on the top champions.
        
        # If hth is true, also plot h2h model predicted probabilities.
        if self.hth is True:
            plt.bar(x - self.bar_width - self.bar_width/2, top_champions['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
            plt.bar(x - self.bar_width/2, top_champions['Champion'], width=self.bar_width, label='Model Win Probability', color='orange')
            for i, (model_name, model_df_hth) in enumerate(csv_dict_k.items()):
                top_champions_hth = top_players[['normalized_winning_probability']].join(model_df_hth['Champion'], how='inner')
                plt.bar(x + i * self.bar_width + self.bar_width/2, top_champions_hth['Champion'], width=self.bar_width, label=f'Model Win Head to Head k = {model_name} Probability')
        else:
            plt.bar(x - self.bar_width/2, top_champions['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
            plt.bar(x + self.bar_width/2, top_champions['Champion'], width=self.bar_width, label='Model Win Probability', color='orange')

        # Plot labels and saving figure
        plt.xlabel('Player Name')
        plt.ylabel('Probability of Winning Championship')
        plt.title(f'Comparison of Odds and Model Win Probabilities for {tournament_name}')
        plt.xticks(x, top_champions.index, rotation=60, fontsize=10)
        plt.legend()

        plt.tight_layout()
        plt.savefig(f'../imgs/{tournament_name_underscore}_plot.png', bbox_inches='tight')
        plt.show()