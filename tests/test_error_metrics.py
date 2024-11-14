import pytest
from error_metrics import Errors

@pytest.fixture
def error_metrics():
    return Errors()

def test_rmse(error_metrics):
    rmse = error_metrics.RMSE(0.8, 0.75)
    assert rmse >= 0, "RMSE should always be non-negative"

def test_linf(error_metrics):
    linf = error_metrics.Linf(0.8, 0.75)
    assert linf >= 0, "L-Infinity should always be non-negative"

def test_l1(error_metrics):
    l1 = error_metrics.L1(0.8, 0.75)
    assert l1 >= 0, "L1 norm should always be non-negative"
