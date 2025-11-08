#!/usr/bin/python3
"""
A decorator that retries database operations automatically
if they fail due to transient errors.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that automatically opens and closes a SQLite database connection.
    Passes the connection as the first argument to the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("[LOG] Database connection closed.")
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a database operation if it fails due to an exception.
    :param retries: number of retry attempts
    :param delay: delay in seconds between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    attempt += 1
                    print(f"[LOG] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"[LOG] Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("[LOG] Max retries reached. Raising exception.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the users table with retry logic.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"[ERROR] Failed to fetch users: {e}")
