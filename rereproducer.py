from kafka import KafkaProducer
import io

from avro.io import DatumWriter, BinaryEncoder
import time

# Create a Kafka producer client
producer = KafkaProducer(bootstrap_servers=['localhost:29092'])

# Load the Avro schema from a file
schema =  {
    "type": "record",
    "name": "TransactionRecord",
    "fields": [
        {"name": "brandId", "type": "string"},
        {"name": "transactionHash", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}


def produce_avro_message(brand_id, transaction_hash):
    # Serialize the message data using the schema
    buf = io.BytesIO()
    encoder = BinaryEncoder(buf)
    writer = DatumWriter(schema)
    message_data = {
        "brandId": brand_id,
        "transactionHash": transaction_hash,
        "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
    }
    writer.write(message_data, encoder)
    buf.seek(0)
    message_data = buf.read()

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
