import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from db_config import get_db_connection
from safe_route import get_safe_route
from location_danger_history import get_location_history_text

def get_locations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM locations ORDER BY id")
    locations = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return locations

def submit_offline_report(name, contact, category, description, location_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM locations WHERE name = %s", (location_name,))
    location = cursor.fetchone()
    if not location:
        messagebox.showerror("Error", "Invalid location selected.")
        return
    location_id = location[0]

    cursor.execute("""
        INSERT INTO offline_reports (name, contact, category, description, location_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, contact, category, description, location_id))

    cursor.execute("""
        INSERT INTO location_danger (location_id, danger_score)
        VALUES (%s, 2)
        ON DUPLICATE KEY UPDATE danger_score = danger_score + 1, last_reported = CURRENT_TIMESTAMP
    """, (location_id,))

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Report submitted successfully!")

def open_report_form():
    report_win = tk.Toplevel(root)
    report_win.title("Submit Offline Report")
    report_win.geometry("400x400")

    tk.Label(report_win, text="Name").pack()
    name_entry = tk.Entry(report_win)
    name_entry.pack()

    tk.Label(report_win, text="Contact").pack()
    contact_entry = tk.Entry(report_win)
    contact_entry.pack()

    tk.Label(report_win, text="Category").pack()
    category_entry = tk.Entry(report_win)
    category_entry.pack()

    tk.Label(report_win, text="Description").pack()
    description_entry = tk.Text(report_win, height=5)
    description_entry.pack()

    tk.Label(report_win, text="Select Location").pack()
    location_var = tk.StringVar()
    location_choices = get_locations()
    location_var.set(location_choices[0])
    tk.OptionMenu(report_win, location_var, *location_choices).pack()

    def submit():
        submit_offline_report(
            name_entry.get(),
            contact_entry.get(),
            category_entry.get(),
            description_entry.get("1.0", tk.END),
            location_var.get()
        )
        report_win.destroy()

    tk.Button(report_win, text="Submit Report", command=submit).pack(pady=10)

def view_location_history():
    history_text = get_location_history_text()
    history_window = tk.Toplevel(root)
    history_window.title("Location History")
    text_area = scrolledtext.ScrolledText(history_window, width=80, height=20)
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, history_text)
    text_area.config(state=tk.DISABLED)

def get_safe_route_ui():
    route_win = tk.Toplevel(root)
    route_win.title("Get Safe Route")
    route_win.geometry("400x250")

    tk.Label(route_win, text="Select Start Location").pack(pady=5)
    start_var = tk.StringVar()
    location_choices = get_locations()
    start_var.set(location_choices[0])
    tk.OptionMenu(route_win, start_var, *location_choices).pack()

    tk.Label(route_win, text="Select Destination").pack(pady=5)
    dest_var = tk.StringVar()
    dest_var.set(location_choices[1])
    tk.OptionMenu(route_win, dest_var, *location_choices).pack()

    def compute_route():
        start = start_var.get()
        dest = dest_var.get()
        if start == dest:
            messagebox.showwarning("Invalid Input", "Start and Destination cannot be the same.")
            return
        try:
            get_safe_route(start, dest)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        route_win.destroy()

    tk.Button(route_win, text="Find Safe Route", command=compute_route).pack(pady=15)

root = tk.Tk()
root.title("Safe Route and Location History System")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

tk.Button(frame, text="Submit Offline Report", command=open_report_form, width=30).pack(pady=5)
tk.Button(frame, text="View Location History", command=view_location_history, width=30).pack(pady=5)
tk.Button(frame, text="Get Safe Route Guidance", command=get_safe_route_ui, width=30).pack(pady=5)
tk.Button(frame, text="Exit", command=root.quit, width=30).pack(pady=5)

root.mainloop()
