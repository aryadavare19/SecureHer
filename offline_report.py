import tkinter as tk
from tkinter import messagebox
from db_config import get_db_connection


def get_location_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM locations ORDER BY id")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results


def add_report_ui():
    def submit_report():
        name = name_entry.get()
        contact = contact_entry.get()
        category = category_entry.get()
        description = description_entry.get("1.0", "end-1c")
        location = location_var.get()

        if not name or not contact or not category or not description or not location:
            messagebox.showerror("Error", "Please fill out all fields")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get location_id from the location name
        cursor.execute("SELECT id FROM locations WHERE name = %s", (location,))
        location_id = cursor.fetchone()
        if not location_id:
            messagebox.showerror("Error", "Invalid location")
            conn.close()
            return

        location_id = location_id[0]

        # Insert the report into the offline_reports table
        cursor.execute("""
            INSERT INTO offline_reports (name, contact, category, description, location_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, contact, category, description, location_id))
        
        # Increment the danger score for this location
        cursor.execute("""
            UPDATE location_danger
            SET danger_score = danger_score + 1, last_reported = CURRENT_TIMESTAMP
            WHERE location_id = %s
        """, (location_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Offline report submitted successfully")
        report_window.destroy()

    # Create the report submission window
    report_window = tk.Toplevel()
    report_window.update_idletasks()
    report_window.title("Submit Offline Report")
    report_window.geometry("400x400")

    tk.Label(report_window, text="Name").pack(pady=5)
    name_entry = tk.Entry(report_window, width=40)
    name_entry.pack(pady=5)

    tk.Label(report_window, text="Contact").pack(pady=5)
    contact_entry = tk.Entry(report_window, width=40)
    contact_entry.pack(pady=5)

    tk.Label(report_window, text="Category").pack(pady=5)
    category_entry = tk.Entry(report_window, width=40)
    category_entry.pack(pady=5)

    tk.Label(report_window, text="Description").pack(pady=5)
    description_entry = tk.Text(report_window, width=40, height=5)
    description_entry.pack(pady=5)

    tk.Label(report_window, text="Location").pack(pady=5)
    location_var = tk.StringVar()
    location_dropdown = tk.OptionMenu(report_window, location_var, *get_location_names())
    location_dropdown.pack(pady=5)

    submit_button = tk.Button(report_window, text="Submit Report", command=submit_report)
    submit_button.pack(pady=20)

