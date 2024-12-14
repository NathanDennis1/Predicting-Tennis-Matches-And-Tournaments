# Predicting Singles Tennis Matches and Tournaments

## Group Members:
Nathan Dennis, John Breedis, Yiming Chen (Team 19)

## Description & Content Overview

In this repository we present a singles tennis match tournament simulation library. There are 2 rating systems used in this project to predict tennis match tournaments including the well known ELO system and the SkillO system developed by us. Tournaments which can be simulated include the Wimbledon, Australian Open, Roland Garros, and US Open, where there are comparable betting odds to compare for the first 3 tournaments listed. Users can freely change parameter combinations in the ELO and SkillO formulas to develop their own predictions for these tournaments. The output of the predictions will be a dataframe corresponding to the predicted probability that a player makes it to a specific round in a tournament, where the last column is the probability they win the Championship.

All tournament simulation data can be found under the src folder. Instructions to run different python scripts are explained below, with deeper explanations regarding specific functions and inputs in the docs folder & related documentation in each python file. The objective of this code is to  simulate major grand slam tournaments and validate these results against betting odds.


### Prerequisites

Ensure you have met these requirements:

- Python 3.8 or higher
- `pip`
- Python libraries:
  - `matplotlib`
  - `numpy`
  - `pandas`
  - `pytest`
  - `requests`
  
### Installation Steps

1. **Clone the Repository**

You can clone our repository to your local machine by running:

```bash
git clone https://code.harvard.edu/AM215/final_19.git
```

2. **Navigate to directory**

Navigate into the project folder

```bash
cd src
```

## Directory Tree

Here we present the directory tree.

```bash
├── LICENSE
├── README.md
├── requirements.txt
├── .gitignore
├── data
├── imgs
├── docs
│   ├── Makefile
│   ├── make.bat
│   ├── build
│   │   ├── doctrees
│   │   └── html
│   └── source
│       ├── src.rst
│       ├── conf.py
│       ├── index.rst
│       └── modules.rst
├── src
│   ├── Odds_to_Prob.py
│   ├── __init__.py
│   ├── elo_calculations.py
│   ├── error_metrics.py
│   ├── get_tennis_data.py
│   ├── main.py
│   ├── past_matches.py
│   ├── plot.py
│   ├── simulation.py
│   ├── skillo_calculations.py
├── tests
│   ├── test_elo_calculations.py
│   ├── test_error_metrics.py
│   ├── test_get_tennis_data.py
│   ├── test_odds_to_prob.py
│   ├── test_past_matches.py
│   ├── test_plot.py
│   ├── test_simulation.py
│   └── test_skillo_calculations.py
```

## Python File Descriptions

In the following section we present descriptions of each python file.

#### get_tennis_data.py

To begin, you can obtain tennis match data between 1960 and 2024 through the `get_tennis_data.py` script under the GetTennisData class, which allows users to input a year interval between 1960 and 2024 to obtain tennis data. This data includes all relevant tournament match outcomes between the years, the winners and losers, their ages, the surface of the tournament, and the tournament level.

#### elo_calculations.py

Next, `elo_calculations.py` contains scripts to calculate ELO scores based on the data given from 'get_tennis_data'. Simply running the "final_elo_csv" function from the ELO class and input the tennis dataframe to output the ELO calculation dataframe for every player in the dataset, saving it to a csv file. Optionally run the function 'win_percentage_common_opponents' in 'past_match_data' to get the win percentage and games played for every player against the others across the dataset, saved in 2 csv files. The input for this function is only the tennis data.

#### simulation.py

To simulate tournaments, initiate the Simulation class with the arguments: elo dataframe for player elos, S (Scaling factor, default 800), hth (Boolean value if you want the model to include the head-to-head win percentage data), and K scaling factor for the head-to-head data. Before simulating the tournament, running 'simulation_params' with the win percentage and games played dataframe will include the head-to-head statistics for each player. To simulate tournaments, running 'user_tournament_simulation' with the inputs of the tennis data, year, tournament name, number of simulation, and saves (A boolean value to save the resulting simulation results to a csv). This will output a csv file named based on the tournament you are simulating, called  'tournament_results_{tournament_name}' where tournament_name is the name of the tournament. If head-to-head was true, the string '_head_to_head_{k}' with the scaling factor k would be in the csv files name at the end.

#### error_metrics.py

To display error metrics (RMSE, L1, and Linf scores), utilize the Odds_to_prob.py script and the function "convert_odds" inputting the year and tournament to create a csv file for the given odds based on the year and tournament. Running 'displayErrors' in the 'error_metrics.py' script will display the error scores across the given tournament input and optional k scaling factors for the head-to-head data. 

#### plot.py

To plot the data, use the 'plot.py' script and Plot class. Run the plots function with the input tournament, year, and optimal k scaling factors to include head-to-head model data in the plots.

#### main.py

A working example of this is in the 'main.py' script in src. This file runs everything from top to bottom and creates the plot/error metrics for a given tournament. To replicate this, navigate to the source code using 'cd src' in your terminal. Then run 'python main.py' to output the plot image and calculate error metrics.

We note that to fully utilize the plot and errors class, ensure you have the sufficient csv files created to do so when using the head-to-head data. You may need to run simulation multiple times for different head-to-head k factors before plotting and getting the error metrics.

**Test Cases**

To run test cases, you can run: 

```bash
PYTHONPATH=. pytest --cov=src -W ignore::DeprecationWarning -v tests/___.py
```

Where ___ would be the specific testing file you would like to run

