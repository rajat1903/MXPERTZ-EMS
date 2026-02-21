import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


# ----------------- DATABASE CONFIGURATION -----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # TODO: change this to your MySQL password
    "database": "employee_db",
}


def get_connection():
    """Create and return a new database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None


def initialize_database():
    """Ensure the database and employee table exist."""
    # First, connect without specifying database to ensure DB exists
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


# ----------------- DATABASE OPERATIONS -----------------
def add_employee(emp_id, name, role, salary):
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


# ----------------- TKINTER UI -----------------
class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x500")

        self.create_widgets()
        self.refresh_employee_table()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self.root, text="Employee Details", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Employee ID:").grid(row=0, column=0, sticky="w")
        self.emp_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.emp_id_var, width=20).grid(
            row=0, column=1, padx=5, pady=2
        )

        tk.Label(form_frame, text="Name:").grid(row=0, column=2, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var, width=25).grid(
            row=0, column=3, padx=5, pady=2
        )

        tk.Label(form_frame, text="Role:").grid(row=1, column=0, sticky="w")
        self.role_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.role_var, width=20).grid(
            row=1, column=1, padx=5, pady=2
        )

        tk.Label(form_frame, text="Salary:").grid(row=1, column=2, sticky="w")
        self.salary_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.salary_var, width=25).grid(
            row=1, column=3, padx=5, pady=2
        )

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Add Employee", width=15, command=self.on_add).pack(
            side="left", padx=5
        )
        tk.Button(btn_frame, text="Remove Employee", width=15, command=self.on_remove).pack(
            side="left", padx=5
        )
        tk.Button(btn_frame, text="Promote Employee", width=15, command=self.on_promote).pack(
            side="left", padx=5
        )
        tk.Button(btn_frame, text="Display Employees", width=18, command=self.refresh_employee_table).pack(
            side="left", padx=5
        )

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("emp_id", "name", "role", "salary")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )
        self.tree.heading("emp_id", text="Employee ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("salary", text="Salary")

        self.tree.column("emp_id", width=100)
        self.tree.column("name", width=200)
        self.tree.column("role", width=150)
        self.tree.column("salary", width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        emp_id, name, role, salary = item["values"]
        self.emp_id_var.set(emp_id)
        self.name_var.set(name)
        self.role_var.set(role)
        self.salary_var.set(str(salary))

    def on_add(self):
        emp_id = self.emp_id_var.get().strip()
        name = self.name_var.get().strip()
        role = self.role_var.get().strip()
        salary_str = self.salary_var.get().strip()

        if not emp_id or not name:
            messagebox.showwarning(
                "Input Error", "Employee ID and Name are required."
            )
            return

        salary = None
        if salary_str:
            try:
                salary = float(salary_str)
            except ValueError:
                messagebox.showwarning("Input Error", "Salary must be a number.")
                return

        add_employee(emp_id, name, role if role else None, salary)
        self.refresh_employee_table()

    def on_remove(self):
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            messagebox.showwarning(
                "Input Error", "Please enter or select an Employee ID to remove."
            )
            return
        remove_employee(emp_id)
        self.refresh_employee_table()

    def on_promote(self):
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            messagebox.showwarning(
                "Input Error", "Please enter or select an Employee ID to promote."
            )
            return

        new_role = self.role_var.get().strip() or None
        salary_str = self.salary_var.get().strip()
        new_salary = None
        if salary_str:
            try:
                new_salary = float(salary_str)
            except ValueError:
                messagebox.showwarning("Input Error", "Salary must be a number.")
                return

        promote_employee(emp_id, new_role, new_salary)
        self.refresh_employee_table()

    def refresh_employee_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        employees = get_all_employees()
        for emp in employees:
            self.tree.insert("", "end", values=emp)


def main():
    initialize_database()
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

