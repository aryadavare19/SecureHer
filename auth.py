import tkinter as tk
from tkinter import messagebox
from db import get_connection
from session import current_user
import main_menu


def signup():
    def submit_signup():
        name = name_entry.get()
        contact = contact_entry.get()
        password = password_entry.get()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE contact=%s", (contact,))
        if cursor.fetchone():
            messagebox.showerror("Error", "User already exists.")
            return

        cursor.execute("INSERT INTO users (name, contact, password) VALUES (%s, %s, %s)", (name, contact, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Signup successful. Please login.")
        signup_window.destroy()

    signup_window = tk.Toplevel()
    signup_window.update_idletasks()
    signup_window.title("Signup")

    tk.Label(signup_window, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(signup_window)
    name_entry.grid(row=0, column=1)

    tk.Label(signup_window, text="Contact").grid(row=1, column=0)
    contact_entry = tk.Entry(signup_window)
    contact_entry.grid(row=1, column=1)

    tk.Label(signup_window, text="Password").grid(row=2, column=0)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.grid(row=2, column=1)

    tk.Button(signup_window, text="Submit", command=submit_signup).grid(row=3, column=1)

def login():
    # auth.py
    def submit_login():
        name = name_entry.get()
        password = password_entry.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, contact FROM users WHERE name=%s AND password=%s", (name, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            current_user[0] = user
            messagebox.showinfo("Success", f"Welcome {user[1]}!")
            login_window.destroy()
            
            # Now pass the user object to the main menu
            main_menu.open_main_menu(user)  # Pass the user object here

        else:
            messagebox.showerror("Error", "Invalid credentials.")


    login_window = tk.Toplevel()
    login_window.update_idletasks()
    login_window.title("Login")

    tk.Label(login_window, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(login_window)
    name_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=submit_login).grid(row=2, column=1)
