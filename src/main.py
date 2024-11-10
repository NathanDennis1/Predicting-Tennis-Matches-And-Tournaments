from simulation import Simulation
from get_tennis_data import GetTennisData
from elo_calculations import ELO
from plot import Plot
from error_metrics import Errors
from Odds_to_Prob import Odds
import pandas as pd

def main():
    tennis_data = GetTennisData()
    plot = Plot()
    error = Errors()
    elo = ELO(1500)
    odds = Odds()

    tennis_data.get_data(year_lower = 2014, year_upper = 2024)

    elo.final_elo_csv()

    player_elos = pd.read_csv('../data/player_elos.csv', index_col = 'Player_Name')
    data = pd.read_csv('../data/tennis_data.csv')

    simulation = Simulation(player_elos, S = 800)

    simulation.user_tournament_simulation(data, 2023, 'Wimbledon', 5000)

    odds.convert_odds(2023, 'Wimbledon')

    plot.plots('Wimbledon', 2023)

    error.displayErrors('Wimbledon')




if __name__ == "__main__":
    results = main()