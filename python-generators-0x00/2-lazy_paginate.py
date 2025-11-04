#!/usr/bin/python3
"""
Lazy loading paginated user data using Python generators.
Simulates pagination by fetching one page at a time on demand.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users using LIMIT and OFFSET.
    Args:
        page_size (int): Number of rows per page.
        offset (int): Starting position for the page.

    Returns:
        list[dict]: A list of users for the given page.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches and yields pages of users.
    Uses only one loop to control pagination flow.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ yield one page (list of users)
        offset += page_size  # move to next page
