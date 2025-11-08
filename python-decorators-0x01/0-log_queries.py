#!/usr/bin/python3
"""
A decorator that logs SQL queries before executing them.
"""

import sqlite3
import functools
import datetime


def log_queries(func):
    """
    Decorator that logs SQL queries executed by the decorated function.
    Logs the time and the exact SQL query before execution.
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument (positional or keyword)
        query = kwargs.get("query") or (args[0] if args else None)

        # Log timestamp and query
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] [LOG] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] [LOG] No SQL query provided.")

        # Execute the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Executes the provided SQL query and returns all results.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    # Fetch all users and log the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
