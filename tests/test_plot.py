import pytest
from unittest import mock
import pandas as pd
from src.plot import Plot
import matplotlib.pyplot as plt

@pytest.fixture
def plot():
    """
    Class for plot to run tests. Returns Plot class.
    """
    return Plot()

class TestPlot:
    """
    Class to test plot script
    """
    def test_plot(self, plot):
        """
        Tests to ensure a figure is created when calling plots.

        Parameters:
            plot (class): An instance of the Plot class to be tested.
        """
        plot.plots('Wimbledon', 2023, 'skillO', '2')

        # This checks to make sure a figure was created
        fig = plt.gcf() 

        # Assert that the figure is a matplotlib figure
        assert isinstance(fig, plt.Figure), "No figure was created."

    def test_plot_comparison(self, plot):
        """
        Tests to ensure a figure is created when calling plot_ELO_vs_SkillO.

        Parameters:
            plot (class): An instance of the Plot class to be tested.
        """
        plot.plot_ELO_vs_SkillO('Wimbledon', 2023, '2')

        # This checks to make sure a figure was created
        fig = plt.gcf() 

        # Assert that the figure is a matplotlib figure
        assert isinstance(fig, plt.Figure), "No figure was created."
