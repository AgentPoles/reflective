from kafka import KafkaProducer
import fastavro
import time
import io
# Create a Kafka producer client
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
# Load the Avro schema from a file
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


def produce_avro_message(brand_id, transaction_hash):
        # Define the message as a dictionary following the Avro schema

    
    message_object = {
            "brandId": brand_id,
            "transactionHash": transaction_hash,
            "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
        }


    # Serialize the message using fastavro and the loaded schema
    buf = io.BytesIO()
    fastavro.schemaless_writer(buf, schema, message_object)
    message_data = buf.getvalue()
        # Message key (if needed)
    key = None

        # Message headers (if needed)
    headers = []

        # Send the serialized message to the Kafka topic
    producer.send(
            'transaction_logs',
            value=message_data,  # The serialized Avro message
            key=key,  # Message key (if needed)
            headers=headers  # Message headers (if needed)
        )

        # Ensure all buffered messages are sent
    producer.flush()
