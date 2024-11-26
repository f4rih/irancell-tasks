import os
from time import sleep

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


DATABASE = {
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': int(os.getenv('POSTGRES_PORT', '5432')),
    'dbname': os.getenv('POSTGRES_DB', 'irancell'),
    'user': os.getenv('POSTGRES_USER', 'irancell_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'Ir4nc3ll@S3cur3!p455w0rd'),

}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw (
    day TIMESTAMP,
    site TEXT,
    city TEXT,
    province TEXT,
    kpi_1 NUMERIC(25, 18),
    kpi_2 NUMERIC(25, 18),
    kpi_3 NUMERIC(25, 18),
    kpi_4 NUMERIC(25, 18),
    kpi_5 NUMERIC(25, 18),
    kpi_6 NUMERIC(25, 18),
    kpi_7 NUMERIC(25, 18),
    kpi_8 NUMERIC(25, 18),
    kpi_9 NUMERIC(25, 18),
    kpi_10 NUMERIC(25, 18),
    kpi_11 NUMERIC(25, 18),
    kpi_12 NUMERIC(25, 18),
    kpi_13 NUMERIC(25, 18),
    kpi_14 NUMERIC(25, 18),
    kpi_15 NUMERIC(25, 18),
    kpi_16 NUMERIC(25, 18),
    kpi_17 NUMERIC(25, 18),
    kpi_18 NUMERIC(25, 18),
    kpi_19 NUMERIC(25, 18),
    kpi_20 NUMERIC(25, 18)
);
"""

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(**DATABASE)
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for database to be ready...")
            sleep(5)

def load_csv_to_database():
    try:
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()

        cur.execute(CREATE_TABLE_SQL)
        print("Reading csv file ...")
        df = pd.read_csv('data.csv')

        # Insert query
        insert_query = """
            INSERT INTO raw (
            day, site, city, province, kpi_1, kpi_2, kpi_3, kpi_4, kpi_5,
            kpi_6, kpi_7, kpi_8, kpi_9, kpi_10, kpi_11, kpi_12, kpi_13,
            kpi_14, kpi_15, kpi_16, kpi_17, kpi_18, kpi_19, kpi_20
        ) VALUES %s
        """
        execute_values(cur, insert_query, df.values.tolist())
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Following error occurred:", e)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

if __name__ == '__main__':
    wait_for_db()
    load_csv_to_database()
    # we need wait here to preventing container to exit
    while True:
        sleep(60)