import tkinter as tk
from tkinter import messagebox
from db import get_connection
from datetime import datetime

def report_window(user):
    def submit():
        mode = mode_var.get()
        description = description_entry.get()
        platform = platform_entry.get() if mode == "Online" else ""
        url = url_entry.get() if mode == "Online" else ""
        screenshot = screenshot_entry.get() if mode == "Online" else ""
        category = category_entry.get() if mode == "Offline" else ""
        location = location_entry.get()

        conn = get_connection()
        cursor = conn.cursor()

        if mode == "Online":
            cursor.execute("""
                INSERT INTO online_reports (user_id, name, contact, description, platform, url, screenshot)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user[0], user[1], user[2], description, platform, url, screenshot))
        else:
            cursor.execute("""
                INSERT INTO offline_reports (name, contact, category, description, location_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (user[1], user[2], category, description, location))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Report submitted successfully!")
        win.destroy()

    win = tk.Toplevel()
    win.update_idletasks()
    win.title("Report Incident")
    win.geometry("400x400")

    mode_var = tk.StringVar(value="Online")
    tk.Label(win, text="Report Mode").pack()
    tk.Radiobutton(win, text="Online", variable=mode_var, value="Online").pack()
    tk.Radiobutton(win, text="Offline", variable=mode_var, value="Offline").pack()

    tk.Label(win, text="Description").pack()
    description_entry = tk.Entry(win)
    description_entry.pack()

    tk.Label(win, text="Location ID").pack()
    location_entry = tk.Entry(win)
    location_entry.pack()

    tk.Label(win, text="Platform (for Online)").pack()
    platform_entry = tk.Entry(win)
    platform_entry.pack()

    tk.Label(win, text="URL (for Online)").pack()
    url_entry = tk.Entry(win)
    url_entry.pack()

    tk.Label(win, text="Screenshot (for Online)").pack()
    screenshot_entry = tk.Entry(win)
    screenshot_entry.pack()

    tk.Label(win, text="Category (for Offline)").pack()
    category_entry = tk.Entry(win)
    category_entry.pack()

    tk.Button(win, text="Submit", command=submit).pack()
