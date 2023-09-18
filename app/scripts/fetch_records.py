
import psycopg
import logging
from psycopg import sql

# Define connection to your CockroachDB cluster
def init_conn():
    db_url = 'postgresql://localhost:26257/defaultdb?sslrootcert=/Users/poamen/projects/pau/drp/assignments/stream-from-file/cockroachdb1/certs/ca.crt&sslkey=/Users/poamen/projects/pau/drp/assignments/stream-from-file/cockroachdb1/certs/client.paul.key.pk8&sslcert=/Users/poamen/projects/pau/drp/assignments/stream-from-file/cockroachdb1/certs/client.paul.crt&sslmode=verify-full&user=paul&password="@Password1"'
    conn = psycopg.connect(db_url, application_name="kaftka-cockroach illustration")
    return conn

# Get connection
def getConnection(mandatory):
    try:
        conn = init_conn()
        print("successful")
        return conn
    except Exception as e:
        logging.fatal("Database connection failed: {}".format(e))
        print("failed")
        if mandatory:
            exit(1)  # database connection must succeed to proceed.



def cockroachRead(brandId):
    conn = getConnection(True)
    try:
        with conn.cursor() as cur:
                query = sql.SQL("SELECT balance FROM BrandAccount WHERE brandId = %s")
                queryb = sql.SQL("SELECT * FROM TransactionRecords WHERE brandId = %s")
                cur.execute(query, [brandId])
                # Fetch the current balance
                current_balance = cur.fetchone()

                cur.execute(queryb, [brandId])
                data = cur.fetchall()

                # Get the column names from the cursor description
                column_names = [desc[0] for desc in cur.description]
               

                conn.commit()

                return current_balance[0], data, column_names

    except Exception as e:
        logging.error("Problem writing to database: {}".format(e))

