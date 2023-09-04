import unittest
import pandas as pd
from unittest.mock import patch
from MultiplicativeTimeSeriesBuilder import MultiplicativeTimeSeriesBuilder

class TestMultiplicativeTimeSeriesBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = MultiplicativeTimeSeriesBuilder()
        self.builder.time_series_product.start_date = pd.to_datetime("2021-07-01")
        self.builder.time_series_product.end_date = pd.to_datetime("2021-07-10")

    def test_add_weekly_seasonality_exist_multi(self):
        # Mock the data for the test
        data = pd.date_range(start="2021-07-01", end="2021-07-07", freq="D")

        # Set the builder's data
        self.builder.set_data(data)

        # Set weekly_seasonality_options to "exist"
        self.builder.time_series_product.weekly_seasonality_options = "exist"

        # Call the method to add weekly seasonality
        seasonal_component = self.builder.add_weekly_seasonality()

        # Verify the result (e.g., check if it's not all ones)
        self.assertTrue(any(seasonal_component != 1))

    def test_add_daily_seasonality_exist_multi(self):
        # Mock the data for the test
        data = pd.date_range(start="2021-07-01", end="2021-07-02", freq="H")

        # Set the builder's data
        self.builder.set_data(data)

        # Set daily_seasonality_options to "exist"
        self.builder.time_series_product.daily_seasonality_options = "exist"

        # Call the method to add daily seasonality
        seasonal_component = self.builder.add_daily_seasonality()

        # Verify the result (e.g., check if it's not all ones)
        self.assertTrue(any(seasonal_component != 1))

    def test_add_trend_exist_multi(self):
        # Mock the data for the test
        data = pd.date_range(start="2021-07-01", end="2021-07-10", freq="D")

        # Set the builder's data
        self.builder.set_data(data)

        # Set trend_levels to "exist"
        self.builder.time_series_product.trend_levels = "exist"

        # Call the method to add trend
        trend_component = self.builder.add_trend()

        # Verify the result (e.g., check if it's not all zeros)
        self.assertTrue(any(trend_component != 0))

    def test_add_cycles_exist_multi(self):
        # Mock the data for the test
        data = pd.date_range(start="2021-01-01", end="2021-12-31", freq="D")

        # Set the builder's data
        self.builder.set_data(data)

        # Set cyclic_periods to "exist"
        self.builder.time_series_product.cyclic_periods = "exist"

        # Call the method to add cycles
        cycle_component = self.builder.add_cycles()

        # Verify the result (e.g., check if it's not all zeros)
        self.assertTrue(any(cycle_component != 0))

    def test_add_data_multi(self):
        # Mock the data for the test
        data = pd.date_range(start="2021-07-01", end="2021-07-10", freq="D")

        # Set the builder's data
        self.builder.set_data(data)

        # Set various configuration options
        self.builder.time_series_product.weekly_seasonality_options = "exist"
        self.builder.time_series_product.daily_seasonality_options = "exist"
        self.builder.time_series_product.trend_levels = "exist"
        self.builder.time_series_product.cyclic_periods = "exist"

        # Call the method to add data
        data_values = self.builder.add_data()

        # Verify the result (e.g., check if it's not all zeros)
        self.assertTrue(any(data_values != 0))

