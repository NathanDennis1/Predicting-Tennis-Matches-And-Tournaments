import pytest
import pandas as pd
from src.error_metrics import Errors


@pytest.fixture
def error_metrics():
    return Errors()

class Test_error_metrics():
    def test_rmse_nonneg(self, error_metrics):
        """
        Tests if RMSE returns a non-negative value
        """
        rmse = error_metrics.RMSE(pd.Series(0.8), pd.Series(0.75))
        assert rmse >= 0, "RMSE should always be non-negative"

    def test_linf_nonneg(self, error_metrics):
        """
        Tests if linf returns a non-negative value
        """
        linf = error_metrics.Linf(pd.Series(0.8), pd.Series(0.75))
        assert linf >= 0, "L-Infinity should always be non-negative"

    def test_l1_nonneg(self, error_metrics):
        """
        Tests if l1 returns a non-negative value
        """
        l1 = error_metrics.L1(pd.Series(0.8), pd.Series(0.75))
        assert l1 >= 0, "L1 norm should always be non-negative"

    def test_rmse_float(self, error_metrics):
        """
        Tests if RMSE function returns a float
        """
        rmse = error_metrics.RMSE(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(rmse, float), f"RMSE should return a float, instead it returned {type(rmse)}"

    def test_linf_float(self, error_metrics):
        """
        Tests if linf function returns a float
        """
        linf = error_metrics.Linf(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(linf, float), f"RMSE should return a float, instead it returned {type(linf)}"

    def test_l1_float(self, error_metrics):
        """
        Tests if l1 function returns a float
        """
        l1 = error_metrics.L1(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(l1, float), f"RMSE should return a float, instead it returned {type(l1)}"
