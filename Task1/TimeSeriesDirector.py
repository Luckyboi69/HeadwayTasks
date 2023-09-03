import TimeSeriesBuilder
import itertools
import yaml
import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
random.seed(22)
class TimeSeriesDirector:   
    def __init__(self, builder):
        self.builder = builder
        self.meta_data = []

    def generate_time_series_data(self,config_combination):
        
        self.builder.configure_from_combination(config_combination)
        self.builder.set_data(self.builder.time_series_product.TimeSeriesGenerator())

    

 

        #generate values for timeseries
        value= self.builder.add_data()
        
        scaler = MinMaxScaler(feature_range=(-1, 1))
        value = scaler.fit_transform(value.values.reshape(-1, 1))
        value = self.add_noise(value,self.builder.time_series_product.noise_levels)
       # value, anomaly = self.add_outliers(value, outlier)
        
        value = self.add_missing_values(value, 0.05)
        # Combine the components into the final time series data
        #print("Im in director")
        #print(value)
        time_series_data = pd.DataFrame({
            'Date': self.builder.data,
            'value': value
          #  ,'anomalies':anomaly
        })
        #file_name = f"TimeSeries_daily_{self.builder.time_series_product.daily_seasonality_options}_weekly_{self.builder.time_series_product.weekly_seasonality_options}_noise_{self.builder.time_series_product.noise_levels}_trend_{self.builder.time_series_product.trend_levels}_cycle_{self.builder.time_series_product.cyclic_periods}_outliers_{int(outlier * 100)}%_freq_{freq}_size_{data_size}Days.csv"
        #print(f"File '{file_name}' generated.")
        return time_series_data   
    
    def generate_all_config_combinations(self, config_attributes):
        config = config_attributes['simulation_parameters']
        frequencies_list = config['frequencies']
        daily_seasonality_options_list = config['daily_seasonality_options']
        weekly_seasonality_options_list = config['weekly_seasonality_options']
        noise_levels_list = config['noise_levels']
        trend_levels_list = config['trend_levels']
        cyclic_periods_list = config['cyclic_periods']
        outliers_percentage_list = config['outliers_percentage']
       
        config_combinations = list(itertools.product(
            frequencies_list,
            daily_seasonality_options_list,
            weekly_seasonality_options_list,
            noise_levels_list,
            trend_levels_list,
            cyclic_periods_list,
            outliers_percentage_list
        ))
      
        return config_combinations

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
    
    def add_missing_values(self,data, percentage_missing=0.05): 
        num_missing = int(len(data) * percentage_missing)
        missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

        data_with_missing = data.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing

    def save_to_file(self,df,counter):
       df=df.to_csv('sample_datasets/' + str(counter+1) + '.csv', encoding='utf-8', index=False)
    #  self.meta_data.append({'id': str(counter+1) + '.csv',
    #                     'daily_seasonality': self.builder.time_series_product.daily_seasonality_options,
    #                     'weekly_seasonality': self.builder.time_series_product.weekly_seasonality_options,
    #                     'noise (high 30% - low 10%)':self.builder.time_series_product.noise_levels,
    #                     'trend':self.builder.time_series_product.trend_levels,
    #                     'cyclic_period (3 months)': self.builder.time_series_product.cyclic_periods,
    #                     'data_size': self.builder.time_series_product.data_sizes,
    #                     'percentage_outliers': int(self.builder.time_series_product.outliers_percentage * 100),
    #                     'percentage_missing': 0.05,
    #                     'freq': self.builder.time_series_product.frequencies})
   
    def generate_multiple_datasets(self):
            #for i in range(0):
                # Update the counter to track the dataset number
             config_combinations = self.generate_all_config_combinations()

             for i, config_combination in enumerate(config_combinations):
            # Generate time series data for the current combination
                time_series_data = self.generate_time_series_data(config_combination)
                self.save_to_file(time_series_data,i)
                
             meta_data_df = pd.DataFrame.from_records(self.meta_data)
             meta_data_df.to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)        
