
# Use an official Airflow image as the base image
FROM apache/airflow:2.7.3

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Switch to root to perform privileged operations
USER root

# Set permissions using sudo
RUN mkdir -p /djangoapp \
    && chmod 777 /djangoapp


