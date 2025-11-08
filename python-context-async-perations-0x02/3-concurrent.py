#!/usr/bin/python3
"""
Concurrent Asynchronous Database Queries using aiosqlite and asyncio.gather
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously from the database."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[LOG] Fetched all users.")
            return users


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("[LOG] Fetched users older than 40.")
            return older_users


async def fetch_concurrently():
    """
    Run both fetch operations concurrently using asyncio.gather().
    """
    print("[LOG] Running concurrent queries...")
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users, older_users = results

    print(f"[RESULT] Total users fetched: {len(all_users)}")
    print(f"[RESULT] Users older than 40 fetched: {len(older_users)}")

    # Display sample data
    print("\n--- Sample All Users ---")
    for user in all_users[:3]:
        print(user)

    print("\n--- Sample Older Users ---")
    for user in older_users[:3]:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
