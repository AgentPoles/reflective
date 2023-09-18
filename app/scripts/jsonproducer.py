import msgpack
import json
from kafka import KafkaProducer
import time

# block until all async messages are sent

 # produce json messages
producer3 = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda m:json.dumps(m).encode('ascii'))

def produce_avro_message(brand_id, transaction_hash):

    message_object = {
            "brandId": brand_id,
            "transactionHash": transaction_hash,
            "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
        }

    producer3.send('transaction_logs',message_object)

    producer3.flush() 
    # block until all asyncmessages are sent

def produce_cost_logs(brandId, costInDollar):
    message_object = {
            "brandid": brandId,
            "dollarcost": costInDollar
        }

    producer3.send('cost_logs',message_object)

    producer3.flush() 
    # block until all asyncmessages are sent