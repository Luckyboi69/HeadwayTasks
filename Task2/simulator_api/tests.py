from django.test import TestCase,TransactionTestCase,Client
from unittest.mock import patch  , MagicMock
from rest_framework import status
from simulator_api import models
from simulator_api import views
from django.urls import reverse
import json
from django.db import transaction

# Create your tests here.
class SimulatorDetailTestCase(TestCase):
    def setUp(self):
        self.simulator = models.SimulatorDetail.objects.create(
            status='submitted',
            start_date='2023-09-16',
            end_date='2023-09-20',
            name='Test Simulator',
            time_series_type='multiplicative',
            producer_type='Kafka',
            process_id='12345'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.simulator), 'Test Simulator')

class DatasetConfigurationTestCase(TestCase):
    def setUp(self):
        self.simulator = models.SimulatorDetail.objects.create(
            status='submitted',
            start_date='2023-09-16',
            end_date='2023-09-20',
            name='Test Simulator',
            time_series_type='multiplicative',
            producer_type='Kafka',
            process_id='12345'
        )
        self.config = models.DatasetConfiguration.objects.create(
            frequency='daily',
            noise_level='low',
            trend_coefficients='0.1,0.2',
            missing_percentage=0.1,
            outlier_percentage=0.05,
            cycle_component_frequency=0.1,
            status='Submitted',
            time_series=self.simulator
        )

    def test_string_representation(self):
        expected_str = f"Configuration for {self.simulator.name} (daily)"
        self.assertEqual(str(self.config), expected_str)

class SeasonalityComponentTestCase(TestCase):
    def setUp(self):
        self.simulator = models.SimulatorDetail.objects.create(
            status='submitted',
            start_date='2023-09-16',
            end_date='2023-09-20',
            name='Test Simulator',
            time_series_type='multiplicative',
            producer_type='Kafka',
            process_id='12345'
        )
        self.config = models.DatasetConfiguration.objects.create(
            frequency='daily',
            noise_level='low',
            trend_coefficients='0.1,0.2',
            missing_percentage=0.1,
            outlier_percentage=0.05,
            cycle_component_frequency=0.1,
            status='Submitted',
            time_series=self.simulator
        )
        self.seasonality = models.SeasonalityComponent.objects.create(
            amplitude=0.5,
            phase_shift=30,
            frequency_type='Daily',
            frequency_multiplier=1.0,
            dataset_configuration=self.config
        )

    def test_string_representation(self):
        expected_str = f"Seasonality Component for {self.config}"
        self.assertEqual(str(self.seasonality), expected_str)


class SimulatorViewsTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
                # Create a simulator for testing
        self.simulator = models.SimulatorDetail.objects.create(
            name="Test Simulator",
            start_date="2023-09-16",
            end_date="2023-09-20",
            time_series_type="multiplicative",
            status="Submitted"
        )

        self.dataset = models.DatasetConfiguration.objects.create(
            frequency="1H",
            trend_coefficients=[0,1,2,3],
            missing_percentage=0.05,
            outlier_percentage=0.05,
            noise_level="small",
            cycle_component_frequency=1,
            time_series=self.simulator
        )
        self.seasonality_component = models.SeasonalityComponent(
                frequency_type="Daily",
                frequency_multiplier=2,
                phase_shift=90,
                amplitude=5,
                dataset_configuration=self.dataset,
            )
    @transaction.atomic
    def test_create_simulator(self):
        # Create a simulator using a POST request
        data = {
            "name": "Test Simulator",
            "start_date": "2023-09-16",
            "end_date": "2023-09-20",
            "type": "multiplicative",
            "datasets": [
                {
                    "frequency": "daily",
                    "trend_coefficients": "0.1,0.2",
                    "missing_percentage": 0.1,
                    "outlier_percentage": 0.05,
                    "noise_level": "low",
                    "cycle_component_frequency": 0.1,
                    "seasonality_components": [
                        {
                            "frequency_type": "Daily",
                            "frequency_multiplier": 1.0,
                            "phase_shift": 30,
                            "amplitude": 0.5
                        }
                    ]
                }
            ]
        }
        response = self.client.post(reverse('create_simulator'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Simulator created successfully")

        # Ensure the simulator is created in the database
        simulator_count = models.SimulatorDetail.objects.filter(name="Test Simulator").count()
        self.assertEqual(simulator_count, 2)
    @transaction.atomic    
    def test_list_simulators(self):
        response = self.client.get(reverse('list_simulators'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": self.simulator.id, "name": self.simulator.name, "status": self.simulator.status}])

class RunSimulatorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_run_simulator(self):
        # Create a simulator in the database for testing
        simulator = models.SimulatorDetail.objects.create(
            name="Test Simulator",
            start_date="2023-09-16",
            end_date="2023-09-20",
            time_series_type="multiplicative",
            status="Submitted"
        )
        dataset = models.DatasetConfiguration.objects.create(
            frequency="1H",
            trend_coefficients=[0,1,2,3],
            missing_percentage=0.05,
            outlier_percentage=0.05,
            noise_level="small",
            cycle_component_frequency=1,
            time_series=simulator
        )
        seasonality_component = models.SeasonalityComponent(
                frequency_type="Daily",
                frequency_multiplier=2,
                phase_shift=90,
                amplitude=5,
                dataset_configuration=dataset,
            )
        # Prepare the request data
        data = {"id": simulator.id}

        # Send a POST request to run the simulator
        response = self.client.post(reverse('run_simulator'), data=json.dumps(data), content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Simulator started")

        # Check that the simulator status has been updated
        simulator.refresh_from_db()
        self.assertEqual(simulator.status, "Completed")

    
   
    def test_run_simulator_simulator_not_found(self):
        # Prepare the request data for a non-existent simulator
        data = {"id": 999}  # Assuming this ID doesn't exist in the database

        # Send a POST request to run the simulator
        response = self.client.post(reverse('run_simulator'), data=json.dumps(data), content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Simulator with ID 999 does not exist")
    


from django.test import TestCase, Client
from django.urls import reverse
import json

class StopSimulatorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('simulator_api.views.subprocess.run')
    
    def test_stop_simulator(self, mock_subprocess_run):
        simulator = models.SimulatorDetail.objects.create(
            name="Test Simulator",
            start_date="2023-09-16",
            end_date="2023-09-20",
            time_series_type="multiplicative",
            status="Running"
        )
        data = {"id": simulator.id}
        # Mock the subprocess run to simulate a successful taskkill
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        response = self.client.post(reverse('stop_simulator'), json.dumps(data), content_type='application/json')

        # Ensure that subprocess.run was called with the correct arguments
        mock_subprocess_run.assert_called_once_with(["taskkill", "/F", "/PID", simulator.process_id], check=True)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Simulator stopped")

    def test_stop_simulator_non_running_status(self):
        # Create a simulator in the database with a status other than "Running"
        simulator = models.SimulatorDetail.objects.create(
            name="Test Simulator",
            start_date="2023-09-16",
            end_date="2023-09-20",
            time_series_type="multiplicative",
            status="Submitted"
        )

        # Prepare the request data
        data = {"id": simulator.id}

        # Send a POST request to stop the simulator
        response = self.client.post(reverse('stop_simulator'), data=json.dumps(data), content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Simulator is not in 'Running' status")

        # Check that the simulator status remains unchanged
        simulator.refresh_from_db()
        self.assertEqual(simulator.status, "Submitted")

    def test_stop_simulator_simulator_not_found(self):
        # Prepare the request data for a non-existent simulator
        data = {"id": 999}  # Assuming this ID doesn't exist in the database

        # Send a POST request to stop the simulator
        response = self.client.post(reverse('stop_simulator'), data=json.dumps(data), content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Simulator with ID 999 does not exist")

        