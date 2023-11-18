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
from DatabaseReader import DatabaseReader
from JSONReader import JSONReader
import sys
import json
import os
random.seed(22)  
def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, "system_config.yaml")

    with open(config_file_path, "r") as config_file:
        system_config = yaml.safe_load(config_file)
    
    data_reading_method = system_config["data_reading"]["method"]
    
    if data_reading_method == "yaml":
        yaml_reader = YAMLReader()
        yaml_config_file = system_config["data_reading"]["yaml_config_file"]
        config_attributes = yaml_reader.read_attributes(yaml_config_file)
        data_saving = system_config["data_saving"]


    
    elif data_reading_method =="database":
        database_reader= DatabaseReader()
    elif data_reading_method== "json":
        json_reader = JSONReader()
        #json_data =
        json_data = sys.stdin.read()
        config_attributes,data_saving = json_reader.read_attributes(json_data)
        
    
# Read the attributes from the YAML file
    
    data_types_value = config_attributes.get("simulation_parameters", {}).get("data_types")

# Check if configuration attributes were successfully read
    
    if not config_attributes:
        print("Failed to read configuration attributes from the file.")
        return
    # Create a builder instance and pass the product and configuration attributes
    if data_types_value == 'additive':
        builder = AdditiveTimeSeriesBuilder()
        builder.build_from_reader(config_attributes)
    elif data_types_value == 'multiplicative':
        builder = MultiplicativeTimeSeriesBuilder()
        builder.build_from_reader(config_attributes)
    else:
        raise ValueError(f"Unsupported data type: {data_types_value}")

        

    # Create a TimeSeriesDirector instance and pass the builder
    director = TimeSeriesDirector(builder)
    director.generate_multiple_datasets(config_attributes,data_saving)


  
if __name__ == "__main__":
    main()