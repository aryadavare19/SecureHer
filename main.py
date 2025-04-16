import tkinter as tk
from auth import signup, login

def main():
    root = tk.Tk()
    root.title("SecureHer - Women Safety App")
    root.geometry("300x200")

    tk.Button(root, text="Signup", command=signup).pack(pady=10)
    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
