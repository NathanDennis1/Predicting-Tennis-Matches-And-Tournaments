import pandas as pd
import numpy as np
from scipy.stats import norm
import math

class InvalidTournamentError(ValueError):
        pass

class Simulation():
    def __init__(self, player_elos, S = 400):
        """
        Initializer for Plot class.

        Args:
            player_elos: Dataframe of player elo ratings
            S (int): Scale for difference in ELO ratings 
        """
        self.elo_df = player_elos
        self.tournament_name = None
        self.S = S
        self.win_per = pd.read_csv('../data/win_percentage.csv', index_col='Player_Name')
        self.games_played = pd.read_csv('../data/games_played_opponents.csv', index_col='Player_Name')    

    def logistic(self, x):
        """
        Creates logistic function used for ELO calculation.

        Args:
            x (float): number input for the log function

        Returns:
            Final calculation of log function with given number
        """
        return 1 / (1 + 10**(-x))

    def compute_prob_using_ELO(self, first_elo, second_elo):
        """
        Calculates expected game score based on the logistic function

        Args:
            first_elo (float): The first elo for a given team/player
            second_elo (float): The second elo for a given team/player
            S (int): Scaling factor

        Returns:
            Final calculation for an expected game score as a float.
        """
        return self.logistic((first_elo-second_elo)/self.S)
    
    def sigmoid(self, games_played, x_0=20, k=0.2):
        """
        Sigmoid function to adjust weight based on the number of games played.

        Args:
            games_played (int): Number of games played between 2 people
            x_0 (int): Midpoint of sigmoid function when sigmoid equals 0.5
            k (float): Steepness factor in sigmoid function
        
        Returns:
            Sigmoid calculation as a float.
        """
        return 1 / (1 + math.exp(-k * (games_played - x_0)))
    
    def adjusted_win_probability(self, P_A, P_head_to_head, games_played, x_0=20, k=0.3):
        """
        Calculate the adjusted win probability for Player A based on the sigmoid-weighted head-to-head record.
        
        Args:
            P_A: Probability played A beats player B
            P_head_to_head: Historical head-to-head winning percentage for player A
            games_played (int): Number of games played between played A and B
            x_0 (int): Midpoint of sigmoid function when sigmoid equals 0.5
            k (float): Steepness factor in sigmoid function
        
        Returns:
            Adjusted win probability for Player A
        """
        # Calculate the sigmoid adjustment factor based on games played
        adjustment_factor = self.sigmoid(games_played, x_0, k)
        
        # Calculate the adjusted win probability using the weighted average
        P_A_adjusted = (1 - adjustment_factor) * P_A + adjustment_factor * P_head_to_head
        
        return P_A_adjusted
    

    def compute_prob_in_sets(self, winning_prob, age, sets, surface):
        """
        Computes a players winning probability based off the number of sets in a match.

        Args:
            winning_prob (float): The initial winning probability for a given player
            age (float): The age of a player
            sets (int): The number of sets in a match
            surface (str): The surface of a given match

        Returns:
            List of winning probability for the number of sets.
        """

        if surface == 'Clay':
            decay_rate = 0.015
        else:
            decay_rate = 0.0075

        if age <= 25:
            factor =  1.0
        else:
            factor = math.exp(-decay_rate * (age-25))

        return [winning_prob * factor ** i for i in range(sets)]

        
    def simulating_game(self, player_1, player_1_elo, player_1_age, player_2, player_2_elo, player_2_age, num_sets, surface):
        """
        Computes a game in a tennis match

        Args:
            player_1 (str): Name of player 1
            player_1_elo (float): The surface ELO of player 1
            player_1_age (float): The age of player 1
            player_2 (str): Name of player 2
            player_2_elo (float): The surface ELO of player 2
            player_2_age (float): The age of player 2
            num_sets (int): Number of sets in a match
            surface (str): Surface of a match

        Returns:
            Player who won the match as a string.
        """   

        set_winner = []
        
        winning_prob_1 = self.compute_prob_using_ELO(player_1_elo, player_2_elo)

        past_head_to_head = self.win_per[player_1][player_2]
        past_games_played = self.games_played[player_1][player_2]

        winning_prob_1 = self.adjusted_win_probability(winning_prob_1, past_head_to_head, past_games_played)
        winning_prob_2 = 1 - winning_prob_1
        
        winning_prob_1_in_sets = self.compute_prob_in_sets(winning_prob_1, player_1_age, num_sets, surface)
        winning_prob_2_in_sets = self.compute_prob_in_sets(winning_prob_2, player_2_age, num_sets, surface)

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
        """
        Finds the initial draw of a tournament for grand slams in the tennis dataset.

        Args:
            data (pandas dataframe): Dataframe of scraped tennis data
            year (int): The year the match was played in
            tournament (str): Name of the tournament

        Returns:
            first_round_df (pandas dataframe): Dataframe of the first round matchup for given tournament.

        Raises:
            InvalidTournamentError: Description of related error, either not a grand slam or no data in dataframe.
                                    The initial draw must have 127 rows.
        """

        grand_slams = ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open']
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
        """
        Computes the matchups based on a list of winners from the previous round

        Args:
            winners (list): The list of players who won in the previous round of the tournament

        Returns:
            matchup_df (pandas dataframe): List of winning next round matchups for the tennis tournament
        """
        match = []
        for i in range(0, len(winners), 2):
            match.append([winners[i], winners[i+1]])
        matchup_df = pd.DataFrame(match, columns=['Player_1','Player_2'])
        return matchup_df


    def simulate_round(self, matchups, results, surface, round, num_sets):
        """
        Simulates the round of a tennis tournament

        Args:
            matchups (list): The matchups of the round in a tournament
            results (matrix): Matrix of tournament results
            surface (str): Name of the surface playing on.
            round (int): Round number in the tournament
            num_sets (int): Number of sets for a match

        Returns:
            winners (list): List of winners in a given round.
        """
        winners = []
        for _, matchup in matchups.iterrows():
            player_1 = matchup.iloc[0]
            player_1_age = self.elo_df.loc[player_1]['Player_age']
            player_1_elo = self.elo_df.loc[player_1][f'{surface}_ELO']

            player_2 = matchup.iloc[1]
            player_2_age = self.elo_df.loc[player_2]['Player_age']
            player_2_elo = self.elo_df.loc[player_2][f'{surface}_ELO']
            winner = self.simulating_game(player_1, player_1_elo, player_1_age, player_2, player_2_elo, player_2_age, num_sets, surface)
            if winner == player_1:
                results.loc[player_1,round] += 1
                winners.append(player_1)
            else:
                results.loc[player_2,round] += 1
                winners.append(player_2)
        return winners


    def simulate_tournament(self, initial_draw, surface, trials):
        """
        Simulates a tournament through the initial draws for the tournament.

        Args:
            initial_draw (list): The initial draw of player matchups in the tournament
            surface (str): Name of the surface playing on.
            trials (int): Number of times to simulate tournament

        Returns:
            Winners_data (pandas dataframe): Dataframe of probability to make a certain round in the tournament.
        """

        final_matrix = np.zeros((128, 8)) 

        players = pd.concat([initial_draw['Player_1'], initial_draw['Player_2']]).to_list()

        # This is whats used for the tournament simulation. The end_matrix stores the matrix value for
        # where each team ended, adding it to final_matrix.
        for _ in range(trials):
            matchup_current = initial_draw
            end_matrix = pd.DataFrame(np.zeros((128, 8)), index=players[:128])
            for round in range(0, 6):
                winners = self.simulate_round(matchup_current, end_matrix, surface, round, 5)
                matchup_current = self.matchups_gen(winners)
            round += 1
            final_winner = self.simulate_round(matchup_current, end_matrix, surface, round, 5)
            end_matrix.loc[final_winner,7] += 1
            final_matrix = final_matrix + end_matrix


        matrix_winners = final_matrix/trials

        column_names = ["Round_64", "Round_32", "Round_16", "Round_8", "Round_4", "Round_2", "Runner_up", "Champion"]
        Winners_data = pd.DataFrame(matrix_winners)
        Winners_data.columns = column_names

        self.tournament_name = self.tournament_name.replace(' ', '_')
        file_path = f'../data/tournament_results_{self.tournament_name}.csv'

        Winners_data.to_csv(file_path, index=True)

        return Winners_data
    
    def user_tournament_simulation(self, tennis_data, year, tournament_name, nsims):
        """
        Allows users to simulate tournament in one function. Utilizes all above methods to simulate tournament and
        saves the results to a final csv used for visualization and validation.

        Args:
            tennis_data (pandas dataframe): Dataframe of tennis data for given years.
            year (int): Year of tournament user wants to simulate
            tournament_name (str): The name of the tournament the user wants to simulate
            nsims (int): Number of tournament simulations

        Raises:
            InvalidTournamentError: User must enter a grand slam tournament
        """
        grand_slams = ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open']

        if tournament_name == 'Australian Open':
            surface = 'Hard'
        elif tournament_name == 'Roland Garros':
            surface = 'Clay'
        elif tournament_name == 'Wimbledon':
            surface = 'Grass'
        elif tournament_name == 'US Open':
            surface = 'Hard'
        else:
            raise InvalidTournamentError(f'Invalid tournament, must be a Grand Slam: One of ', {grand_slams})

        initial_draw = self.find_initial_draw(tennis_data, year, tournament_name)

        self.simulate_tournament(initial_draw, surface, nsims)