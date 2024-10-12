import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Plot():
    def __init__(self):
        """
        Initializer for Plot class.
        """
        self.bar_width = 0.3

    def plots(self, tournament_name, year):
        """
        Creates the plotting function comparing the model's winning probabilities against the betting odds.
        A side by side bar plot comparing the top 10 players according to the betting odds is plot against the 
        models probabilities. Saves plot to a png

        Args:
            tournament_name (str): Name of tournament.
            year (int): Year tournament was played in
        """

        tournament_name_underscore = tournament_name.replace(' ', '_')
        odds_df = pd.read_csv(f'../data/2023_{tournament_name_underscore}_Prob.csv', index_col=0)

        model_df = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}.csv', index_col = 0)

        # Renames incorrect player name from csv file.
        odds_df = odds_df.rename(index={'Felix Auger-Aliassime': 'Felix Auger Aliassime'})
    
        if tournament_name == 'Australian Open' and year == 2023:
            # He was injured hence did not play in the 2023 Australian Open
            odds_df = odds_df.drop(index='Nick Kyrgios')

        top_players = odds_df.nlargest(10, 'normalized_winning_probability')
        top_champions = top_players[['normalized_winning_probability']].join(model_df['Champion'], how='inner')

        x = np.arange(len(top_champions.index))  # The label locations, arranges based on the top champions.

        plt.bar(x - self.bar_width/2, top_champions['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
        plt.bar(x + self.bar_width/2, top_champions['Champion'], width=self.bar_width, label='Model Win Probability', color='orange')

        plt.xlabel('Player Name')
        plt.ylabel('Probability of Winning Championship')
        plt.title(f'Comparison of Odds and Model Win Probabilities for {tournament_name}')
        plt.xticks(x, top_champions.index, rotation=60, fontsize=10)
        plt.legend()

        plt.tight_layout()
        plt.savefig(f'../imgs/{tournament_name_underscore}_plot.png', bbox_inches='tight')
        plt.show()