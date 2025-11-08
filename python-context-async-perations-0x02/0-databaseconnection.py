#!/usr/bin/python3
"""
A custom class-based context manager for database connections.
Automatically opens and closes the SQLite database connection.
"""

import sqlite3


class DatabaseConnection:
    """
    A context manager class that handles connecting to and closing a SQLite database.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Opens the database connection and returns the cursor."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print("[LOG] Database connection opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures that the database connection is properly closed.
        Commits the transaction if no exception occurred,
        otherwise rolls back.
        """
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_value}. Rolling back transaction.")
            self.connection.rollback()
        else:
            self.connection.commit()
            print("[LOG] Transaction committed successfully.")

        self.connection.close()
        print("[LOG] Database connection closed.")
        # Returning False re-raises any exception after cleanup
        return False


# Example usage
if __name__ == "__main__":
    db_file = "users.db"

    with DatabaseConnection(db_file) as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("[RESULT] Users fetched from database:")
        for user in users:
            print(user)
