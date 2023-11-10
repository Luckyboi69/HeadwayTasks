#!/bin/bash
airflow db init
airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@admin.com --password password
