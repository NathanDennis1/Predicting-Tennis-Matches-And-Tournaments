from simulation import Simulation
from get_tennis_data import GetTennisData
from elo_calculations import ELO
import pandas as pd

def main():
    player_elos = pd.read_csv('player_elos.csv', index_col = 'Player_Name')
    data = pd.read_csv('tennis_data.csv')

    elo = ELO()
    elo.final_elo_csv()

    #tennis_data = GetTennisData()

    #tennis_data.get_data()

    #simulation = Simulation(player_elos)

    #initial_draw = simulation.find_initial_draw(data, 2024, 'Australian Open')

    #results = simulation.simulate_tournament(initial_draw, 'Hard')

if __name__ == "__main__":
    results = main()