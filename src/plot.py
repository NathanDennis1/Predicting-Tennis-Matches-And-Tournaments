import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class Plot():
    """
    Plot class to plot models predicted tournament winner probabilities vs the betting odds probabilities.
    """
    def __init__(self):
        """
        Initializer for Plot class.
        """
        self.bar_width = 0.3

    def get_project_root(self):
        """
        Returns the root directory of the project, which in our case is team_19. This was done
        so that the test_plot.py test code would work.
        """
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def plots(self, tournament_name, year, rating_system, simulation_num = None, k_list = None):
        """
        Creates the plotting function comparing the model's winning probabilities against the betting odds.
        A side by side bar plot comparing the top 10 players according to the betting odds is plot against the 
        models probabilities. Saves plot to a png.

        Args:
            tournament_name (str): Name of tournament.
            year (int): Year tournament was played in.
            k_list (None or list): The list of different k factors used in the H2H model to calculate error rates for. This can be none if the H2H model is not being used.

        Outputs:
            A png file for the given tournament and probabilities of winning for top 10 players.

        Raises:
            ValueError: Year must be between 1968 and 2024. Year must also be of type int. If k_list is not None, then it must be a list.
            FileNotFoundError: One of the dataframes for the plotting function does not exist.
        """
        if not isinstance(year, int):
            raise TypeError(f"Year must be of type int, it is {type(year)}")
        
        if not (1968 <= year <= 2024):
            raise ValueError(f"Invalid year: {year}. Year must be between 1968 and 2024.")
        
        self.k_list = k_list
        if self.k_list is not None:
            if not isinstance(k_list, list):
                raise ValueError("k_list must be a list")
            
            assert len(k_list) <= 3, f"The k_list must be at most length 3, it was {len(k_list)}"
            for i, k in enumerate(self.k_list):
                setattr(self, f'k{i + 1}', k)
            self.hth = True
            self.bar_width = 0.15

        else:
            self.hth = False

        tournament_name_underscore = tournament_name.replace(' ', '_')

        project_root = self.get_project_root()

        odds_file = os.path.join(project_root, 'data', f'2023_{tournament_name_underscore}_Prob.csv')
        if simulation_num is not None:
            model_file = os.path.join(project_root, 'data', f'tournament_results_{tournament_name_underscore}_{rating_system}_{simulation_num}.csv')
        else:
            model_file = os.path.join(project_root, 'data', f'tournament_results_{tournament_name_underscore}_{rating_system}.csv')

        # Check for the odds file
        if not os.path.exists(odds_file):
            raise FileNotFoundError(f"The odds file {odds_file} does not exist")
        
        # Check for the model file
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"The model results file {model_file} does not exist")
        
        # Reads in dataframes for odds and model
        odds_df = pd.read_csv(odds_file, index_col=0)
        model_df = pd.read_csv(model_file, index_col=0)
        
        csv_dict_k = {}
        if self.k_list is not None:
            for k in self.k_list:
                hth_file = os.path.join(project_root, 'data', f'tournament_results_{tournament_name_underscore}_head_to_head_{k}.csv')
                
                # Check if head-to-head CSV exists for each k
                if not os.path.exists(hth_file):
                    raise FileNotFoundError(f"The head-to-head file {hth_file} does not exist")
                csv_dict_k[k] = pd.read_csv(hth_file, index_col=0)

        # Renames incorrect player name from csv file.
        odds_df = odds_df.rename(index={'Felix Auger-Aliassime': 'Felix Auger Aliassime'})
    
        if tournament_name == 'Australian Open' and year == 2023:
            # He was injured hence did not play in the 2023 Australian Open
            odds_df = odds_df.drop(index='Nick Kyrgios')

        top_players = odds_df.nlargest(10, 'normalized_winning_probability')
        top_champions = top_players[['normalized_winning_probability']].join(model_df['Champion'], how='inner')

        x = np.arange(len(top_champions.index))  # The label locations, arranges based on the top champions.
        
        # If hth is true, also plot h2h model predicted probabilities. If not, skip the extra bars.
        if self.hth is True:
            plt.bar(x - self.bar_width - self.bar_width/2, top_champions['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
            plt.bar(x - self.bar_width/2, top_champions['Champion'], width=self.bar_width, label='Baseline Model Win Probability', color='orange')
            for i, (model_name, model_df_hth) in enumerate(csv_dict_k.items()):
                top_champions_hth = top_players[['normalized_winning_probability']].join(model_df_hth['Champion'], how='inner')
                plt.bar(x + i * self.bar_width + self.bar_width/2, top_champions_hth['Champion'], width=self.bar_width, label=f'Model Win Head to Head k = {model_name} Probability')
        else:
            plt.bar(x - self.bar_width/2, top_champions['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
            plt.bar(x + self.bar_width/2, top_champions['Champion'], width=self.bar_width, label='Baseline Model Win Probability', color='orange')

        # Plot labels and saving figure
        plt.xlabel('Player Name')
        plt.ylabel('Probability of Winning Championship')
        plt.title(f'Comparison of Odds and Model Win Probabilities for {tournament_name}')
        plt.xticks(x, top_champions.index, rotation=60, fontsize=10)
        plt.legend()

        plt.tight_layout()
        imgs_dir = os.path.join(project_root, 'imgs')
        plt.savefig(os.path.join(imgs_dir, f'{tournament_name_underscore}_plot.png'), bbox_inches='tight')
        plt.show()



    def plot_ELO_vs_SkillO(self, tournament_name, year, simulation_num = None):
        """
        Creates plot to compare ELO and SkillO simulation compared to betting odds as a side by side bar plot for the top 10 players
        according to betting odds.

        Args:
            tournament_name (str): Name of tournament.
            year (int): Year tournament was played in.
            simulation_num (None or int): Simulation number for title. Default set to None.

        Outputs:
            A png file for the given tournament and probabilities of winning for top 10 players.

        Raises:
            ValueError: Year must be between 1968 and 2024. Year must also be of type int. If k_list is not None, then it must be a list.
            FileNotFoundError: One of the dataframes for the plotting function does not exist.
        """
        self.bar_width = 0.2
        self.simulation_num = simulation_num

        if not isinstance(year, int):
            raise TypeError(f"Year must be of type int, it is {type(year)}")
        
        if not (1968 <= year <= 2024):
            raise ValueError(f"Invalid year: {year}. Year must be between 1968 and 2024.")

        tournament_name_underscore = tournament_name.replace(' ', '_')

        project_root = self.get_project_root()

        odds_file = os.path.join(project_root, 'data', f'2023_{tournament_name_underscore}_Prob.csv')
        model_file_ELO = os.path.join(project_root, 'data', f'tournament_results_{tournament_name_underscore}_ELO.csv')
        model_file_SkillO = os.path.join(project_root, 'data', f'tournament_results_{tournament_name_underscore}_SkillO_{simulation_num}.csv')

        # Check for the odds file
        if not os.path.exists(odds_file):
            raise FileNotFoundError(f"The odds file {odds_file} does not exist")
        
        # Check for the model file
        if not os.path.exists(model_file_ELO):
            raise FileNotFoundError(f"The model results file {model_file_ELO} does not exist")
        
        # Reads in dataframes for odds and model
        odds_df = pd.read_csv(odds_file, index_col=0)
        model_df_ELO = pd.read_csv(model_file_ELO, index_col=0)
        model_df_SkillO = pd.read_csv(model_file_SkillO, index_col=0)
        

        # Renames incorrect player name from csv file.
        odds_df = odds_df.rename(index={'Felix Auger-Aliassime': 'Felix Auger Aliassime'})
    
        if tournament_name == 'Australian Open' and year == 2023:
            # He was injured hence did not play in the 2023 Australian Open
            odds_df = odds_df.drop(index='Nick Kyrgios')

        top_players = odds_df.nlargest(10, 'normalized_winning_probability')
        top_champions_ELO = top_players[['normalized_winning_probability']].join(model_df_ELO['Champion'], how='inner')
        top_champions_SkillO = top_players[['normalized_winning_probability']].join(model_df_SkillO['Champion'], how='inner')

        x = np.arange(len(top_champions_ELO.index))  # The label locations, arranges based on the top champions.
        
        # If hth is true, also plot h2h model predicted probabilities. If not, skip the extra bars.
        plt.bar(x - self.bar_width, top_champions_ELO['normalized_winning_probability'], width=self.bar_width, label='Odds Win Probability', color='blue')
        plt.bar(x, top_champions_ELO['Champion'], width=self.bar_width, label='ELO Model Win Probability', color='orange')
        plt.bar(x + self.bar_width, top_champions_SkillO['Champion'], width=self.bar_width, label='SkillO Model Win Probability', color='green')

        # Plot labels and saving figure
        plt.xlabel('Player Name')
        plt.ylabel('Probability of Winning Championship')

        if self.simulation_num is not None:
            plt.title(f'Comparison of Odds vs SkillO and ELO Model Win Probabilities for {tournament_name}\nSimulation #{self.simulation_num}', fontsize=10)
        else:
            plt.title(f'Comparison of Odds vs SkillO and ELO Model Win Probabilities for {tournament_name}', fontsize=10)
        plt.xticks(x, top_champions_ELO.index, rotation=60, fontsize=10)
        plt.legend()

        plt.tight_layout()
        imgs_dir = os.path.join(project_root, 'imgs')
        if self.simulation_num is not None:
            plt.savefig(os.path.join(imgs_dir, f'{tournament_name_underscore}_plot_comparison_simulation_{self.simulation_num}.png'), bbox_inches='tight')
        else:
            plt.savefig(os.path.join(imgs_dir, f'{tournament_name_underscore}_plot_comparison.png'), bbox_inches='tight')
        plt.show()