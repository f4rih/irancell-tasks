import os
import time

import psycopg2
from psycopg2 import sql

DATABASE = {
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': int(os.getenv('POSTGRES_PORT', '5432')),
    'dbname': os.getenv('POSTGRES_DB', 'irancell'),
    'user': os.getenv('POSTGRES_USER', 'irancell_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'Ir4nc3ll@S3cur3!p455w0rd'),

}

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(**DATABASE)
    return conn


def wait_for_csv_loader_service():
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        );
    """
    conn = connect_to_db()
    while True:
        with conn.cursor() as cursor:
            cursor.execute(query, ('public', 'raw'))
            exists = cursor.fetchone()[0]
            if exists:
                break
        time.sleep(10)

def create_table(cursor, table_name):
    """Create a table dynamically for each KPI aggregation."""
    create_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            field_type varchar(50),
            field_name varchar(100),
            value NUMERIC(25, 18),
            agg_type varchar(10)
        )
    """).format(
        table_name=sql.Identifier(table_name),
    )
    cursor.execute(create_query)