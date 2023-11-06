FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create the output_data directory and set permissions
RUN mkdir -p /etc/kafka/secrets/output_data \
    && chmod 777 /etc/kafka/secrets/output_data

# Copy the rest of the application code
COPY . /app/
