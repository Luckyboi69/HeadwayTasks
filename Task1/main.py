from datetime import datetime, timedelta
import pandas as pd
import random
import itertools
import yaml
import numpy as np

from TimeSeriesProduct import TimeSeriesProduct
from TimeSeriesDirector import TimeSeriesDirector
from TimeSeriesBuilder import TimeSeriesBuilder
from AdditiveTimeSeriesBuilder import AdditiveTimeSeriesBuilder
from MultiplicativeTimeSeriesBuilder import MultiplicativeTimeSeriesBuilder
from YAMLReader import YAMLReader
random.seed(22)  
def main():
    yaml_reader = YAMLReader()

    # Specify the path to your YAML configuration file
    config_file_path = 'config.yml'

    # Read the attributes from the YAML file
    config_attributes = yaml_reader.read_attributes(config_file_path)
    data_types_value = config_attributes.get("simulation_parameters", {}).get("data_types")
    # Check if configuration attributes were successfully read
    if not config_attributes:
        print("Failed to read configuration attributes from the YAML file.")
        return
    # Create a builder instance and pass the product and configuration attributes
    if data_types_value == 'additive':
        builder = AdditiveTimeSeriesBuilder(config_attributes)
    elif data_types_value == 'multiplicative':
        builder = MultiplicativeTimeSeriesBuilder(config_attributes)
    else:
        raise ValueError(f"Unsupported data type: {data_types_value}")

    # Create a TimeSeriesDirector instance and pass the builder and configuration
    director = TimeSeriesDirector(builder)

        # Generate time series data using the director
    config_combinations = director.generate_all_config_combinations(config_attributes)
    for i, config_combination in enumerate(config_combinations):
        time_series_data = director.generate_time_series_data(config_combination)
        director.save_to_file(time_series_data, i)

  
if __name__ == "__main__":
    main()