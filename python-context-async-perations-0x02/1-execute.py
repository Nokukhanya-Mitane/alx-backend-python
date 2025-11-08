#!/usr/bin/python3
"""
A reusable class-based context manager that handles database connection
and executes a given SQL query with parameters.
"""

import sqlite3


class ExecuteQuery:
    """
    A context manager that:
    - Opens a SQLite database connection
    - Executes a given SQL query with parameters
    - Returns the query results on entry
    - Closes the connection automatically on exit
    """

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Opens the database connection, executes the query, and returns the results."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("[LOG] Database connection opened.")
            print(f"[LOG] Executing query: {self.query} | Params: {self.params}")

            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            return self.results

        except Exception as e:
            print(f"[ERROR] Query execution failed: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures proper cleanup:
        - Commits if no error occurred
        - Rolls back on error
        - Closes connection
        """
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_value}. Rolling back.")
            if self.connection:
                self.connection.rollback()
        else:
            if self.connection:
                self.connection.commit()
                print("[LOG] Transaction committed successfully.")

        if self.connection:
            self.connection.close()
            print("[LOG] Database connection closed.")

        # Returning False allows exception to propagate if any
        return False


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print("[RESULT] Query Results:")
        for row in results:
            print(row)
