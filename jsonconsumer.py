import json
from kafka import KafkaConsumer
from oracle import fetch_cost
from fetchprice import fetch_eth_price
from cockroach_connect import getConnection
import logging
from datetime import datetime
import re
from psycopg import sql
from jsonproducer import produce_cost_logs
# Get mandatory connection
conn = getConnection(True)

def cockroachWrite(timestamp, brandId, transactionHash, costInEth, costInDollar):
    try:
        conn.autocommit = True
        timestamp = int(timestamp/1000)
        eventTimestamp = datetime.fromtimestamp(timestamp)
        eventTimestamp = datetime.fromtimestamp(timestamp) #convert event.timestamp from epoch to datetime
        
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS TransactionRecords (id SERIAL PRIMARY KEY, timestamp TIMESTAMP, brandId STRING, transactionHash STRING, costInEth FLOAT, costInDollar FLOAT)")
            logging.debug("create_accounts(): status message: %s",cur.statusmessage)
            if timestamp and transactionHash:
                cur.execute("INSERT INTO TransactionRecords (timestamp, brandId, transactionHash, costInEth, costInDollar ) VALUES (%s, %s, %s, %s, %s)", (eventTimestamp, brandId, transactionHash, costInEth, costInDollar ))
                conn.commit()
                produce_cost_logs(brandId=brandId, costInDollar=costInDollar)

    except Exception as e:
        logging.error("Problem writing to database: {}".format(e))


consumer = KafkaConsumer('transaction_logs',bootstrap_servers=['localhost:9092'],value_deserializer=lambda m:json.loads(m.decode('ascii')),auto_offset_reset='latest')
for msg in consumer:
    timestamp = msg.value['timestamp']
    brandId = msg.value['brandId']
    transactionHash = msg.value['transactionHash']
    cost_in_eth = fetch_cost(transaction_hash=transactionHash)
    eth_price = fetch_eth_price()
    dollar_cost = 0
    if(cost_in_eth and eth_price):  dollar_cost = cost_in_eth * eth_price
    print(cost_in_eth, eth_price, dollar_cost)
    cockroachWrite(msg.timestamp,brandId,transactionHash,cost_in_eth,dollar_cost)