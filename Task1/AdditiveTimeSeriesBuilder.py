import random
import pandas as pd
import numpy as np
from TimeSeriesBuilder import TimeSeriesBuilder
from TimeSeriesProduct import TimeSeriesProduct

random.seed(22)
# Concrete builder class
class AdditiveTimeSeriesBuilder(TimeSeriesBuilder):
    def __init__(self, config_attributes):
        # Create an instance of TimeSeriesProduct directly within the builder
        self.time_series_product = TimeSeriesProduct()
        self.data=None
        # Set the configuration attributes within the builder
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
    def set_data(self, data):
        self.data = data
    def configure_from_combination(self, config_combination):
        # Implement configuration logic here based on the provided config_combination
        frequency,daily_seasonality_option, weekly_seasonality_option,  noise_level, trend_level, cyclic_period, outliers_percentage, missing_percentage = config_combination
        self.time_series_product.daily_seasonality_options = daily_seasonality_option
        self.time_series_product.weekly_seasonality_options = weekly_seasonality_option
        self.time_series_product.frequencies = frequency
        self.time_series_product.noise_levels = noise_level
        self.time_series_product.trend_levels = trend_level
        self.time_series_product.cyclic_periods = cyclic_period
        self.time_series_product.outliers_percentage = outliers_percentage
        self.time_series_product.missing_percentage = missing_percentage

    def add_weekly_seasonality (self):
        
        if self.time_series_product.weekly_seasonality_options == "exist":
            seasonal_component = np.sin(2 * np.pi * self.data.dayofweek / 7)
        else:
            seasonal_component = np.zeros(len(self.data)) 
        return pd.Series(seasonal_component)
    def add_daily_seasonality(self):
        if self.time_series_product.daily_seasonality_options == "exist":  # Daily Seasonality
         seasonal_component = np.sin(2 * np.pi * self.data.hour / 24)
        else:
            seasonal_component = np.zeros(len(self.data))  
        return pd.Series(seasonal_component)
    def add_trend(self):
        start_date = self.time_series_product.start_date
        end_date = self.time_series_product.end_date
        self.data_size = (end_date - start_date).days

        if self.time_series_product.trend_levels == "exist":
            slope = random.choice([1, -1])
            trend_component = np.linspace(0, self.data_size / 30 * slope, len(self.data)) if slope == 1 else np.linspace(
                -1 *self.data_size / 30, 0, len(self.data)) 
        else:  # No Trend
            trend_component = np.zeros(len(self.data))    
        return pd.Series(trend_component)
    def add_cycles(self):
        cycle_component=0
        if self.time_series_product.cyclic_periods == "exist":  # Quarterly
                cycle_component += np.sin(2 * np.pi * (self.data.quarter-1) / 4)
        else:
             cycle_component = 0
        return cycle_component
             
    def add_data(self):
         weekly_seasonality = self.add_weekly_seasonality()
         daily_seasonality = self.add_daily_seasonality()
         trend = self.add_trend()
         cycles = self.add_cycles()
         data_values= weekly_seasonality+daily_seasonality+trend+cycles
         return data_values