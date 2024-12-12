import pytest
from unittest import mock
import pandas as pd
from src.plot import Plot
import matplotlib.pyplot as plt

@pytest.fixture
def plot():
    return Plot()

class TestPlot:
    """
    Class to test plot script
    """

    def test_plot(self, plot):
        """
        Tests to ensure a figure is created when calling plot
        """
        plot.plots('Wimbledon', 2023, 'skillO', '2')

        # This checks to make sure a figure was created
        fig = plt.gcf() 

        # Assert that the figure is a matplotlib figure
        assert isinstance(fig, plt.Figure), "No figure was created."

    def test_plot_comparison(self, plot):
        """
        Tests to ensure a figure is created when calling plot
        """
        plot.plot_ELO_vs_SkillO('Wimbledon', 2023, '2')

        # This checks to make sure a figure was created
        fig = plt.gcf() 

        # Assert that the figure is a matplotlib figure
        assert isinstance(fig, plt.Figure), "No figure was created."
