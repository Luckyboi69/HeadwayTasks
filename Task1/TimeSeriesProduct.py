from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np
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
        self.missing_percentage = None
    def TimeSeriesGenerator(self):
        date_rng = pd.date_range(start=self.start_date, end=self.end_date, freq=self.frequencies)
        return date_rng
    def add_noise(self,data,noise_level):
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
    def add_missing_values(self,data, percentage_missing):
       
        num_missing = int(len(data) * percentage_missing)
        missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

        data_with_missing = data.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing
    def add_outliers(self,data, percentage_outliers):
        
        num_outliers = int(len(data) * percentage_outliers)
        outlier_indices = np.random.choice(len(data), num_outliers, replace=False)
        data_with_outliers = data.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask