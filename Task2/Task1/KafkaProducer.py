import json
from confluent_kafka import Producer
import pandas as pd

class KafkaProducer:
    def __init__(self):
        # Initialize Kafka producer with your Kafka configuration
        self.kafka_producer = Producer({'bootstrap.servers': 'kafka:9092'})  # Replace with your Kafka broker(s)

    def produce_time_series_to_kafka(self, time_series_data, kafka_topic, generator_id, attribute_id):
        """
        Produce a DataFrame to a Kafka topic with JSON serialization.

        Args:
            time_series_data (pd.DataFrame): The DataFrame to send to Kafka.
            kafka_topic (str): The name of the Kafka topic to send the data.
            generator_id (str): The generator_id to include in the message.
            attribute_id (str): The attribute_id to include in the message.
        """
        # Convert the entire DataFrame to a JSON string
        dataframe_json = time_series_data.to_json(orient='records', lines=True)

        # Create a message that includes the entire DataFrame
        message = {
            'attributeId': attribute_id,
            'assetId': generator_id,
            'data': dataframe_json
        }

        # Serialize the message to JSON
        message_json = json.dumps(message)

        # Send the JSON message as a message to the Kafka topic
        self.kafka_producer.produce(kafka_topic, key=None, value=message_json)

        # Wait for any outstanding messages to be delivered and delivery reports received
        self.kafka_producer.flush()

        print(f"DataFrame sent to Kafka topic '{kafka_topic}' with JSON serialization.")
