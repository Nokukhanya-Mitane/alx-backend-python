#!/usr/bin/python3
"""
Generator that streams rows from user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Connect to the ALX_prodev database and yield rows one by one
    from the user_data table as dictionaries.
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

            # Yield one row at a time
            for row in cursor:
                yield row

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
