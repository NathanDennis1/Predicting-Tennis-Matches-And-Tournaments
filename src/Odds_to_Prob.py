import pandas as pd

# Function to convert American odds to implied probability
def american_odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)

# Load the CSV file into a DataFrame
df = pd.read_csv('2024_US_Odds.csv')

# Add a new column for implied winning probability (before normalization)
df['Winning Probability'] = df['Betting Odds'].apply(american_odds_to_probability) * 100

# Normalize the probabilities so they sum to 100%
total_probability = df['Winning Probability'].sum()
df['Normalized Winning Probability'] = (df['Winning Probability'] / total_probability)

# Export the modified DataFrame to a new CSV file
df.to_csv('2024_US_Prob.csv', index=False)
