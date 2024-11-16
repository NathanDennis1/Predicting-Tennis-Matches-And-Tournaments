from simulation import Simulation
from get_tennis_data import GetTennisData
from elo_calculations import ELO
from plot import Plot
from error_metrics import Errors
from Odds_to_Prob import Odds
from past_matches import past_match_data
import pandas as pd

def main():
    tennis_data = GetTennisData()
    plot = Plot()
    error = Errors()
    elo = ELO(1500, 2023)
    odds = Odds()
    matches = past_match_data()

    tennis_data.get_data(year_lower = 2014, year_upper = 2024)

    data = pd.read_csv('../data/tennis_data.csv')

    elo.final_elo_csv(data)

    player_elos = pd.read_csv('../data/player_elos.csv', index_col = 'Player_Name')

    matches.win_percentage_common_opponents(data)

    win_percentage_df = pd.read_csv('../data/win_percentage.csv', index_col='Player_Name')

    games_played = pd.read_csv('../data/games_played_opponents.csv', index_col='Player_Name')

    simulation = Simulation(player_elos, S = 800, hth = True, k = 0.1)

    simulation.simulation_params(win_percentage_df, games_played)
    simulation.user_tournament_simulation(data, 2023, 'Australian Open', 5000, saves = True)

    odds.convert_odds(2023, 'Australian Open')

    plot.plots('Australian Open', 2023, [0.05, 0.1, 0.5])

    error.displayErrors('Australian Open', [0.05, 0.1, 0.5])




if __name__ == "__main__":
    results = main()