from Saver import Saver
import pandas as pd
import os
class FolderSaver(Saver):
    """
    A concrete producer class that saves files and metadata to a folder.

    Attributes:
        meta_data (list): A list to store metadata for saved files.
        builder: The builder used for generating time series data.
    """

    def __init__(self, builder):
        """
        Initialize a FolderProducer instance with a builder and an empty metadata list.

        Args:
            builder: The builder used for generating time series data.
        """
        self.meta_data = []
        self.builder = builder

    def save_file(self, df, counter, path):
        """
        Save a DataFrame as a CSV file and record metadata.

        Args:
            df (pd.DataFrame): The DataFrame to be saved.
            counter (int): The counter used for generating the filename.
            path (str): The path where the file should be saved.

        Returns:
            bool: True if the file is successfully saved, False otherwise.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        config_file_path = os.path.join(script_directory, path)


  
        df = df.to_csv(config_file_path + str(counter + 1) + '.csv', encoding='utf-8', index=False)
        self.meta_data.append({
            'id': str(counter + 1) + '.csv',
            'daily_seasonality': self.builder.time_series_product.daily_seasonality_options,
            'weekly_seasonality': self.builder.time_series_product.weekly_seasonality_options,
            'noise (high 30% - low 10%)': self.builder.time_series_product.noise_levels,
            'trend': self.builder.time_series_product.trend_levels,
            'cyclic_period (3 months)': self.builder.time_series_product.cyclic_periods,
            'percentage_outliers': int(self.builder.time_series_product.outliers_percentage * 100),
            'percentage_missing': int(self.builder.time_series_product.missing_percentage * 100),
            'freq': self.builder.time_series_product.frequencies
        })

    def save_meta_data(self, path):
        """
        Save the metadata to a CSV file.

        Args:
            path (str): The path where the metadata file should be saved.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.abspath(os.path.join(script_directory, path))
        meta_data_df = pd.DataFrame.from_records(self.meta_data)
        meta_data_df.to_csv(config_file_path + '/meta_data.csv', encoding='utf-8', index=False)
