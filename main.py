"""
Entry point for the Employee Management System.
Run this file to start the application:  python main.py
"""

import tkinter as tk

from database import initialize_database
from ui import EmployeeApp


def main():
    """Initialize the database, create the main window, and start the event loop."""
    initialize_database()
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
