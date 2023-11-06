from Saver import Saver
import pandas as pd
import requests

class NifiSaver (Saver):
    
    
    def __init__(self, builder):
        """
        Initialize a Producer instance with a builder and an empty metadata list.

        Args:
            builder: The builder used for generating time series data.
        """
        self.meta_data = []
        self.builder = builder


    def save_file(self, df,counter, nifi_url):
            """
            Send the time series data to NiFi using HTTP POST request.

            Args:
                time_series_data (pd.DataFrame): Time series data as a DataFrame.
                nifi_url (str): NiFi endpoint URL.

            Returns:
                bool: True if the data is successfully sent, False otherwise.
            """
            try:
                # Convert DataFrame to CSV string
                df = df.to_json(orient='records')
                # Send CSV data as a POST request to NiFi
                response = requests.post(nifi_url, data=df)
                self.meta_data.append({
                    'id': str(counter + 1) + '.csv',
                    'daily_seasonality': self.builder.time_series_product.daily_seasonality_options,
                    'weekly_seasonality': self.builder.time_series_product.weekly_seasonality_options,
                    'noise (high 30% - low 10%)': self.builder.time_series_product.noise_levels,
                    'trend': self.builder.time_series_product.trend_levels,
                    'cyclic_period (3 months)': self.builder.time_series_product.cyclic_periods,
                    'percentage_outliers': int(self.builder.time_series_product.outliers_percentage * 100),
                    'percentage_missing': int(self.builder.time_series_product.missing_percentage * 100),
                    'freq': self.builder.time_series_product.frequencies})
                if response.status_code == 200:
                    print("Data sent to NiFi successfully.")
                    return True
                else:
                    print("Failed to send data to NiFi. Status code:", response.status_code)
                    return False
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                return False
    def save_meta_data(self, path):
    #     """
    #     Save the metadata to a CSV file.

    #     Args:
    #         path (str): The path where the metadata file should be saved.
    #     """
         meta_data_df = pd.DataFrame.from_records(self.meta_data)
         meta_data_df.to_csv(path + '/meta_data.csv', encoding='utf-8', index=False)