import unittest
from unittest.mock import Mock, patch
from FolderProducer import FolderProducer
import pandas as pd

class TestFolderProducer(unittest.TestCase):

    def setUp(self):
        self.builder_mock = Mock()
        self.builder_mock.time_series_product.daily_seasonality_options = ["no"]
        self.builder_mock.time_series_product.weekly_seasonality_options = ["exist"]
        self.builder_mock.time_series_product.noise_levels = ["small"]
        self.builder_mock.time_series_product.trend_levels = ["exist"]
        self.builder_mock.time_series_product.cyclic_periods = ["no"]
        self.builder_mock.time_series_product.outliers_percentage = 0.05
        self.builder_mock.time_series_product.missing_percentage = 0.05
        self.builder_mock.time_series_product.frequencies = ["10T"]
        self.producer = FolderProducer(self.builder_mock)

    @patch('pandas.DataFrame.to_csv')
    def test_save_file(self, mock_to_csv):
        # Create a sample DataFrame
        df = pd.DataFrame({'column1': [1, 2, 3]})

        # Mock the to_csv method to avoid actual file I/O
        mock_to_csv.return_value = None

        # Save the file
        self.producer.save_file(df, 0, '/some/folder/')

        # Verify that to_csv was called with the expected arguments
        mock_to_csv.assert_called_once_with('/some/folder/1.csv', encoding='utf-8', index=False)

