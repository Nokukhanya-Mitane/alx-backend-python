#!/usr/bin/python3
"""
A decorator that logs SQL queries before executing them.
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs SQL queries executed by the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No query provided.")
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
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
