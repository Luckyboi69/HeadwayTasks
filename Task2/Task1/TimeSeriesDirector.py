import TimeSeriesBuilder
from FolderSaver import FolderSaver
from KafkaProducer import KafkaProducer
from KafkaConsumer import KafkaConsumer
from NifiSaver import NifiSaver
import itertools
import yaml
import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

random.seed(22)

class TimeSeriesDirector:
    """
    A class responsible for generating time series data based on configurations.

    Attributes:
        builder: The builder used for generating time series data.
    """

    def __init__(self, builder):
        """
        Initialize a TimeSeriesDirector instance with a builder.

        Args:
            builder: The builder used for generating time series data.
        """
        self.builder = builder

    def generate_time_series_data(self, config_combination):
        """
        Generate time series data based on a specific configuration combination.

        Args:
            config_combination (tuple): A combination of configuration parameters.

        Returns:
            pd.DataFrame: A DataFrame representing the generated time series data.
        """
        self.builder.configure_from_combination(config_combination)
        self.builder.set_data(self.builder.time_series_product.TimeSeriesGenerator())

        # Generate values for time series
        value = self.builder.add_data()
        scaler = MinMaxScaler(feature_range=(-1, 1))
        value = scaler.fit_transform(value.values.reshape(-1, 1))
        value = self.builder.time_series_product.add_noise(value, self.builder.time_series_product.noise_levels)
        value, anomaly = self.builder.time_series_product.add_outliers(value, self.builder.time_series_product.outliers_percentage)
        value = self.builder.time_series_product.add_missing_values(value, self.builder.time_series_product.missing_percentage)

        # Combine the components into the final time series data
        time_series_data = pd.DataFrame({
            'Date': self.builder.data,
            'value': value,
            'anomalies': anomaly
        })

        file_name = f"TimeSeries_daily_{self.builder.time_series_product.daily_seasonality_options}_weekly_{self.builder.time_series_product.weekly_seasonality_options}_noise_{self.builder.time_series_product.noise_levels}_trend_{self.builder.time_series_product.trend_levels}_cycle_{self.builder.time_series_product.cyclic_periods}_outliers_{int(self.builder.time_series_product.outliers_percentage * 100)}%_freq_{self.builder.time_series_product.frequencies}_missing_{int(self.builder.time_series_product.missing_percentage * 100)}%.csv"
        print(f"File '{file_name}' generated.")
        return time_series_data

    def generate_all_config_combinations(self, config_attributes):
        """
        Generate all possible combinations of configuration parameters based on the provided attributes.

        Args:
            config_attributes (dict): Configuration attributes.

        Returns:
            list: A list of all configuration combinations as tuples.
        """
        config = config_attributes['simulation_parameters']
        frequencies_list = config['frequencies']
        daily_seasonality_options_list = config['daily_seasonality_options']
        weekly_seasonality_options_list = config['weekly_seasonality_options']
        noise_levels_list = config['noise_levels']
        trend_levels_list = config['trend_levels']
        cyclic_periods_list = config['cyclic_periods']
        outliers_percentage_list = config['outliers_percentage']
        missing_percentage_list = config['missing_percentage']
        daily_amplitude_list = config['daily_amplitude']
        daily_phase_shift_list = config ['daily_phase_shift']
        daily_multiplier = config ['daily_multiplier']
        weekly_amplitude_list = config['weekly_amplitude']
        weekly_phase_shift_list = config ['weekly_phase_shift']
        weekly_multiplier_list = config ['weekly_multiplier']
        cyclic_frequency_list = config ['cyclic_frequency']
        config_combinations = list(itertools.product(
            frequencies_list,
            daily_seasonality_options_list,
            weekly_seasonality_options_list,
            noise_levels_list,
            trend_levels_list,
            cyclic_periods_list,
            outliers_percentage_list,
            missing_percentage_list,
            daily_amplitude_list,
            daily_phase_shift_list,
            daily_multiplier,
            weekly_amplitude_list,
            weekly_phase_shift_list,
            weekly_multiplier_list,
            cyclic_frequency_list
        ))

        return config_combinations

    def generate_multiple_datasets(self, config_attributes, data_saving):
        """
        Generate multiple time series datasets based on configurations and save them.

        Args:
            config_attributes (dict): Configuration attributes.
            data_saving (dict): Data saving method and configuration.

        Returns:
            None
        """
        config_combinations = self.generate_all_config_combinations(config_attributes)

        if data_saving["producer_type"] == "folder":
            config = data_saving["sink_name"]
            data_saver = FolderSaver(self.builder)
            for i, config_combination in enumerate(config_combinations):
            # Generate time series data for the current combination
                time_series_data = self.generate_time_series_data(config_combination)
                #nifi.save_file(time_series_data,i,nifi_url)
                data_saver.save_file(time_series_data, i, config)
            #nifi= NifiSaver(self.builder)
            #nifi_url="http://nifi:5000"
            data_saver.save_meta_data(config)
        elif data_saving["producer_type"] == "kafka":
            config = data_saving["sink_name"]
            att_id = data_saving["attribute_id"]
            gen_id = data_saving["generator_id"]
            data_producer=KafkaProducer()
            data_consumer = KafkaConsumer(config)
            for i, config_combination in enumerate(config_combinations):
            # Generate time series data for the current combination
                time_series_data = self.generate_time_series_data(config_combination)
                data_producer.produce_time_series_to_kafka(time_series_data,config,gen_id,att_id)
            data_consumer.consume_and_save()

           

