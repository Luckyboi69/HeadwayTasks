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

random.seed(22)  
def main():
    # Read the configuration from the YAML file
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Create a TimeSeriesProduct instance
    time_series_product = TimeSeriesProduct()

    # Create a builder instance and pass the product
    if config["simulation_parameters"]["data_types"]=='addittive':
        builder = AdditiveTimeSeriesBuilder(time_series_product)
    else: 
        builder = MultiplicativeTimeSeriesBuilder(time_series_product)
    # Create a TimeSeriesDirector instance and pass the builder and configuration
    director = TimeSeriesDirector(builder, config)

        # Generate time series data using the director
    director.generate_multiple_datasets()

  
if __name__ == "__main__":
    main()