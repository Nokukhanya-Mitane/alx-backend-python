#!/usr/bin/python3
"""
Batch processing of user data from the database using generators.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.

    Args:
        batch_size (int): Number of rows per batch.

    Yields:
        list[dict]: A list of user records (each as a dictionary).
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ilikelearning',  
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  # ✅ Yield one batch at a time

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Process batches of users and print those over age 25.

    Args:
        batch_size (int): Number of rows per batch to process.
    """
    # ✅ Loop 1: iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # ✅ Loop 2: iterate through each user in the batch
        for user in batch:
            try:
                if float(user['age']) > 25:
                    print(user)
            except (ValueError, TypeError):
                continue
