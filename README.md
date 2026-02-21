# Employee Management System (MXPERTZ-EMS)

A simple **database-driven Employee Management System** built with **Python**, **Tkinter** for the GUI, and **MySQL** for persistent storage.

## Features

- **Add Employee**: Insert a new employee record into the database.
- **Remove Employee**: Delete an employee record by Employee ID.
- **Promote Employee**: Update an existing employee's role and/or salary.
- **Display Employees**: View all employees from the database in a table.

## Requirements

- Python 3.9+ (Tkinter is included with most Python installers)
- MySQL Server running locally or accessible over the network

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configure Database Connection

Edit `config.py` to match your MySQL setup:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "employee_db",
}
```

Make sure the MySQL user exists and has permission to create tables in the given database.

## Run the Program

```bash
python main.py
```

Or:

```bash
python employee_management.py
```

The Tkinter window will open and you can use the buttons to **Add**, **Remove**, **Promote**, and **Display** employees.

## Project structure

| File | Purpose |
|------|--------|
| **main.py** | Entry point: initializes DB and starts the Tkinter app. |
| **config.py** | Database and app settings. Edit here to change MySQL credentials. |
| **database.py** | Connection and setup: `get_connection()`, `initialize_database()`. |
| **employee_operations.py** | CRUD: add, remove, promote, list employees. |
| **ui.py** | Tkinter UI: form, buttons, employee table. |
| **employee_management.py** | Launcher that calls `main()`; use `main.py` directly if you prefer. |

---
