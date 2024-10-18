"""Module for executing queries."""

import os
import mysql.connector
from dotenv import load_dotenv
from tabulate import tabulate


def query(query_name):
    """Executes a specified query."""
    load_dotenv()
    db_config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
    }

    query_file = f"sql/{query_name}.sql"
    if not os.path.exists(query_file):
        print(f"Query file '{query_file}' does not exist.")
        return None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        with open(query_file, "r", encoding="utf-8") as f:
            sql_query = f.read()

        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]

        print(f"Results for query '{query_name}':")
        print(tabulate(results, headers=column_names, tablefmt="psql"))

        conn.close()
        return results
    except Exception as e:
        print(f"An error occurred during querying: {e}")
        return None
