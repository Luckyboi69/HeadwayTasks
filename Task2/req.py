import requests
import json

# Define the URL of your Django API endpoint
api_url = 'http://127.0.0.1:8000/create_simulator/'  # Update with your API URL

# Define the JSON data you want to send to the API
json_data =  {
                                "name": "simulator1",
                                "start_date": "2021-01-01",
                                "end_date": "2022-01-01",
                                "type": "additive",
                                "datasets": [
                                    {
                                        "frequency": "1H",
                                        "trend_coefficients": [0, 2, 1, 3],
                                        "missing_percentage": 0.06,
                                        "outlier_percentage": 0.05,
                                        "noise_level": "small",
                                        "cycle_component_frequency": 1,
                                        "seasonality_components": [
                                            {
                                                "frequency_type": "Weekly",
                                                "frequency_multiplier": 1,
                                                "phase_shift": 0,
                                                "amplitude": 3
                                            },
                                            {
                                                "frequency_type": "Daily",
                                                "frequency_multiplier": 2,
                                                "phase_shift": 90,
                                                "amplitude": 5
                                            }
                                        ]
                                    }
                                ]
                            }
# Send a POST request with the JSON data
response = requests.post(api_url, json=json_data)

# Check the response
if response.status_code == 200:
    print("Simu",response.text)
else:
    print("Error:", response.text, response.status_code)
