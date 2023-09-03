from datetime import datetime, timedelta
import pandas as pd
import random
random.seed(22)

class TimeSeriesProduct():
    
    def __init__(self):
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
        self.num_datasets = None
        self.data_sizes = None
    def TimeSeriesGenerator(self):
        f=random.choice(self.frequencies)
        date_rng = pd.date_range(start=self.start_date, end=self.end_date, freq=f)
        return date_rng, f

