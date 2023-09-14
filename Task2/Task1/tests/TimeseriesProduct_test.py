import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from TimeSeriesProduct import TimeSeriesProduct  # Import the class

class TestTimeSeriesProduct(unittest.TestCase):

    def setUp(self):
        self.product = TimeSeriesProduct()
        self.product.start_date = datetime(2021, 7, 1)
        self.product.end_date = datetime(2022, 7, 1)
        self.product.frequencies = ['10T']
        self.product.daily_seasonality_options = ["no"]
        self.product.weekly_seasonality_options = ["exist"]
        self.product.noise_levels = ["small"]
        self.product.trend_levels = ["exist"]

    def test_TimeSeriesGenerator(self):
        # Mock the pd.date_range method to return a predefined date range once
        with patch('pandas.date_range') as mock_date_range:
            expected_date_rng = pd.date_range(start=self.product.start_date, end=self.product.end_date, freq=self.product.frequencies)
            mock_date_range.return_value = expected_date_rng

            date_rng = self.product.TimeSeriesGenerator()


            # Verify the result
            self.assertEqual(date_rng, expected_date_rng)

    def test_add_noise(self):
        # Create a sample data array
        data = np.array([[1.0], [2.0], [3.0]])

        # Mock random number generation to return a predefined value once
        with patch('numpy.random.normal') as mock_normal:
            mock_normal.return_value = np.array([0.1])  # Mocked noise value

            noisy_data = self.product.add_noise(data, "small")

   
            expected_noisy_data = [1.1, 2.1, 3.1]
        
            self.assertTrue(np.array_equal(noisy_data, expected_noisy_data))

    def test_add_missing_values(self):
        # Create a sample data array
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        # Mock random number generation to return predefined missing indices
        with patch('numpy.random.choice') as mock_choice:
            mock_choice.return_value = np.array([1, 3])  # Mocked missing indices

            missing_data = self.product.add_missing_values(data, 0.4)

            # Verify that np.random.choice was called once
            mock_choice.assert_called_once_with(5, size=2, replace=False)

            # Verify the result
            expected_missing_data = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
    
            self.assertTrue(np.all(np.isnan(missing_data) == np.isnan(expected_missing_data)))

    def test_add_outliers(self):
        # Create a sample data array
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        # Mock random number generation to return predefined outlier indices and values
        with patch('numpy.random.choice') as mock_choice:
            mock_choice.return_value = np.array([1, 3])  # Mocked outlier indices
            with patch('numpy.random.uniform') as mock_uniform:
                mock_uniform.return_value = np.array([0.5, 0.7])  # Mocked outliers

                outlier_data, anomaly_mask = self.product.add_outliers(data, 0.4)

                # Verify that np.random.choice and np.random.uniform were called once each
                mock_choice.assert_called_once_with(5, 2, replace=False)
                mock_uniform.assert_called_once_with(-1, 1, 2)

                # Verify the result
                expected_outlier_data = np.array([1.0, 0.5, 3.0, 0.7, 5.0])
                expected_anomaly_mask = np.array([False, True, False, True, False])
                self.assertTrue(np.array_equal(outlier_data, expected_outlier_data))
                self.assertTrue(np.array_equal(anomaly_mask, expected_anomaly_mask))
