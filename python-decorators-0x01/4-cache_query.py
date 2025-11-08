#!/usr/bin/python3
"""
A decorator that caches database query results to avoid redundant calls.
"""

import sqlite3
import functools
import time


# Global in-memory cache dictionary
query_cache = {}


def with_db_connection(func):
    """
    Decorator that automatically opens and closes a SQLite database connection.
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


def cache_query(func):
    """
    Decorator that caches query results to avoid redundant DB calls.
    Caching is based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query string from args or kwargs
        query = kwargs.get('query')
        if not query and len(args) > 1:
            query = args[1]

        if query in query_cache:
            print(f"[CACHE] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[DB] Executing query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Query cached successfully.")
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database with caching support.
    The first call executes the query and caches the result.
    The second call returns from cache.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call — should hit the database
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call — should return from cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
