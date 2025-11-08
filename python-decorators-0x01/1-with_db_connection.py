#!/usr/bin/python3
"""
A decorator that automatically manages database connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that opens and closes a SQLite database connection automatically.
    The connection is passed as the first argument to the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection to the wrapped function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close connection, even if an error occurs
            conn.close()
            print("[LOG] Database connection closed.")
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a single user record by ID using the provided connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
