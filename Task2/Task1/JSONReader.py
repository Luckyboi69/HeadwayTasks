import json
from Reader import Reader
from datetime import datetime
class JSONReader(Reader):
    """
    A concrete reader class for reading attributes from a JSON file.

    Attributes:
        None
    """

    def read_attributes(self, json_object):
        """
        Read attributes from a JSON object.

        Args:
            json_object (dict): A dictionary containing the JSON attributes.

        Returns:
            dict: A dictionary containing the read attributes.
        """
        try:
            # json_object   =  {
            #                     "name": "simulator1",
            #                     "start_date": "2021-01-01",
            #                     "end_date": "2022-01-01",
            #                     "type": "additive",
            #                     "datasets": [
            #                         {
            #                             "frequency": "1H",
            #                             "trend_coefficients": [0, 2, 1, 3],
            #                             "missing_percentage": 0.06,
            #                             "outlier_percentage": 0.05,
            #                             "noise_level": "small",
            #                             "cycle_component_frequency": 1,
            #                             "seasonality_components": [
            #                                 {
            #                                     "frequency_type": "Weekly",
            #                                     "frequency_multiplier": 1,
            #                                     "phase_shift": 0,
            #                                     "amplitude": 3
            #                                 },
            #                                 {
            #                                     "frequency_type": "Daily",
            #                                     "frequency_multiplier": 2,
            #                                     "phase_shift": 90,
            #                                     "amplitude": 5
            #                                 }
            #                             ]
            #                         }
            #                     ]
            #                 }

            # Parse the JSON object
            json_object = json.loads(json_object)
            # Transform into the desired structure
        
            # Extract the datasets from the JSON object
            datasets = json_object.get("datasets", [])
           

            # Determine daily and weekly seasonality based on seasonality components
            daily_seasonality_options = ["exist" if any(seasonality["frequency_type"] == "Daily" for seasonality in dataset["seasonality_components"]) else "no" for dataset in datasets]
            weekly_seasonality_options = ["exist" if any(seasonality["frequency_type"] == "Weekly" for seasonality in dataset["seasonality_components"]) else "no" for dataset in datasets]
            trend_levels = ["exist" if dataset.get("trend_coefficients") else "no" for dataset in datasets]
            start_date = datetime.strptime(json_object["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(json_object["end_date"], "%Y-%m-%d")
            # Transform the given JSON into the desired structure
            desired_structure = {
                "simulation_parameters": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "frequencies": [dataset["frequency"] for dataset in datasets],
                    "daily_seasonality_options": daily_seasonality_options,
                    "daily_amplitude": [seasonality["amplitude"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "daily_phase_shift": [seasonality["phase_shift"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "daily_multiplier": [seasonality["frequency_multiplier"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "weekly_seasonality_options": weekly_seasonality_options,
                    "weekly_amplitude": [seasonality["amplitude"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "weekly_phase_shift": [seasonality["phase_shift"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "weekly_multiplier": [seasonality["frequency_multiplier"] for dataset in datasets for seasonality in dataset["seasonality_components"]],
                    "noise_levels": [dataset["noise_level"] for dataset in datasets],
                    "trend_levels": trend_levels,
                    "cyclic_periods": ["exist" if dataset["cycle_component_frequency"] else "no" for dataset in datasets],
                    "cyclic_frequency": [dataset["cycle_component_frequency"] for dataset in datasets],
                    "trend_coefficients": datasets[0]["trend_coefficients"],
                    "data_types": json_object["type"],
                    "outliers_percentage": [dataset["outlier_percentage"] for dataset in datasets],
                    "missing_percentage": [dataset["missing_percentage"] for dataset in datasets],
                }
            }

            return desired_structure
        except Exception as e:
            print(f"Error parsing JSON object: {str(e)}")
            return {}


 