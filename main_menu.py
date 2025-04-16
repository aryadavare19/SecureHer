# main_menu.py
import tkinter as tk
from report import report_window
from view_reports import view_reports_window
from safe_route_ui import open_safe_route_window
from location_danger_history import open_danger_location_ui

def open_main_menu(user):
    menu = tk.Toplevel()
    menu.update_idletasks()
    menu.title("Main Menu")
    menu.geometry("300x300")

    tk.Label(menu, text=f"Welcome, {user[1]}", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(menu, text="Add Report", command=lambda: report_window(user), width=25).pack(pady=5)
    tk.Button(menu, text="View My Reports", command=lambda: view_reports_window(user), width=25).pack(pady=5)
    tk.Button(menu, text="Get Safe Route", command=open_safe_route_window, width=25).pack(pady=5)
    tk.Button(menu, text="High Risk Locations", command=open_danger_location_ui, width=25).pack(pady=5)
    tk.Button(menu, text="Logout", command=menu.destroy, width=25).pack(pady=10)
