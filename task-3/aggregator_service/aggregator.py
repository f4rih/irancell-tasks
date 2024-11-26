import time

import pandas as pd
from utils import (
    AGGREGATION,
    connect_to_db,
    perform_aggregation_and_insert,
    wait_for_db,
    wait_for_csv_loader_service
)


def main():
    # Wait for csv loader service to insert data
    wait_for_csv_loader_service()
    # Connect to the database
    conn = connect_to_db()

    # Load raw data from the database into a DataFrame
    raw_query = "SELECT * FROM raw;"
    raw_df = pd.read_sql(raw_query, conn)

    # Process each KPI
    for kpi, agg_func in AGGREGATION.items():
        print(f"Processing {kpi} with {agg_func} aggregation...")

        # perform aggregation
        perform_aggregation_and_insert(conn, raw_df, kpi, agg_func)

    # Close the connection
    conn.close()
    print("Aggregation process completed.")


if __name__ == "__main__":
    wait_for_db()
    main()
    while True:
        time.sleep(60)