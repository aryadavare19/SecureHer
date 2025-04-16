import tkinter as tk
from db import get_connection

def view_reports_window(user):
    conn = get_connection()
    cursor = conn.cursor()

    win = tk.Toplevel()
    win.update_idletasks()
    win.title("My Reports")
    win.geometry("500x600")

    tk.Label(win, text=f"Reports by {user[1]}", font=("Arial", 14, "bold")).pack(pady=10)

    # Offline
    tk.Label(win, text="Offline Reports", font=("Arial", 12, "underline")).pack()
    cursor.execute("SELECT category, description, location_id, time FROM offline_reports WHERE name = %s", (user[1],))
    offline_reports = cursor.fetchall()
    if offline_reports:
        for r in offline_reports:
            text = f"Category: {r[0]}\nDescription: {r[1]}\nLocation ID: {r[2]}\nTime: {r[3]}\n"
            tk.Label(win, text=text, justify="left", anchor="w").pack(padx=10, pady=5)
    else:
        tk.Label(win, text="No offline reports found.", fg="gray").pack(pady=5)

    # Online
    tk.Label(win, text="Online Reports", font=("Arial", 12, "underline")).pack(pady=(20, 0))
    cursor.execute("SELECT platform, url, description FROM online_reports WHERE user_id = %s", (user[0],))
    online_reports = cursor.fetchall()
    if online_reports:
        for r in online_reports:
            text = f"Platform: {r[0]}\nURL: {r[1]}\nDescription: {r[2]}\n"
            tk.Label(win, text=text, justify="left", anchor="w").pack(padx=10, pady=5)
    else:
        tk.Label(win, text="No online reports found.", fg="gray").pack(pady=5)

    conn.close()
