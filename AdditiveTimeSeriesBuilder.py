import random
import pandas as pd
import numpy as np
from TimeSeriesBuilder import TimeSeriesBuilder

random.seed(22)
# Concrete builder class
class AdditiveTimeSeriesBuilder(TimeSeriesBuilder):
    def __init__(self, time_series_product):
        self.time_series_product=time_series_product
      
    def Generator(self):
        self.data=self.time_series_product.TimeSeriesGenerator()
        self.data_size=random.choice(self.time_series_product.data_sizes)
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