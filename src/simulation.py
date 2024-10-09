import pandas as pd
import numpy as np

class InvalidTournamentError(ValueError):
        pass

class Simulation():
    def __init__(self, player_elos):
        self.elo_df = player_elos
        self.tournament_name = None

    def logistic(self, x):
        return 1 / (1 + 10**(-x))

    def compute_prob_using_ELO(self, R_A, R_B):
        return self.logistic((R_A-R_B)/800)
    

    def compute_prob_in_sets(self, winning_prob, age, age_threshold1, age_threshold2, games_played):
        if age <= age_threshold1:
            return [winning_prob * ( 2/3 * np.exp(-1/(1+(games_played/20)**2)) +1/3) for i in range(5)]
        else:
            return [winning_prob * ( 2/3 * np.exp(-1/(1+(games_played/20)**2)) +1/3) * 
                    (1 - (age - age_threshold1)**2 / ((age_threshold2 - age_threshold1)**2 + (age - age_threshold1)**2) * i/5) for i in range(5)]
        
    def simulating_game(self, player_1, player_1_elo, player_1_age, player_1_games_played, player_2, player_2_elo, player_2_age, player_2_games_played, num_sets):
        set_winner = []
        
        winning_prob_1 = self.compute_prob_using_ELO(player_1_elo, player_2_elo)
        winning_prob_2 = self.compute_prob_using_ELO(player_2_elo, player_1_elo)
        
        age_threshold1 = 27 #age from which endurance starts to fall
        age_threshold2 = 34 #age at which winning probability decay 50% in the last set
        
        winning_prob_1_in_sets = self.compute_prob_in_sets(winning_prob_1, player_1_age, age_threshold1, age_threshold2, player_1_games_played)
        winning_prob_2_in_sets = self.compute_prob_in_sets(winning_prob_2, player_2_age, age_threshold1, age_threshold2, player_2_games_played)
            
        for i in range(num_sets):
            winning_prob_1_inthisset = winning_prob_1_in_sets[i] / (winning_prob_1_in_sets[i] + winning_prob_2_in_sets[i])
            if bool(np.random.uniform() < winning_prob_1_inthisset):
                set_winner.append(player_1)
            else:
                set_winner.append(player_2)
                
        if set_winner.count(player_1) >= int(num_sets/2)+1:
            return player_1
        elif set_winner.count(player_2) >= int(num_sets/2)+1:
            return player_2


    def find_initial_draw(self, data, year, tournament):
        grand_slams = ['Australian Open', 'French Open', 'Wimbledon', 'US Open']
        if tournament not in grand_slams:
            raise InvalidTournamentError(f'Invalid tournament, must be a Grand Slam: One of ', {grand_slams})

        
        tournament_results = data[(data['Year'] == year) & (data['tourney_name'] == tournament)]

        if len(tournament_results) != 127:
            raise InvalidTournamentError(f'Incomplete Tournament results in data')

        first_round = tournament_results.head(64).apply(lambda row: [row['winner_name'], row['loser_name']], axis=1).tolist()
        first_round_df = pd.DataFrame(first_round, columns=['Player_1','Player_2'])
        self.tournament_name = tournament
        return first_round_df


    def matchups_gen(self, winners):
        match = []
        for i in range(0, len(winners), 2):
            match.append([winners[i], winners[i+1]])
        matchup_df = pd.DataFrame(match, columns=['Player_1','Player_2'])
        return matchup_df


    def simulate_round(self, matchups, results, surface, round, num_sets):
        winners = []
        for _, matchup in matchups.iterrows():
            player_1 = matchup.iloc[0]
            player_1_age = self.elo_df.loc[player_1]['Player_age']
            player_1_games_played = self.elo_df.loc[player_1]['Games_played']
            player_1_elo = self.elo_df.loc[player_1][f'{surface}_ELO']

            player_2 = matchup.iloc[1]
            player_2_age = self.elo_df.loc[player_2]['Player_age']
            player_2_games_played = self.elo_df.loc[player_2]['Games_played']
            player_2_elo = self.elo_df.loc[player_2][f'{surface}_ELO']
            winner = self.simulating_game(player_1, player_1_elo, player_1_age, player_1_games_played, player_2, player_2_elo, player_2_age, player_2_games_played, num_sets)
            if winner == player_1:
                results.loc[player_1,round] += 1
                winners.append(player_1)
            else:
                results.loc[player_2,round] += 1
                winners.append(player_2)
        return winners


    def simulate_tournament(self, inital_draw, surface):

        final_matrix = np.zeros((128, 8)) 

        players = pd.concat([inital_draw['Player_1'], inital_draw['Player_2']]).to_list()

        trials = 1000

        # This is whats used for the tournament simulation. The end_matrix stores the matrix value for
        # where each team ended, adding it to final_matrix.
        for _ in range(trials):
            matchup_current = inital_draw
            end_matrix = pd.DataFrame(np.zeros((128, 8)), index=players[:128])
            for round in range(0, 6):
                winners = self.simulate_round(matchup_current, end_matrix, surface, round, 5)
                matchup_current = self.matchups_gen(winners)
            round += 1
            final_winner = self.simulate_round(matchup_current, end_matrix, surface, round, 5)
            end_matrix.loc[final_winner,7] += 1
            final_matrix = final_matrix + end_matrix


        matrix_W = final_matrix/trials

        # Creates the dataframe that I submit.
        column_names = ["Round_64", "Round_32", "Round_16", "Round_8", "Round_4", "Round_2", "Runner_up", "Champion"]
        W_data = pd.DataFrame(matrix_W)
        W_data.columns = column_names

        file_path = f'../data/tournament_results_{self.tournament_name}.csv'

        W_data.to_csv(file_path, index=True)

        return W_data