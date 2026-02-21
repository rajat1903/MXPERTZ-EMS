"""
Application configuration for the Employee Management System.
Edit DB_CONFIG to match your MySQL server (host, user, password, database name).
"""

# ----------------- DATABASE CONFIGURATION -----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # TODO: change this to your MySQL password
    "database": "employee_db",
}

# Optional: app-level constants (e.g. window size) can go here later
APP_TITLE = "Employee Management System"
WINDOW_GEOMETRY = "800x500"
