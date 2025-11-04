#!/usr/bin/python3
"""
Memory-efficient aggregation using generators.
Compute average user age without loading full dataset into memory.
"""

import seed


def stream_user_ages():
    """
    Generator that streams (yields) user ages one by one from the database.
    Yields:
        int or float: The user's age.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:  # ✅ Loop 1: stream each user's age
        yield float(row['age'])

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates the average user age using the generator stream_user_ages.
    Prints: "Average age of users: X.YY"
    """
    total_age = 0
    count = 0

    # ✅ Loop 2: iterate through generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
