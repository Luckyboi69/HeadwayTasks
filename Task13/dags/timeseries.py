import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
# Add Django project root to path
sys.path.append('/djangoapp')

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Task2.settings")

import django
django.setup()
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from simulator_api.models import SimulatorDetail
from simulator_api.views import trigger_simulator

# Assuming simulators_data is a list of dictionaries with simulator information
simulators_data = list(SimulatorDetail.objects.all().values())

def create_simulator_dag(simulator_data, schedule_interval):
    default_args = {
        'owner': 'airflow',
        'start_date': datetime(2023, 11, 11),
        'retries': 2,
        'retry_delay': timedelta(seconds=10),
    }

    # Now 'simulator_data' is a dictionary with the fields of the SimulatorDetail model
    dag_id = f'simulator_dag_{simulator_data["id"]}'
    dag = DAG(
        dag_id,
        default_args=default_args,
        description=f'DAG for Simulator {simulator_data["id"]}',
        schedule_interval=schedule_interval,
    )

    # Define a PythonOperator to set up Django and trigger the simulator
    task_id = f'setup_and_run_simulator_task_{simulator_data["id"]}'
    setup_and_run_simulator_task = PythonOperator(
        task_id=task_id,
        python_callable=setup_and_run_simulator,
        op_args=[simulator_data],
        provide_context=True,
        dag=dag,
    )

    return dag

# Define a PythonOperator to set up Django and trigger the run_simulator API endpoint
def setup_and_run_simulator(simulator_data_dict, **kwargs):
    # Trigger the run_simulator API endpoint
    trigger_run_simulator(simulator_data_dict, **kwargs)

# Define a PythonOperator to trigger the run_simulator API endpoint
def trigger_run_simulator(simulator_data_dict, **kwargs):
    
    trigger_simulator({"id": simulator_data_dict["id"]})

#
all_dags=[]
# Create DAGs for simulators with different schedule intervals
for simulator_data in simulators_data:
    scheduler_value = simulator_data['scheduler']
    schedule_interval = timedelta(days=int(scheduler_value))
    dag = create_simulator_dag(simulator_data, schedule_interval)
    all_dags.append(dag)
for dag in all_dags:
    globals()[dag.dag_id] = dag    
    
    