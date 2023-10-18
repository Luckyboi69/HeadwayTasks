from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from .models import SimulatorDetail,DatasetConfiguration,SeasonalityComponent
from subprocess import Popen, PIPE
import threading
import json
import uuid
import subprocess
import os
@api_view(['POST'])
def create_simulator(request):
    """
    Create a new Simulator instance along with associated datasets and seasonality components.

    This view function handles the creation of a SimulatorDetail instance and its related DatasetConfiguration
    instances, including seasonality components, based on the provided JSON data in the request.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data.

    Returns:
        JsonResponse: A JSON response indicating the result of the creation process.
            - If successful, it returns a message indicating the simulator was created successfully.
            - If there's an error, it returns an error message with a 500 status code.
    """    
    data = request.data

    # Extract simulator data from the JSON request.
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    time_series_type = data.get("type")

    # Create the Simulator instance.
    simulator = SimulatorDetail(
        #process_id=uuid.uuid4(),
        name=name,
        start_date=start_date,
        end_date=end_date,
        time_series_type=time_series_type,
        status='Submitted'  # Set the initial status to 'Submitted'.
    )
    simulator.save()

    # Extract and create datasets and seasonality components.
    datasets_data = data.get("datasets", [])
    for dataset_data in datasets_data:
        frequency = dataset_data.get("frequency")
        trend_coefficients = dataset_data.get("trend_coefficients")
        missing_percentage = dataset_data.get("missing_percentage")
        outlier_percentage = dataset_data.get("outlier_percentage")
        noise_level = dataset_data.get("noise_level")
        cycle_component_frequency = dataset_data.get("cycle_component_frequency")
        dataset = DatasetConfiguration(
            frequency=frequency,
            trend_coefficients=trend_coefficients,
            missing_percentage=missing_percentage,
            outlier_percentage=outlier_percentage,
            noise_level=noise_level,
            cycle_component_frequency=cycle_component_frequency,
            time_series=simulator,
        )
        dataset.save()

        # Extract and create seasonality components for the dataset.
        seasonality_components_data = dataset_data.get("seasonality_components", [])
        for seasonality_data in seasonality_components_data:
            seasonality_frequency = seasonality_data.get("frequency_type")
            multiplier = seasonality_data.get("frequency_multiplier")
            phase_shift = seasonality_data.get("phase_shift")
            amplitude = seasonality_data.get("amplitude")

            seasonality_component = SeasonalityComponent(
                frequency_type=seasonality_frequency,
                frequency_multiplier=multiplier,
                phase_shift=phase_shift,
                amplitude=amplitude,
                dataset_configuration=dataset,
            )
            seasonality_component.save()
   
   
    if simulator.id:
        return JsonResponse({"message": "Simulator created successfully"})
    else:
        return JsonResponse({"message": f"Error: Simulator creation Failed"}, status=500)
# Define a function to list simulators
def list_simulators_thread(result_list):
    """
    Retrieve a list of all simulators and store their serialized information in the result_list.

    This function queries the SimulatorDetail model to retrieve all simulators and then serializes
    their relevant information, including their ID, name, and status. The serialized data is appended
    to the provided result_list.

    Args:
        result_list (list): A list where the serialized simulator information will be appended.

    Returns:
        None: This function does not return a value directly but populates the result_list with data.
    """    
    simulators = SimulatorDetail.objects.all()
    serialized_simulators = [{"id":simulator.id, "name": simulator.name, "status": simulator.status} for simulator in simulators]
    result_list.append(serialized_simulators)

@api_view(['GET'])
def list_simulators(request):
    """
    Retrieve a list of all simulators and return them as JSON response.

    This function creates a thread to asynchronously retrieve a list of all simulators from the
    SimulatorDetail model. The results are serialized and returned as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing a list of serialized simulators. The response
        format is [{"id": simulator_id, "name": simulator_name, "status": simulator_status}, ...].

    Note:
        The function uses threading to improve performance by executing the database query in
        a separate thread, allowing the main thread to respond to other requests.
    """    
    # Create a list to store the results from threads
    result_list = []

    # Create and start a thread to list simulators
    list_thread = threading.Thread(target=list_simulators_thread, args=(result_list,))
    list_thread.start()

    # Wait for the thread to finish
    list_thread.join()

    # Retrieve the result from the thread
    serialized_simulators = result_list[0] if result_list else []

    return JsonResponse(serialized_simulators, safe=False)



def get_simulator_data(simulator_id):
    """
    Retrieve simulator data and related configurations as JSON for a given simulator ID.

    This function queries the SimulatorDetail and related models to gather data associated with
    the specified simulator ID. The data is structured and returned as a JSON string.

    Args:
        simulator_id (int): The ID of the simulator to retrieve data for.

    Returns:
        str: A JSON string containing simulator and configuration data in the following format:
        {
            "name": "Simulator Name",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "type": "Time Series Type",
            "datasets": [
                {
                    "frequency": "Frequency",
                    "trend_coefficients": "Trend Coefficients",
                    "missing_percentage": Missing Percentage,
                    "outlier_percentage": Outlier Percentage,
                    "noise_level": Noise Level,
                    "cycle_component_frequency": Cycle Component Frequency,
                    "seasonality_components": [
                        {
                            "frequency_type": "Seasonality Frequency Type",
                            "frequency_multiplier": Frequency Multiplier,
                            "phase_shift": Phase Shift,
                            "amplitude": Amplitude
                        },
                        ...
                    ]
                },
                ...
            ]
        }

    Note:
        This function handles database query exceptions and returns an error response if the specified
        simulator ID does not exist.
    """    
    try:
        # Query the SimulatorDetail model by ID and select related objects
        simulator = SimulatorDetail.objects.get(id=simulator_id)
        dataset_configuration= DatasetConfiguration.objects.get(time_series_id=simulator_id)
        
        # Access related data
        name = simulator.name
        status = simulator.status
        start_date = simulator.start_date.strftime("%Y-%m-%d")
        end_date = simulator.end_date.strftime("%Y-%m-%d")
        time_series_type= simulator.time_series_type
        

        # Create a data structure to store all associated data
        data = {
            'name': name,
            'start_date': start_date,
            'end_date': end_date,
            'type': time_series_type,
            'datasets': []
        }

        #for dataset_configuration in dataset_configurations:
        frequency = dataset_configuration.frequency
        trend_coefficients = dataset_configuration.trend_coefficients
        missing_percentage= dataset_configuration.missing_percentage
        outlier_percentage = dataset_configuration.outlier_percentage
        noise_level = dataset_configuration.noise_level
        cycle_component_frequency = dataset_configuration.cycle_component_frequency
        # Access related SeasonalityComponent instances
        dataset_id= dataset_configuration.id

        seasonality_components = SeasonalityComponent.objects.filter(dataset_configuration_id=dataset_id)

        dataset_data = {
            'frequency': frequency,
            "trend_coefficients": trend_coefficients,
            "missing_percentage": missing_percentage,
            "outlier_percentage": outlier_percentage,
            "noise_level": noise_level,
            "cycle_component_frequency": cycle_component_frequency,
            'seasonality_components': []
        }

        for seasonality_component in seasonality_components:
            frequency_type = seasonality_component.frequency_type
            amplitude = seasonality_component.amplitude
            phase_shift = seasonality_component.phase_shift
            frequency_multiplier = seasonality_component.frequency_multiplier
            # Add seasonality component data to the dataset data
            dataset_data['seasonality_components'].append({
                'frequency_type': frequency_type,
                'frequency_multiplier':frequency_multiplier,
                'phase_shift':phase_shift,
                'amplitude':amplitude
                # Add other fields as needed
            })

        # Add dataset data to the main data structure
        data['datasets'].append(dataset_data)
        json_data = json.dumps(data)

        return json_data

    except SimulatorDetail.DoesNotExist:
        return JsonResponse({"message": f"Simulator with ID {simulator_id} does not exist"}, status=404)


@api_view(['POST'])
def run_simulator(request):
    """
    Start the execution of a simulator by its ID.

    This function allows starting the execution of a simulator with the specified ID. If the simulator is in the
    'Submitted' status, it changes the status to 'Running', starts a separate thread to run the simulator's task,
    and updates the status based on the task's completion or failure.

    Args:
        request (HttpRequest): The HTTP request object containing the simulator ID in the request data.

    Returns:
        JsonResponse: A JSON response indicating the result of the operation. Possible responses include:
            - {"message": "Simulator started"} if the simulator was successfully started.
            - {"message": "Simulator is not in 'Submitted' status"} if the simulator is not in the 'Submitted' status.
            - {"message": f"Simulator with ID {simulator_id} does not exist"} if the specified simulator ID does not exist.

    Note:
        - The function uses a separate thread to run the simulator, allowing the main thread to respond immediately.
        - The simulator's process ID is saved in the database for reference.
        - The simulator status is updated based on the process return code ('Completed' or 'Failed').
    """    
    try:
        # Logic to run a simulator by its ID.
        # Query the SimulatorDetail model by ID
        data=request.data
        simulator_id=data.get("id") 
        simulator = SimulatorDetail.objects.get(id=simulator_id)
     
        if simulator.status == "Submitted":
            simulator.status = "Running"
            simulator.save()  # Update the status to "Running" in the database
        if simulator.status == "Running":
            # Define a function to run the simulator in a separate thread

            dataset = get_simulator_data(simulator_id)
            def run_simulator_thread(data):
                #json_data = json.dumps(data)
                process = subprocess.Popen(['python', 'Task1/main.py'], stdin=subprocess.PIPE, text=True)
                process_id = process.pid
                simulator.process_id = str(process_id)
                simulator.save()
                process.communicate(input=data)

                print(process)
                print("HEHEHE")
                print(process_id)
                
                # Update the simulator status based on the process return code
                if process.returncode == 0:
                    simulator.status = "Completed"
                else:
                    simulator.status = "Failed"
                #simulator.process_id = process_id
                simulator.save()  # Update the status in the database

            # Create and start a thread to run the simulator
            simulator_thread = threading.Thread(target=run_simulator_thread(dataset))
            simulator_thread.start()

            return JsonResponse({"message": "Simulator started"})
        else:
            return JsonResponse({"message": "Simulator is not in 'Submitted' status"}, status=400)

    except SimulatorDetail.DoesNotExist:
        return JsonResponse({"message": f"Simulator with ID {simulator_id} does not exist"}, status=404)



@api_view(['POST'])
def stop_simulator(request):
    """
    Stop the execution of a running simulator by its ID.

    This function allows stopping the execution of a running simulator with the specified ID. It retrieves the
    process ID associated with the simulator, uses the `taskkill` command on Windows to stop the process, and
    updates the simulator's status to 'Stopped'.

    Args:
        request (HttpRequest): The HTTP request object containing the simulator ID in the request data.

    Returns:
        JsonResponse: A JSON response indicating the result of the operation. Possible responses include:
            - {"message": "Simulator stopped"} if the simulator was successfully stopped.
            - {"message": "Simulator is not in 'Running' status"} if the simulator is not running.
            - {"message": f"Simulator with ID {simulator_id} does not exist"} if the specified simulator ID does not exist.

    Note:
        - The function assumes that the process ID associated with the simulator has been stored in the database.
        - It uses the `taskkill` command on Windows to forcibly terminate the process.
    """    
    try:
        data = request.data
        simulator_id = data.get("id") 
        # Query the SimulatorDetail model by ID
        simulator = SimulatorDetail.objects.get(id=simulator_id)

        if simulator.status == "Running":
            # Get the process_id associated with the simulator
            process_id = simulator.process_id
            print(process_id)
            print(type(process_id))
            # Use the subprocess module to run a command to stop the process
            try:
                # On Windows, you can use taskkill to stop a process by its ID
                subprocess.run(["taskkill", "/F", "/PID", process_id], check=True)
            except subprocess.CalledProcessError as e:
                return JsonResponse({"message": f"Error stopping simulator: {str(e)}"}, status=500)

            # Update the simulator status to "Stopped"
            simulator.status = "Stopped"
            simulator.save()

            return JsonResponse({"message": "Simulator stopped"})
        else:
            return JsonResponse({"message": "Simulator is not in 'Running' status"}, status=400)

    except SimulatorDetail.DoesNotExist:
        return JsonResponse({"message": f"Simulator with ID {simulator_id} does not exist"}, status=404)
