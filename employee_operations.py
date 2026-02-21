"""
Employee CRUD operations: add, remove, promote, and list employees.
Uses the database connection from database.py and shows user feedback via messagebox.
"""

from tkinter import messagebox
from mysql.connector import Error

from database import get_connection


def add_employee(emp_id, name, role, salary):
    """Insert a new employee. emp_id and name are required."""
    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (emp_id, name, role, salary) VALUES (%s, %s, %s, %s)",
            (emp_id, name, role, salary),
        )
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully.")
    except Error as e:
        messagebox.showerror("Database Error", f"Error adding employee:\n{e}")
    finally:
        cursor.close()
        conn.close()


def remove_employee(emp_id):
    """Delete an employee by emp_id."""
    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
        if cursor.rowcount == 0:
            messagebox.showwarning("Not Found", "No employee found with the given ID.")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Employee removed successfully.")
    except Error as e:
        messagebox.showerror("Database Error", f"Error removing employee:\n{e}")
    finally:
        cursor.close()
        conn.close()


def promote_employee(emp_id, new_role=None, new_salary=None):
    """Update an employee's role and/or salary. At least one of new_role or new_salary must be provided."""
    if not new_role and new_salary is None:
        messagebox.showwarning(
            "Input Error", "Please provide a new role and/or a new salary to promote."
        )
        return

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if new_role:
            updates.append("role = %s")
            params.append(new_role)
        if new_salary is not None:
            updates.append("salary = %s")
            params.append(new_salary)

        params.append(emp_id)
        sql = f"UPDATE employees SET {', '.join(updates)} WHERE emp_id = %s"
        cursor.execute(sql, tuple(params))

        if cursor.rowcount == 0:
            messagebox.showwarning("Not Found", "No employee found with the given ID.")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Employee promoted/updated successfully.")
    except Error as e:
        messagebox.showerror("Database Error", f"Error promoting employee:\n{e}")
    finally:
        cursor.close()
        conn.close()


def get_all_employees():
    """Return a list of (emp_id, name, role, salary) for all employees. Returns [] on error."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, role, salary FROM employees ORDER BY id")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching employees:\n{e}")
        return []
    finally:
        cursor.close()
        conn.close()
