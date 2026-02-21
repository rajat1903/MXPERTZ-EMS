import tkinter as tk

from database import initialize_database
from ui import EmployeeApp


def main():
    initialize_database()
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
