#!/usr/bin/python3
"""
A decorator that manages database transactions.
Automatically commits or rolls back changes.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that opens and closes a SQLite database connection automatically.
    Passes the connection to the wrapped function.
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


def transactional(func):
    """
    Decorator that wraps a function in a transaction.
    Commits if successful, rolls back if an error occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[LOG] Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[LOG] Transaction rolled back due to error: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email address by ID.
    Automatically handled inside a transaction.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"[LOG] Updated user ID {user_id} email to {new_email}")


# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
