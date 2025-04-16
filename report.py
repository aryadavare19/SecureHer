# report.py

import tkinter as tk
from tkinter import messagebox
from db import get_connection

def report_window(user):
    window = tk.Toplevel()
    window.title("Choose Report Type")
    window.geometry("300x200")

    tk.Label(window, text="Select Report Type", font=("Helvetica", 12)).pack(pady=20)
    tk.Button(window, text="Offline Report", width=20, command=lambda: open_offline_report(user)).pack(pady=5)
    tk.Button(window, text="Online Report", width=20, command=lambda: open_online_report(user)).pack(pady=5)

def open_offline_report(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM locations ORDER BY id")
    locations = [row[0] for row in cursor.fetchall()]
    conn.close()

    win = tk.Toplevel()
    win.title("Offline Report")
    win.geometry("400x400")

    tk.Label(win, text="Category").pack()
    category_entry = tk.Entry(win)
    category_entry.pack()

    tk.Label(win, text="Description").pack()
    description_entry = tk.Text(win, height=5)
    description_entry.pack()

    tk.Label(win, text="Location").pack()
    location_var = tk.StringVar()
    if locations:
        location_var.set(locations[0])
    tk.OptionMenu(win, location_var, *locations).pack()

    def submit():
        category = category_entry.get()
        description = description_entry.get("1.0", "end-1c")
        location_name = location_var.get()

        if not category or not description or not location_name:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM locations WHERE name = %s", (location_name,))
        loc = cursor.fetchone()
        if not loc:
            messagebox.showerror("Error", "Invalid location.")
            return
        location_id = loc[0]

        cursor.execute("""
            INSERT INTO offline_reports (user_id, name, contact, category, description, location_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user[0], user[1], user[2], category, description, location_id))

        cursor.execute("""
            INSERT INTO location_danger (location_id, danger_score)
            VALUES (%s, 2)
            ON DUPLICATE KEY UPDATE danger_score = danger_score + 1, last_reported = CURRENT_TIMESTAMP
        """, (location_id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Offline report submitted.")
        

    tk.Button(win, text="Submit", command=submit).pack(pady=10)

def open_online_report(user):
    win = tk.Toplevel()
    win.title("Online Report")
    win.geometry("400x350")

    tk.Label(win, text="Platform").pack()
    platform_entry = tk.Entry(win)
    platform_entry.pack()

    tk.Label(win, text="URL").pack()
    url_entry = tk.Entry(win)
    url_entry.pack()

    tk.Label(win, text="Screenshot Link").pack()
    screenshot_entry = tk.Entry(win)
    screenshot_entry.pack()

    tk.Label(win, text="Description").pack()
    description_entry = tk.Entry(win)
    description_entry.pack()

    def submit():
        platform = platform_entry.get()
        url = url_entry.get()
        screenshot = screenshot_entry.get()
        description = description_entry.get()

        if not platform or not url or not description:
            messagebox.showwarning("Missing Fields", "Please fill out all required fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO online_reports (user_id, name, contact, description, platform, url, screenshot)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user[0], user[1], user[2], description, platform, url, screenshot))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Online report submitted.")
        

    tk.Button(win, text="Submit", command=submit).pack(pady=20)
