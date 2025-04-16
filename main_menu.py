import tkinter as tk
from report import report_window
from view_reports import view_reports_window
from safe_route_ui import open_safe_route_window

def open_main_menu(user):
    menu = tk.Toplevel()
    menu.update_idletasks()
    menu.title("Main Menu")
    menu.geometry("300x200")

    tk.Label(menu, text=f"Welcome, {user[1]}").pack(pady=10)
    tk.Button(menu, text="Add Report", command=lambda: report_window(user)).pack(pady=5)
    tk.Button(menu, text="View My Reports", command=lambda: view_reports_window(user)).pack(pady=5)
    tk.Button(menu, text="Get Safe Route", command=open_safe_route_window).pack(pady=10)

    tk.Button(menu, text="Logout", command=menu.destroy).pack(pady=5)
