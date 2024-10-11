from simulation import Simulation
from get_tennis_data import GetTennisData
from elo_calculations import ELO
from plot import Plot
import pandas as pd

def main():
    player_elos = pd.read_csv('../data/player_elos.csv', index_col = 'Player_Name')
    data = pd.read_csv('../data/tennis_data.csv')


    tennis_data = GetTennisData()
    plot = Plot()

    tennis_data.get_data(year_lower = 2010, year_upper = 2024)

    elo = ELO()
    elo.final_elo_csv()

    simulation = Simulation(player_elos)

    initial_draw = simulation.find_initial_draw(data, 2023, 'Roland Garros')

    results = simulation.simulate_tournament(initial_draw, 'Clay')

    plot.plots('Roland Garros')



if __name__ == "__main__":
    results = main()