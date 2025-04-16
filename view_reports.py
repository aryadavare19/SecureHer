import tkinter as tk
from db import get_connection

def view_reports_window(user):
    user_id, name, contact = user  # Extract user info
    conn = get_connection()
    cursor = conn.cursor()

    win = tk.Toplevel()
    win.update_idletasks()
    win.title("My Reports")
    win.geometry("600x600")

    tk.Label(win, text=f"Reports by {name}", font=("Arial", 14, "bold")).pack(pady=10)

    # ===== Offline Reports =====
    tk.Label(win, text="Offline Reports", font=("Arial", 12, "underline")).pack()
    cursor.execute("""
        SELECT o.category, o.description, l.name AS location_name, o.time
        FROM offline_reports o
        JOIN locations l ON o.location_id = l.id
        WHERE o.user_id = %s
        ORDER BY o.time DESC
    """, (user_id,))
    offline_reports = cursor.fetchall()

    if offline_reports:
        for report in offline_reports:
            text = f"Category: {report[0]}\nDescription: {report[1]}\nLocation: {report[2]}\nTime: {report[3]}\n"
            tk.Label(win, text=text, justify="left", anchor="w", wraplength=550).pack(padx=10, pady=5)
    else:
        tk.Label(win, text="No offline reports found.", fg="gray").pack(pady=5)

    # ===== Online Reports =====
    tk.Label(win, text="Online Reports", font=("Arial", 12, "underline")).pack(pady=(20, 0))
    cursor.execute("""
        SELECT platform, url, description, time
        FROM online_reports
        WHERE user_id = %s
        ORDER BY time DESC
    """, (user_id,))
    online_reports = cursor.fetchall()

    if online_reports:
        for report in online_reports:
            text = f"Platform: {report[0]}\nURL: {report[1]}\nDescription: {report[2]}\nTime: {report[3]}\n"
            tk.Label(win, text=text, justify="left", anchor="w", wraplength=550).pack(padx=10, pady=5)
    else:
        tk.Label(win, text="No online reports found.", fg="gray").pack(pady=5)

    conn.close()
