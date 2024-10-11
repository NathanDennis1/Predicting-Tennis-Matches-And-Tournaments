import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Plot():
    def __init__(self):
        pass

    def plots(self, tournament_name):

        tournament_name_underscore = tournament_name.replace(' ', '_')
        odds = pd.read_csv(f'../data/2023_{tournament_name_underscore}_Prob.csv', index_col=0)

        data_fr = pd.read_csv(f'../data/tournament_results_{tournament_name_underscore}.csv', index_col = 0)

        top_players = odds.nlargest(10, 'Normalized Winning Probability')
        top_champions = top_players[['Normalized Winning Probability']].join(data_fr['Champion'], how='inner')

        bar_width = 0.3
        x = np.arange(len(top_champions.index))  # The label locations

        plt.bar(x - bar_width/2, top_champions['Normalized Winning Probability'], width=bar_width, label='Odds Win Probability', color='blue')
        plt.bar(x + bar_width/2, top_champions['Champion'], width=bar_width, label='Model Win Probability', color='orange')

        plt.xlabel('Player Name')
        plt.ylabel('Probability')
        plt.title(f'Comparison of Odds and Model Win Probabilities for {tournament_name}')
        plt.xticks(x, top_champions.index, rotation=60, fontsize=10)
        plt.legend()

        plt.tight_layout()
        plt.savefig(f'../imgs/{tournament_name}_plot.png', bbox_inches='tight')
        plt.show()