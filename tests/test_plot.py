import pytest
from unittest import mock
import pandas as pd
from plot import Plot
import matplotlib.pyplot as plt

@pytest.fixture
def plot():
    return Plot()

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
        # Call the plot function
        plot.plots('Wimbledon', 2023, [0.05, 0.1])

        # Check if a figure has been created by checking the current figure
        fig = plt.gcf()  # Get the current figure

        # Assert that the figure is an instance of a matplotlib Figure object
        assert isinstance(fig, plt.Figure), "No figure was created."

