from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np

random.seed(22)

class TimeSeriesProduct():
    """
    A class representing a time series product with various configuration options.

    Attributes:
        start_date (datetime): The start date of the time series.
        end_date (datetime): The end date of the time series.
        frequencies (str): The frequency of the time series data.
        daily_seasonality_options (str): Options for daily seasonality.
        weekly_seasonality_options (str): Options for weekly seasonality.
        noise_levels (str): The level of noise to add to the time series.
        trend_levels (str): The level of trend to add to the time series.
        cyclic_periods (str): The periodicity of cyclic components.
        data_type (str): The type of data to generate.
        noise_percentage (float): The percentage of noise to add.
        outliers_percentage (float): The percentage of outliers to add.
        missing_percentage (float): The percentage of missing values to introduce.
    """

    def __init__(self):
        """
        Initialize a TimeSeriesProduct instance with default configuration attributes.
        """
        self.start_date = None
        self.end_date = None
        self.frequencies = None
        self.daily_seasonality_options = None
        self.weekly_seasonality_options = None
        self.noise_levels = None
        self.trend_levels = None
        self.cyclic_periods = None
        self.data_type = None
        self.noise_percentage = None
        self.outliers_percentage = None
        self.missing_percentage = None

    def TimeSeriesGenerator(self):
        """
        Generate a date range for the time series based on the configured attributes.

        Returns:
            pd.DatetimeIndex: A pandas DatetimeIndex representing the date range.
        """
        date_rng = pd.date_range(start=self.start_date, end=self.end_date, freq=self.frequencies)
        return date_rng

    def add_noise(self, data, noise_level):
        """
        Add noise to the given data based on the specified noise level.

        Args:
            data (pd.Series): The data to which noise will be added.
            noise_level (str): The level of noise to add ("small", "large", or "none").

        Returns:
            pd.Series: A pandas Series with added noise.
        """
        if noise_level == "small":
            noise_level = 0.1
        elif noise_level == "large":
            noise_level = 0.3
        else:  # No Noise
            noise_level = 0

        noise = np.zeros_like(data)
        for i in range(len(data)):
            noise[i] = np.random.normal(0, abs(data[i]) * noise_level) if noise_level > 0 else 0
        return pd.Series((data + noise)[:, 0])

    def add_missing_values(self, data, percentage_missing):
        """
        Add missing values to the given data based on the specified percentage.

        Args:
            data (pd.Series): The data to which missing values will be added.
            percentage_missing (float): The percentage of missing values to introduce.

        Returns:
            pd.Series: A pandas Series with missing values.
        """
        num_missing = int(len(data) * percentage_missing)
        missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

        data_with_missing = data.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing

    def add_outliers(self, data, percentage_outliers):
        """
        Add outliers to the given data based on the specified percentage.

        Args:
            data (pd.Series): The data to which outliers will be added.
            percentage_outliers (float): The percentage of outliers to introduce.

        Returns:
            pd.Series: A pandas Series with added outliers.
            np.ndarray: A boolean array indicating the positions of outliers in the data.
        """
        num_outliers = int(len(data) * percentage_outliers)
        outlier_indices = np.random.choice(len(data), num_outliers, replace=False)
        data_with_outliers = data.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask
