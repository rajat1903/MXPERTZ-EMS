"""
User interface for the Employee Management System.
Builds the Tkinter window: form, buttons, and employee table.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import APP_TITLE, WINDOW_GEOMETRY
from employee_operations import (
    add_employee,
    remove_employee,
    promote_employee,
    get_all_employees,
)


class EmployeeApp:
    """Main application window: form to add/remove/promote employees and a table to display them."""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)

        self.create_widgets()
        self.refresh_employee_table()

    def create_widgets(self):
        """Create the form frame, buttons, and the employee table (Treeview)."""
        # ----- Form: Employee ID, Name, Role, Salary -----
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

        # ----- Buttons -----
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
        tk.Button(
            btn_frame, text="Display Employees", width=18, command=self.refresh_employee_table
        ).pack(side="left", padx=5)

        # ----- Table (Treeview) -----
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("emp_id", "name", "role", "salary")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("emp_id", text="Employee ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("salary", text="Salary")

        self.tree.column("emp_id", width=100)
        self.tree.column("name", width=200)
        self.tree.column("role", width=150)
        self.tree.column("salary", width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def on_row_select(self, event):
        """When a row is selected, fill the form with that employee's data."""
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
        """Validate form and add employee; then refresh the table."""
        emp_id = self.emp_id_var.get().strip()
        name = self.name_var.get().strip()
        role = self.role_var.get().strip()
        salary_str = self.salary_var.get().strip()

        if not emp_id or not name:
            messagebox.showwarning("Input Error", "Employee ID and Name are required.")
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
        """Remove the employee whose ID is in the form; then refresh the table."""
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            messagebox.showwarning(
                "Input Error", "Please enter or select an Employee ID to remove."
            )
            return
        remove_employee(emp_id)
        self.refresh_employee_table()

    def on_promote(self):
        """Update role/salary for the employee whose ID is in the form; then refresh the table."""
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
        """Clear the table and reload all employees from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        employees = get_all_employees()
        for emp in employees:
            self.tree.insert("", "end", values=emp)
