from simulation import Simulation
from get_tennis_data import GetTennisData
from elo_calculations import ELO
from plot import Plot
from error_metrics import Errors
from Odds_to_Prob import Odds
from past_matches import past_match_data
from skillo_calculations import skillO
import pandas as pd

def main():
    tennis_data = GetTennisData()
    plot = Plot()
    error = Errors()
    elo = ELO(1500, 2023)
    skillo = skillO(initial_mean=25, initial_variance=8.3333, current_year=2023, beta = 1, year_decay = 1.1, gamma = 0.1)
    odds = Odds()
    matches = past_match_data()

    #tennis_data.get_data(year_lower = 2014, year_upper = 2024)
    data = pd.read_csv('../data/tennis_data.csv')

    skillo.final_csv(data, '../data/skillo_4.csv')
    skillo_df_4 = pd.read_csv('../data/skillo_4.csv', index_col = 'Player_Name')

    elo.final_elo_csv(data)
    player_elos = pd.read_csv('../data/player_elos.csv', index_col = 'Player_Name')

    simulation_1 = Simulation(skillo_df_4, 'skillO', beta = 1)
    simulation_1.user_tournament_simulation(data, 2023, 'Wimbledon', 5000, sim_num = '4', saves = True)
    simulation_1.user_tournament_simulation(data, 2023, 'Roland Garros', 5000, sim_num = '4', saves = True)
    simulation_1.user_tournament_simulation(data, 2023, 'Australian Open', 5000, sim_num = '4', saves = True)
    skillo_wimbledon = pd.read_csv(f'../data/tournament_results_Wimbledon_skillO_1.csv', index_col = 0)

    simulation_ELO = Simulation(player_elos, 'ELO', S = 800)
    simulation_ELO.user_tournament_simulation(data, 2023, 'Wimbledon', 5000, saves = True)
    ELO_wimbledon = pd.read_csv(f'../data/tournament_results_Wimbledon_ELO.csv', index_col = 0)


    print(error.displayErrors('SkillO', 'Wimbledon', '4'))
    print(error.displayErrors('SkillO', 'Roland Garros', '4'))
    print(error.displayErrors('SkillO', 'Australian Open', '4'))
    plot.plot_ELO_vs_SkillO('Wimbledon', 2023, '4')
    plot.plot_ELO_vs_SkillO('Roland Garros', 2023, '4')
    plot.plot_ELO_vs_SkillO('Australian Open', 2023, '4')
if __name__ == "__main__":
    results = main()