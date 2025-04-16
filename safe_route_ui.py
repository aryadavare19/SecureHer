# safe_route_ui.py
import tkinter as tk
from tkinter import messagebox
from db import get_connection
from safe_route import get_safe_route

def fetch_location_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM locations ORDER BY id")
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return names

def open_safe_route_window():
    locations = fetch_location_names()
    if not locations or len(locations) < 2:
        messagebox.showerror("Error", "Not enough locations in the database.")
        return

    route_window = tk.Toplevel()
    route_window.title("Safe Route Finder")
    route_window.geometry("400x300")

    tk.Label(route_window, text="Start Location").pack(pady=5)
    start_var = tk.StringVar()
    start_var.set(locations[0])
    tk.OptionMenu(route_window, start_var, *locations).pack()

    tk.Label(route_window, text="Destination").pack(pady=5)
    dest_var = tk.StringVar()
    dest_var.set(locations[1])
    tk.OptionMenu(route_window, dest_var, *locations).pack()

    def find_route():
        start = start_var.get()
        dest = dest_var.get()
        if start == dest:
            messagebox.showwarning("Invalid", "Start and destination cannot be the same.")
            return
        try:
            get_safe_route(start, dest)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    tk.Button(route_window, text="Get Safe Route", command=find_route).pack(pady=20)
