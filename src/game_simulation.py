import numpy as np

def logistic(x):
    return 1 / (1 + 10**(-x))

def compute_prob_using_ELO(R_A, R_B):
    return logistic((R_A-R_B)/800)

#Calculating the decayed winning probability in each set due to age factor
#We use Hill function to model the decay of winning probability in the last set due to age factor
#and we let the decay to be linear among 5 sets
#We also add a discount to winning probability based on the number of games that a player have played
#to nerf those inexperienced (since we set their ELO to be the baseline value 1500)
#the function we choose is a modified version of bump function
def compute_prob_in_sets(winning_prob, age, age_threshold1, age_threshold2, games_played):
    if age <= age_threshold1:
        return [winning_prob * ( 2/3 * np.exp(-1/(1+(games_played/20)**2)) +1/3) for i in range(5)]
    else:
        return [winning_prob * ( 2/3 * np.exp(-1/(1+(games_played/20)**2)) +1/3) * (1 - (age - age_threshold1)**2 / ((age_threshold2 - age_threshold1)**2 + (age - age_threshold1)**2) * i/5) for i in range(5)]

def simulating_game(player_1, player_1_elo, player_1_age, player_1_games_played, player_2, player_2_elo, player_2_age, player_2_games_played, num_sets):
    set_winner = []
    
    winning_prob_1 = compute_prob_using_ELO(player_1_elo, player_2_elo)
    winning_prob_2 = compute_prob_using_ELO(player_2_elo, player_1_elo)
    
    age_threshold1 = 27 #age from which endurance starts to fall
    age_threshold2 = 34 #age at which winning probability decay 50% in the last set
    
    winning_prob_1_in_sets = compute_prob_in_sets(winning_prob_1, player_1_age, age_threshold1, age_threshold2, player_1_games_played)
    winning_prob_2_in_sets = compute_prob_in_sets(winning_prob_2, player_2_age, age_threshold1, age_threshold2, player_2_games_played)
        
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