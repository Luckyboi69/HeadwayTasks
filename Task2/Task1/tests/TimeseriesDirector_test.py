import unittest
from unittest.mock import Mock, patch
from TimeSeriesDirector import TimeSeriesDirector
import pandas as pd
import numpy as np
class TestTimeSeriesDirector(unittest.TestCase):

    @patch('TimeSeriesDirector.FolderProducer')

    @patch('sklearn.preprocessing.MinMaxScaler', autospec=True)
    def setUp(self, MockFolderProducer, MockMinMaxScaler):
        self.builder = Mock()
        self.director = TimeSeriesDirector(self.builder)

        self.mock_folder_producer = MockFolderProducer.return_value
        self.mock_scaler = MockMinMaxScaler.return_value

        # Set up the self.builder.time_series_product mock with expected values
        self.builder.time_series_product = Mock(
            daily_seasonality_options="exist",
            weekly_seasonality_options="exist",
            noise_levels="small",
            trend_levels="exist",
            cyclic_periods="exist",
            outliers_percentage=0.1,
            frequencies="10T",
            missing_percentage=0.1
        )

        # Set up config_attributes once
        self.config_attributes = {
            'simulation_parameters': {
                'frequencies': ["10T", "20T"],
                'daily_seasonality_options': ['exist', 'none'],
                'weekly_seasonality_options': ['exist', 'none'],
                'noise_levels': ['small', 'large'],
                'trend_levels': ['exist', 'none'],
                'cyclic_periods': ['exist', 'none'],
                'outliers_percentage': [0.1, 0.2],
                'missing_percentage': [0.1, 0.2],
            }
        }


    def test_generate_time_series_data(self):
        # Mock builder and producer methods
        self.builder.configure_from_combination.return_value = None
        self.builder.set_data.return_value = None
        values = np.array([1.0, 2.0])  # Provide values directly
        df = pd.DataFrame({'value': values})  # Create a Pandas DataFrame
        self.builder.add_data.return_value = df  # Return the DataFrame
        self.builder.time_series_product.add_noise.return_value = None
        self.builder.time_series_product.add_outliers.return_value = (None, [0, 0])
        self.builder.time_series_product.add_missing_values.return_value = None
        self.mock_scaler.fit_transform.return_value = df.values.reshape(-1, 1)

        # Call the method under test
        config_combination = (1, 'exist', 'exist', 'small', 'exist', 'exist', 0.1, 0.1)
        result = self.director.generate_time_series_data(config_combination)

        # Assert that the expected DataFrame structure is returned
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ['Date', 'value', 'anomalies'])
        self.assertEqual(len(result), 2)


    def test_generate_all_config_combinations(self):
        # Call the method under test using the common config_attributes
        result = self.director.generate_all_config_combinations(self.config_attributes)

        # Assert that the expected number of combinations is generated
        expected_combinations = 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2
        self.assertEqual(len(result), expected_combinations)




