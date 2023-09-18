import json
from kafka import KafkaConsumer
from utils.oracle import fetch_cost
from utils.fetchprice import fetch_eth_price
from utils.cockroach_connect import getConnection
import logging
from datetime import datetime
import re
from psycopg import sql

# Get mandatory connection
conn = getConnection(True)

def cockroachWrite(brandId, costInDollar):
    try:
        with conn.cursor() as cur:
                query = sql.SQL("SELECT balance FROM BrandAccount WHERE brandId = %s")
                cur.execute(query, [brandId])
                # Fetch the current balance
                current_balance = cur.fetchone()
                print(current_balance)

                if current_balance:
                    current_balance = current_balance[0]
                    # Subtract the value from the current balance
                    new_balance = current_balance - costInDollar
                    
                    # Define the SQL query to update the balance for the specified brandId
                    update_query = sql.SQL("UPDATE BrandAccount SET balance = %s WHERE brandId = %s")
                    
                    # Execute the update query
                    cur.execute(update_query, [new_balance, brandId])

                    # Commit the changes to the database
                    conn.commit()

                    print(f"Updated balance for brandId {brandId} to {new_balance}")

    except Exception as e:
        logging.error("Problem writing to database: {}".format(e))


consumer = KafkaConsumer('cost_logs',bootstrap_servers=['localhost:9092'],value_deserializer=lambda m:json.loads(m.decode('ascii')),auto_offset_reset='latest')
for msg in consumer:
    brandId = msg.value['brandid']
    costInDollar = msg.value['dollarcost']
    print(costInDollar)
    if(brandId and costInDollar):
        cockroachWrite(brandId,costInDollar)