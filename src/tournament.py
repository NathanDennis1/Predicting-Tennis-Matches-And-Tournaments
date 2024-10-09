import pandas as pd
import numpy as np


class Tournament():
    def __init__(self):
        pass


    def convert_elo_to_pair_probabilities(self, elo_df, surface='Grass', S=600):
        """
        Converts ELO scores from a DataFrame to a matrix of pairwise winning probabilities.

        Args:
        elo_df: A DataFrame containing ELO scores with player names as index and surfaces as columns.
        surface: The surface being played on ('Grass', 'Clay', 'Hard').
        S: The scaling factor for ELO scores.

        Returns:
        A DataFrame of pairwise winning probabilities with player names as both index and columns.
        """
        
        # Check if the surface column exists in the DataFrame, if not tell user it doesn't exist
        if f"{surface}_ELO" not in elo_df.columns:
            raise ValueError(f"Surface '{surface}' not found in DataFrame columns. Make sure the spelling is correct and capitalize the first letter.")

        # Extract ELO scores for the specified surface
        elo_scores = elo_df[f"{surface}_ELO"].values
        
        # Create an empty matrix to store the probabilities
        probabilities = np.zeros((len(elo_scores), len(elo_scores)))

        # Calculate the probability of each player winning against each other player
        for i in range(len(elo_scores)):
            probabilities[i, i] = 0.5  # Each player has a 50% chance against themselves
            
            for j in range(i + 1, len(elo_scores)):
                # Calculate the expected score difference
                expected_score_diff = (elo_scores[i] - elo_scores[j]) / S
                
                # Calculate the probability of player i winning
                probability_i = 1 / (1 + 10**(-expected_score_diff))
                
                # Set the probabilities for both i vs j and j vs i
                probabilities[i, j] = probability_i
                probabilities[j, i] = 1 - probability_i

        # Create a DataFrame for better visualization
        probability_df = pd.DataFrame(probabilities, index=elo_df.index, columns=elo_df.index)
        
        return probability_df
    

def main():
    pass


if __name__ == "__main__":
    main()