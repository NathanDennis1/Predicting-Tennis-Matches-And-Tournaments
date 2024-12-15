import pytest
import pandas as pd
from unittest.mock import patch
from src.error_metrics import Errors


@pytest.fixture
def error_metrics():
    """
    Initializes Errors class to be tested
    """
    return Errors()

class Test_error_metrics():
    def test_rmse_nonneg(self, error_metrics):
        """
        Tests if RMSE returns a non-negative value.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        rmse = error_metrics.RMSE(pd.Series(0.8), pd.Series(0.75))
        assert rmse >= 0, "RMSE should always be non-negative"

    def test_linf_nonneg(self, error_metrics):
        """
        Tests if linf returns a non-negative value.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        linf = error_metrics.Linf(pd.Series(0.8), pd.Series(0.75))
        assert linf >= 0, "L-Infinity should always be non-negative"

    def test_l1_nonneg(self, error_metrics):
        """
        Tests if l1 returns a non-negative value.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        l1 = error_metrics.L1(pd.Series(0.8), pd.Series(0.75))
        assert l1 >= 0, "L1 norm should always be non-negative"

    def test_rmse_float(self, error_metrics):
        """
        Tests if RMSE function returns a float.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        rmse = error_metrics.RMSE(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(rmse, float), f"RMSE should return a float, instead it returned {type(rmse)}"
    
    def test_rmse_type_error_true(self, error_metrics):
        """
        Test that RMSE raises TypeError if the 'true' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.RMSE([0.8, 0.9], pd.Series([0.75, 0.85])) 

    def test_rmse_type_error_pred(self, error_metrics):
        """
        Test that RMSE raises TypeError if the 'pred' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.RMSE(pd.Series([0.8, 0.9]), [0.75, 0.85])

    def test_linf_float(self, error_metrics):
        """
        Tests if Linf function returns a float.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        linf = error_metrics.Linf(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(linf, float), f"RMSE should return a float, instead it returned {type(linf)}"

    def test_linf_type_error_true(self, error_metrics):
        """
        Test that Linf raises TypeError if the 'true' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.Linf([0.8, 0.9], pd.Series([0.75, 0.85])) 

    def test_linf_type_error_pred(self, error_metrics):
        """
        Test that Linf raises TypeError if the 'pred' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.Linf(pd.Series([0.8, 0.9]), [0.75, 0.85])

    def test_l1_float(self, error_metrics):
        """
        Tests if l1 function returns a float.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        l1 = error_metrics.L1(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(l1, float), f"RMSE should return a float, instead it returned {type(l1)}"

    def test_l1_type_error_true(self, error_metrics):
        """
        Test that l1 raises TypeError if the 'true' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.L1([0.8, 0.9], pd.Series([0.75, 0.85])) 

    def test_l1_type_error_pred(self, error_metrics):
        """
        Test that l1 raises TypeError if the 'pred' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.L1(pd.Series([0.8, 0.9]), [0.75, 0.85])

    def test_MAPE_float(self, error_metrics):
        """
        Tests if MAPE function returns a float.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        MAPE = error_metrics.MAPE(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(MAPE, float), f"MAPE should return a float, instead it returned {type(MAPE)}"

    def test_MAPE_type_error_true(self, error_metrics):
        """
        Test that MAPE raises TypeError if the 'true' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.MAPE([0.8, 0.9], pd.Series([0.75, 0.85])) 

    def test_MAPE_type_error_pred(self, error_metrics):
        """
        Test that MAPE raises TypeError if the 'pred' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.MAPE(pd.Series([0.8, 0.9]), [0.75, 0.85])

    def test_R_squared_float(self, error_metrics):
        """
        Tests if R_squared function returns a float.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        R_sq = error_metrics.R_squared(pd.Series(0.8), pd.Series(0.75))
        assert isinstance(R_sq, float), f"R_squared should return a float, instead it returned {type(R_sq)}"

    def test_R_squared_type_error_true(self, error_metrics):
        """
        Test that R_squared raises TypeError if the 'true' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.R_squared([0.8, 0.9], pd.Series([0.75, 0.85])) 

    def test_R_squared_type_error_pred(self, error_metrics):
        """
        Test that R_squared raises TypeError if the 'pred' argument is not a pandas Series.

        Parameters:
            error_metrics (class): An instance of the Errors class to be tested.
        """
        with pytest.raises(TypeError):
            error_metrics.R_squared(pd.Series([0.8, 0.9]), [0.75, 0.85])

    @patch('pandas.read_csv') 
    def test_display_errors_returns_dataframe(self, mock_read_csv, error_metrics):
        """
        Test that displayErrors returns a pandas DataFrame and ensures that the `read_csv` function
        is properly mocked to simulate reading data.

        Parameters:
            mock_read_csv (MagicMock): The mocked version of `pandas.read_csv`, which is 
                                       used to simulate the behavior of reading CSV files 
                                       without actually accessing the file.
            error_metrics (class): An instance of the error_metrics class to be tested.
        """
        # Prepare mock data
        mock_odds_data = pd.DataFrame({
            'normalized_winning_probability': [0.8, 0.75, 0.65]
        })
        
        mock_model_data = pd.DataFrame({
            'Champion': [1, 2, 1]  # Mocked model predictions (Champion)
        })
        
        # Set the mock read_csv return values
        mock_read_csv.side_effect = [mock_odds_data, mock_model_data, mock_model_data]  # Assuming 3 calls to read_csv

        # Call the displayErrors method with mocked inputs
        result_df = error_metrics.displayErrors(
            rating_system="ELO",
            tournament_name="Australian Open"
        )

        # Test that the result is a DataFrame
        assert isinstance(result_df, pd.DataFrame), f"Expected a DataFrame, but got {type(result_df)}"

        # Test that the DataFrame contains the expected columns
        expected_columns = ['Model', 'RMSE', 'Linf', 'L1', 'MAPE', 'R-squared']
        assert all(col in result_df.columns for col in expected_columns), f"Missing columns. Expected columns: {expected_columns}, found: {result_df.columns.tolist()}"

    @patch('pandas.read_csv')  # Mocking the pandas read_csv function
    def test_display_errors_returns_dataframe_k_list(self, mock_read_csv, error_metrics):
        """
        Test that displayErrors returns a pandas DataFrame.
        
        Parameters:
            mock_read_csv (MagicMock): The mocked version of `pandas.read_csv`, which is 
                                       used to simulate the behavior of reading CSV files 
                                       without actually accessing the file.
            error_metrics (class): An instance of the error_metrics class to be tested.
        """
        # Prepare mock data
        mock_odds_data = pd.DataFrame({
            'normalized_winning_probability': [0.8, 0.75, 0.65]
        })
        
        mock_model_data = pd.DataFrame({
            'Champion': [1, 2, 1]  # Mocked model predictions (Champion)
        })
        
        # Set the mock read_csv return values
        mock_read_csv.side_effect = [mock_odds_data, mock_model_data, mock_model_data]  # Assuming 3 calls to read_csv

        # Call the displayErrors method with mocked inputs
        result_df = error_metrics.displayErrors(
            rating_system="ELO",
            tournament_name="Australian Open",
            k_list = [0.1]
        )

        # Test that the result is a DataFrame
        assert isinstance(result_df, pd.DataFrame), f"Expected a DataFrame, but got {type(result_df)}"

        # Test that the DataFrame contains the expected columns
        expected_columns = ['Model', 'RMSE', 'Linf', 'L1', 'MAPE', 'R-squared']
        assert all(col in result_df.columns for col in expected_columns), f"Missing columns. Expected columns: {expected_columns}, found: {result_df.columns.tolist()}"