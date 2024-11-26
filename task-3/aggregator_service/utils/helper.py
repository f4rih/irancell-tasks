import time
import psycopg2
from psycopg2 import sql
from .db import (
    DATABASE,
    create_table
)

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(**DATABASE)
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for database and csv loader service to be ready...")
            time.sleep(5)


def perform_aggregation_and_insert(conn, df, kpi, agg_func):
    """
    Perform aggregation for a specific KPI and insert into a new table.
    """
    GROUP_BY_COLUMNS = ['site', 'city', 'province']
    table_name = f'{kpi}_aggregations'

    for column in GROUP_BY_COLUMNS:
        if agg_func == "avg":
            agg_func = "mean"
        agg_result = df.groupby(column)[kpi].agg(agg_func).reset_index()
        agg_result.columns = [column, "value"]

        # Create the table for the KPI
        with conn.cursor() as cursor:
            create_table(cursor, table_name)
            conn.commit()

        # Insert data into the table
        with conn.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO {table_name} (field_type, field_name, value, agg_type)
                VALUES (%s, %s, %s, %s)
            """).format(
                table_name=sql.Identifier(table_name),
            )
            for _, row in agg_result.iterrows():
                cursor.execute(insert_query, (column, row[column], row["value"], agg_func))
            conn.commit()