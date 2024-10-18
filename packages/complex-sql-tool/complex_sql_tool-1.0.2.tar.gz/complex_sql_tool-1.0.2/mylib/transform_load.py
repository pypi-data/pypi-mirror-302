"""Module for data transformation and loading."""

import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv


def load():
    """Loads the data into the MySQL database."""
    load_dotenv()
    db_config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "autocommit": True,
    }
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        print("Creating tables...")
        with open("sql/create_tables.sql", "r", encoding="utf-8") as f:
            create_tables_sql = f.read()
        for statement in create_tables_sql.strip().split(";"):
            if statement.strip():
                cursor.execute(statement + ";")
        print("Tables created successfully.")

        data_dir = "data"
        data_file = os.path.join(data_dir, "adult.data")
        column_names = [
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education_num",
            "marital_status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital_gain",
            "capital_loss",
            "hours_per_week",
            "native_country",
            "income",
        ]

        print("Loading data...")
        df = pd.read_csv(data_file, names=column_names, sep=",\\s", engine="python")
        df = df.replace("?", None)

        df["id"] = df.index + 1

        # table：personal_info
        personal_info = df[
            ["id", "age", "sex", "race", "native_country", "marital_status", "relationship"]
        ]

        # table：employment_info
        employment_info = df[
            [
                "id",
                "workclass",
                "occupation",
                "education",
                "education_num",
                "hours_per_week",
                "capital_gain",
                "capital_loss",
                "fnlwgt",
            ]
        ]

        # table：income_info
        income_info = df[["id", "income"]]

        print("Inserting data into personal_info table...")
        personal_info_records = personal_info.where(pd.notnull(personal_info), None).values.tolist()
        cursor.executemany(
            """
            INSERT INTO personal_info (id, age, sex, race, native_country, marital_status, relationship)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
            personal_info_records,
        )

        print("Inserting data into employment_info table...")
        employment_info_records = employment_info.where(
            pd.notnull(employment_info), None
        ).values.tolist()
        cursor.executemany(
            """
            INSERT INTO employment_info (id, workclass, occupation, education, education_num, hours_per_week, capital_gain, capital_loss, fnlwgt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
            employment_info_records,
        )

        print("Inserting data into income_info table...")
        income_info_records = income_info.where(pd.notnull(income_info), None).values.tolist()
        cursor.executemany(
            """
            INSERT INTO income_info (id, income)
            VALUES (%s, %s);
        """,
            income_info_records,
        )

        conn.close()
        print("Data loaded successfully.")

    except Exception as e:
        print(f"An error occurred during loading: {e}")
