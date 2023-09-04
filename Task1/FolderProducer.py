from Producer import Producer
import pandas as pd
class FolderProducer(Producer):    
    def __init__(self,builder):
     self.meta_data = []
     self.builder=builder
    def save_file(self,df,counter,path):
       df=df.to_csv(path + str(counter+1) + '.csv', encoding='utf-8', index=False)
       self.meta_data.append({'id': str(counter+1) + '.csv',
                        'daily_seasonality': self.builder.time_series_product.daily_seasonality_options,
                        'weekly_seasonality': self.builder.time_series_product.weekly_seasonality_options,
                        'noise (high 30% - low 10%)':self.builder.time_series_product.noise_levels,
                        'trend':self.builder.time_series_product.trend_levels,
                        'cyclic_period (3 months)': self.builder.time_series_product.cyclic_periods,
                        'percentage_outliers': int(self.builder.time_series_product.outliers_percentage * 100),
                        'percentage_missing': int(self.builder.time_series_product.missing_percentage * 100),
                        'freq': self.builder.time_series_product.frequencies})    
    def save_meta_data(self,path):
             meta_data_df = pd.DataFrame.from_records(self.meta_data)
             meta_data_df.to_csv(path+'/meta_data.csv', encoding='utf-8', index=False) 
       