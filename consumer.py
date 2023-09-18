from confluent_kafka import Consumer, KafkaError
from avro import schema, io
import io as std_io

# Avro schema definition (must match the schema used for producing)
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
avro_parsed_schema = schema.parse(avro_schema_str)

# Configure Kafka consumer
consumer_config = {
    'bootstrap.servers': ['broker:9092'],
    'group.id': '1',
    'auto.offset.reset': 'earliest',
    'key.deserializer': 'io.confluent.kafka.serializers.StringDeserializer',
    'value.deserializer': 'io.confluent.kafka.serializers.KafkaAvroDeserializer',
    'schema.registry.url': 'http://schema-registry:8081'
}

# Create a Kafka consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
topic = 'your_topic_name'
consumer.subscribe([topic])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print('Error occurred: {}'.format(msg.error()))
    else:
        # Deserialize the Avro message
        avro_reader = io.DatumReader(avro_parsed_schema)
        avro_message_bytes = msg.value()
        avro_message_stream = std_io.BytesIO(avro_message_bytes)
        avro_message = avro_reader.read(avro_message_stream)

        # Extract fields from the Avro message
        brand_id = avro_message["brandId"]
        transaction_hash = avro_message["transactionHash"]
        timestamp_ms = avro_message["timestamp"]

        # Print the extracted data
        print('Brand ID:', brand_id)
        print('Transaction Hash:', transaction_hash)
        print('Timestamp (ms):', timestamp_ms)
