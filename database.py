"""
Database connection and initialization.
Handles connecting to MySQL and creating the database/table if they don't exist.
"""

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

from config import DB_CONFIG


def get_connection():
    """Create and return a new database connection. Returns None on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None


def initialize_database():
    """
    Ensure the database and employees table exist.
    Call this once at application startup.
    """
    try:
        temp_config = DB_CONFIG.copy()
        database_name = temp_config.pop("database")
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        conn.database = database_name

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                emp_id VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                role VARCHAR(100),
                salary DECIMAL(10, 2)
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Error initializing database:\n{e}")
