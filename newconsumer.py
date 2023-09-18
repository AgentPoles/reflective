from kafka import KafkaConsumer
import fastavro
import io


# Create a Kafka consumer client
consumer = KafkaConsumer(
    'transaction_logs',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest'  
)

# Load the Avro schema from a file in the same folder as bytes
with open("transaction_schema.avsc", "rb") as schema_file:
    schema = {
        "type": "record",
        "name": "TransactionRecord",
        "fields": [
            {"name": "transactionHash", "type": "string"},
            {"name": "brandId", "type": "string"},
            {"name": "timestamp", "type": "long"}
        ]
    }

# Iterate over messages and deserialize Avro data
for message in consumer:
    avro_data = message.value  # Assuming messages are Avro-encoded
    print(avro_data)
    # Deserialize the Avro data using fastavro
    avro_reader = fastavro.reader(io.BytesIO(avro_data), schema)
    deserialized_data = next(avro_reader)

    # Access the deserialized data fields
    transaction_hash = deserialized_data["transactionHash"]
    brand_id = deserialized_data["brandId"]
    timestamp = deserialized_data["timestamp"]

    # Perform your processing with the deserialized data
    print(f"Transaction Hash: {transaction_hash}")
    print(f"Brand ID: {brand_id}")
    print(f"Timestamp: {timestamp}")
    print()

# Close the Kafka consumer when done
consumer.close()
