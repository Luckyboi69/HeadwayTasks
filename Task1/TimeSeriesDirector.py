import TimeSeriesBuilder
from FolderProducer import FolderProducer
from KafkaProducer import KafkaProducer
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

    def generate_time_series_data(self,config_combination):
        
        self.builder.configure_from_combination(config_combination)
        self.builder.set_data(self.builder.time_series_product.TimeSeriesGenerator())
        #generate values for timeseries
        value= self.builder.add_data()
        scaler = MinMaxScaler(feature_range=(-1, 1))
        value = scaler.fit_transform(value.values.reshape(-1, 1))
        value = self.builder.time_series_product.add_noise(value,self.builder.time_series_product.noise_levels)
        value, anomaly = self.builder.time_series_product.add_outliers(value,self.builder.time_series_product.outliers_percentage )
        value = self.builder.time_series_product.add_missing_values(value,self.builder.time_series_product.missing_percentage )
        # Combine the components into the final time series data
      
        time_series_data = pd.DataFrame({
            'Date': self.builder.data,
            'value': value
           ,'anomalies':anomaly
        })
        file_name = f"TimeSeries_daily_{self.builder.time_series_product.daily_seasonality_options}_weekly_{self.builder.time_series_product.weekly_seasonality_options}_noise_{self.builder.time_series_product.noise_levels}_trend_{self.builder.time_series_product.trend_levels}_cycle_{self.builder.time_series_product.cyclic_periods}_outliers_{int(self.builder.time_series_product.outliers_percentage * 100)}%_freq_{self.builder.time_series_product.frequencies}_missing_{int(self.builder.time_series_product.missing_percentage * 100)}%.csv"
        print(f"File '{file_name}' generated.")
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
        missing_percentage_list = config['missing_percentage']
       
        config_combinations = list(itertools.product(
            frequencies_list,
            daily_seasonality_options_list,
            weekly_seasonality_options_list,
            noise_levels_list,
            trend_levels_list,
            cyclic_periods_list,
            outliers_percentage_list,
            missing_percentage_list
        ))
      
        return config_combinations



    
    
    def generate_multiple_datasets(self,config_attributes,data_saving):
             if (data_saving["method"]=="folder"):
                config=data_saving["folder_path"]
                data_producer=FolderProducer(self.builder)  
             elif(data_saving["method"]=="kafka"):
                 config=data_saving["kafka_config"]
                 data_producer=KafkaProducer(self.builder)  
             config_combinations = self.generate_all_config_combinations(config_attributes)
           
             for i, config_combination in enumerate(config_combinations):
            # Generate time series data for the current combination
                time_series_data = self.generate_time_series_data(config_combination)
               
                data_producer.save_file(time_series_data,i,config)
                
             data_producer.save_meta_data(config)        
                

