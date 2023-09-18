from kafka import KafkaProducer
import io
from avro.io import DatumWriter, DatumReader, BinaryEncoder, BinaryDecoder
from avro.schema import parse
import time

# Avro schema definition
avro_schema_str = '''
{
    "type": "record",
    "name": "TransactionRecord",
    "fields": [
        {"name": "brandId", "type": "string"},
        {"name": "transactionHash", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}
'''

# Parse the Avro schema
avro_parsed_schema = parse(avro_schema_str)

# Configure Kafka producer
producer_config = {
    'bootstrap.servers': ['broker:9092'],
    'value.serializer': 'io.confluent.kafka.serializers.KafkaAvroSerializer',
    'schema.registry.url': 'http://schema-registry:8081'
}



producer = KafkaProducer(bootstrap_servers=['localhost:29092'])

# Topic to produce messages to
topic = 'your_topic_name'

def produce_avro_message(brand_id, transaction_hash):
    # Create an Avro writer
    avro_writer = DatumWriter(avro_parsed_schema)

    # Create a bytes buffer to store Avro message
    avro_buffer = io.BytesIO()

    # Create a dictionary with the message data
    message_data = {
        "brandId": brand_id,
        "transactionHash": transaction_hash,
        "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
    }

    # Serialize the message data to Avro format
    avro_writer.write(message_data, avro_buffer)

    # Get the Avro message bytes
    avro_message_bytes = avro_buffer.getvalue()

    # Produce the Avro-encoded message
    producer.produce(topic=topic, key=None, value=avro_message_bytes)
    producer.flush()

# Example usage:
brand_id = "YourBrandID"
transaction_hash = "YourTransactionHash"
produce_avro_message(brand_id, transaction_hash)
