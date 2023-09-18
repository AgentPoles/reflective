# producer.py

from confluent_kafka import Producer
import fastavro.schema
import random
import string

# Define Avro schema
avro_schema = {
    "type": "record",
    "name": "MyMessage",
    "fields": [
        {"name": "brandId", "type": "string"},
        {"name": "transactionHash", "type": "string"}
    ]
}

# Create an Avro schema object
schema = fastavro.schema.parse(avro_schema)

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'your_kafka_broker',
    'schema.registry.url': 'http://your_schema_registry_url',
    'key.serializer': 'io.confluent.kafka.serializers.StringSerializer',
    'value.serializer': 'io.confluent.kafka.serializers.KafkaAvroSerializer'
}



# Create a Kafka producer instance
producer = Producer(producer_config)

# Function to produce Avro-encoded message
def produce_avro_message(brand_id, transaction_hash):
    message = {"brandId": brand_id, "transactionHash": transaction_hash}
    producer.produce(topic='your_topic_name', value=message, value_schema=schema)
    producer.flush()
