import random
import pandas as pd
import numpy as np
from TimeSeriesBuilder import TimeSeriesBuilder
from TimeSeriesProduct import TimeSeriesProduct
from YAMLReader import YAMLReader

random.seed(22)

class AdditiveTimeSeriesBuilder(TimeSeriesBuilder):
    """
    A concrete builder class for creating additive time series data.

    Attributes:
        time_series_product (TimeSeriesProduct): An instance of the TimeSeriesProduct to build.
        data (pandas.DataFrame): The data used for constructing the time series.
        config (dict): Configuration attributes for the builder.
    """

    def __init__(self):
        """
        Initialize the AdditiveTimeSeriesBuilder with a TimeSeriesProduct instance and data attribute.
        """
        self.time_series_product = TimeSeriesProduct()
        self.data = None
        self.config = None

    def build_from_yaml(self, config_attributes):
        """
        Build the time series data from YAML configuration attributes.

        Args:
            config_attributes (dict): Configuration attributes for generating the time series data.
        """
        self.time_series_product.start_date = config_attributes['simulation_parameters']['start_date']
        self.time_series_product.end_date = config_attributes['simulation_parameters']['end_date']
        self.time_series_product.frequencies = config_attributes['simulation_parameters']['frequencies']
        self.time_series_product.daily_seasonality_options = config_attributes['simulation_parameters']['daily_seasonality_options']
        self.time_series_product.weekly_seasonality_options = config_attributes['simulation_parameters']['weekly_seasonality_options']
        self.time_series_product.noise_levels = config_attributes['simulation_parameters']['noise_levels']
        self.time_series_product.trend_levels = config_attributes['simulation_parameters']['trend_levels']
        self.time_series_product.cyclic_periods = config_attributes['simulation_parameters']['cyclic_periods']
        self.time_series_product.missing_percentage = config_attributes['simulation_parameters']['missing_percentage']
        self.time_series_product.data_type = config_attributes['simulation_parameters']['data_types']
        self.config = config_attributes

    def build_from_db(self, data):
        """
        Build the time series data from a database source.

        Args:
            data: Data source for generating the time series data (e.g., database query result).
        """
        pass

    def set_data(self, data):
        """
        Set the data attribute with external data.

        Args:
            data: Data source for generating the time series data (e.g., pandas DataFrame).
        """
        self.data = data

    def configure_from_combination(self, config_combination):
        """
        Configure the builder based on a combination of parameters.

        Args:
            config_combination (tuple): A combination of parameters to configure the time series generation.
        """
        frequency, daily_seasonality_option, weekly_seasonality_option, noise_level, trend_level, cyclic_period, outliers_percentage, missing_percentage = config_combination
        self.time_series_product.daily_seasonality_options = daily_seasonality_option
        self.time_series_product.weekly_seasonality_options = weekly_seasonality_option
        self.time_series_product.frequencies = frequency
        self.time_series_product.noise_levels = noise_level
        self.time_series_product.trend_levels = trend_level
        self.time_series_product.cyclic_periods = cyclic_period
        self.time_series_product.outliers_percentage = outliers_percentage
        self.time_series_product.missing_percentage = missing_percentage

    def add_weekly_seasonality(self):
        """
        Add weekly seasonality component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the weekly seasonality component.
        """
        if self.time_series_product.weekly_seasonality_options == "exist":
            seasonal_component = np.sin(2 * np.pi * self.data.dayofweek / 7)
        else:
            seasonal_component = np.zeros(len(self.data))
        return pd.Series(seasonal_component)

    def add_daily_seasonality(self):
        """
        Add daily seasonality component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the daily seasonality component.
        """
        if self.time_series_product.daily_seasonality_options == "exist":
            seasonal_component = np.sin(2 * np.pi * self.data.hour / 24)
        else:
            seasonal_component = np.zeros(len(self.data))
        return pd.Series(seasonal_component)

    def add_trend(self):
        """
        Add trend component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the trend component.
        """
        start_date = self.time_series_product.start_date
        end_date = self.time_series_product.end_date
        data_size = (end_date - start_date).days

        if self.time_series_product.trend_levels == "exist":
            slope = random.choice([1, -1])
            trend_component = np.linspace(0, data_size / 30 * slope, len(self.data)) if slope == 1 else np.linspace(
                -1 * data_size / 30, 0, len(self.data))
        else:
            trend_component = np.zeros(len(self.data))
        return pd.Series(trend_component)

    def add_cycles(self):
        """
        Add cyclic component to the time series data.

        Returns:
            float: The cyclic component value.
        """
        cycle_component = 0
        if self.time_series_product.cyclic_periods == "exist":
            cycle_component += np.sin(2 * np.pi * (self.data.quarter - 1) / 4)
        else:
            cycle_component = 0
        return cycle_component

    def add_data(self):
        """
        Add all components to generate the time series data.

        Returns:
            pd.Series: A pandas Series representing the generated time series data.
        """
        weekly_seasonality = self.add_weekly_seasonality()
        daily_seasonality = self.add_daily_seasonality()
        trend = self.add_trend()
        cycles = self.add_cycles()
        data_values = weekly_seasonality + daily_seasonality + trend + cycles
        return data_values
