import json
from Reader import Reader

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
            # Parse the JSON object
            given_json = json.loads(json_object)
            # Transform into the desired structure
            desired_structure = {
                "simulation_parameters": {
                    "start_date": given_json["start_date"],
                    "end_date": given_json["end_date"],
                    "frequencies": [dataset["frequency"] for dataset in given_json["datasets"]],
                    "daily_seasonality_options": ["exist" if dataset["frequency"] == "1H" else "no" for dataset in given_json["datasets"]],
                    "daily_amplitude": [seasonality["amplitude"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "daily_phase_shift": [seasonality["phase_shift"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "daily_multiplier": [seasonality["frequency_multiplier"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "weekly_seasonality_options": ["exist" if dataset["frequency_type"] == "Weekly" else "no" for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "weekly_amplitude": [seasonality["amplitude"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "weekly_phase_shift": [seasonality["phase_shift"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "weekly_multiplier": [seasonality["frequency_multiplier"] for dataset in given_json["datasets"] for seasonality in dataset["seasonality_components"]],
                    "noise_levels": [given_json["noise_level"]],
                    "trend_levels": ["exist" if given_json["trend_coefficients"] else "no"],
                    "cyclic_periods": ["exist" if given_json["cycle_component_frequency"] else "no"],
                    "cyclic_frequency": [given_json["cycle_component_frequency"]],
                    "trend_coefficients": given_json["trend_coefficients"],
                    "data_types": given_json["type"],
                    "outliers_percentage": [given_json["outlier_percentage"]],
                    "missing_percentage": [given_json["missing_percentage"]],
                }
            }

                    # Convert to JSON
            desired_json = json.dumps(desired_structure, indent=4)
            return desired_json
        except Exception as e:
            print(f"Error parsing JSON object: {str(e)}")
            return {}