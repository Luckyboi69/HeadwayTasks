import json
from confluent_kafka import Consumer, KafkaError
import pandas as pd

class KafkaConsumer:
    def __init__(self, kafka_topic):
        kafka_config = {
            'bootstrap.servers': 'kafka:9092',  # Update with your Kafka broker(s)
            'group.id': 'my-group',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(kafka_config)
        self.kafka_topic = kafka_topic
        self.output_dir = './Task1/sample_datasets'
        self.count = 1  # Counter for file naming

    def consume_and_save(self):
        self.consumer.subscribe([self.kafka_topic])

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue  # Continue the loop when there are no messages

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached the end of the partition")
                    break  # Exit the loop
                else:
                    print(f"Error while consuming: {msg.error()}")
                    break  # Exit the loop

            try:
                # Deserialize the JSON message
                message = json.loads(msg.value())

                # Extract the DataFrame from the message
                dataframe_json = message.get('data')
                if dataframe_json:
                    df = pd.read_json(dataframe_json, orient='records', lines=True)

                    # Save the DataFrame as a CSV file with a numbered name
                    file_name = f"{self.output_dir}/message_{self.count}.csv"
                    df.to_csv(file_name, index=False)
                    print(f"Saved message to {file_name}")

                    # Increment the counter for the next file
                    self.count += 1

            except Exception as e:
                print(f"Error processing message: {e}")

        # Close the consumer after processing all messages
        self.consumer.close()
