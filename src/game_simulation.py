import numpy as np

def logistic(x):
    return 1 / (1 + 10**(-x))

def compute_prob_using_ELO(R_A, R_B):
    return logistic((R_A-R_B)/400)

#calculated the decayed winning probability in each set due to age factor
def compute_prob_in_sets(winning_prob, age, age_threshold):
    if age <= age_threshold:
        return [winning_prob for i in range(5)]
    else:
        return [winning_prob * (1 - i * (age - age_threshold)**2 / 1300) for i in range(5)]

def simulating_game(player_1, player_1_elo, player_1_age, player_2, player_2_elo, player_2_age):
    set_winner = []
    
    winning_prob_1 = compute_prob_using_ELO(player_1_elo, player_2_elo)
    winning_prob_2 = compute_prob_using_ELO(player_2_elo, player_1_elo)
    
    age_threshold = 27 #age from which endurance starts to fall
    
    winning_prob_1_in_sets = compute_prob_in_sets(winning_prob_1, player_1_age, age_threshold)
    winning_prob_2_in_sets = compute_prob_in_sets(winning_prob_2, player_2_age, age_threshold)
        
    for i in range(5):
        winning_prob_1_inthisset = winning_prob_1_in_sets[i] / (winning_prob_1_in_sets[i] + winning_prob_2_in_sets[i]) 
        if bool(np.random.uniform() < winning_prob_1_inthisset):
            set_winner.append(player_1)
        else:
            set_winner.append(player_2)
            
    if set_winner.count(player_1) >= 3:
        return player_1
    elif set_winner.count(player_2) >= 3:
        return player_2