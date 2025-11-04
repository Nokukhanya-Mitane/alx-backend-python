#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import txt
import uuid


def connect_db():
    """Connect to the MySQL server (no DB selected)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ilikelearning'  
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Error while creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ilikelearning', 
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error while creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert data from your user_data.txt (CSV-formatted) file."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name'].strip()
                email = row['email'].strip()
                age = row['age'].strip()

                # Check if user already exists (by email)
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        print("Data inserted successfully.")
    except FileNotFoundError:
        print(f"TXT file '{txt_file}' not found.")
    except Error as e:
        print(f"Error while inserting data: {e}")
    finally:
        cursor.close()
