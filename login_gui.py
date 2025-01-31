__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import messagebox
import os
import sys
from user_manager import UserManager
from finanzen_gui import FinanzenDashboard
from kassenwart_gui import KassenwartDashboard
from admin_gui import AdminDashboard

# Check operating system
IS_WINDOWS = sys.platform.startswith("win")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory of the script


# Login-Funktion
def login():
    """
        Handles the login process and opens the appropriate GUI.
    """
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    manager = UserManager()
    users_dict = manager.load_users()  # Load users from JSON

    if not username or not password:
        messagebox.showerror("Fehler", "Benutzername und Passwort eingeben!")
        return

    print(f"[DEBUG] Benutzername eingeben: {username}")
    print(f"[DEBUG] Passwort eingeben: {password}")

    # Verify credentials
    if username in users_dict:
        print(f"[DEBUG] Gefundener Benutzer: {users_dict[username]}")  # Debugging output
        print(f"[DEBUG] Erwartetes Passwort: {users_dict[username].password}")

        if users_dict[username].password == password:
            role = users_dict[username].role
            konten = users_dict[username].accounts

            message = f"Willkommen, {username}!\nRolle: {role}"
            if konten:
                message += f"\nZugriff auf Konten: {', '.join(konten)}"

            messagebox.showinfo("Login Erfolgreich", message)

            # Hide the login window instead of destroying it
            root.withdraw()

            # Start correct GUI
            if role == "Administrator":
                open_admin_gui()
            elif role == "Treasurer":
                root.withdraw()
                open_kassenwart_gui(username)
            elif role == "Finance-Referent":
                open_finanzen_gui()
        else:
            print("[DEBUG] Passwort stimmt nicht überein!")  # Debugging
            messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")
    else:
        print("[DEBUG] Benutzer nicht gefunden!")  # Debugging
        messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")

def open_admin_gui():
    """Opens the administrator GUI with the correct AdminDashboard."""
    root.withdraw()  # Hides the login window
    admin_window = tk.Toplevel(root)  # New window for the admin dashboard
    AdminDashboard(admin_window)

def open_kassenwart_gui(username):
    """Opens the cashier GUI with the correct dashboard."""
    kassenwart_window = tk.Toplevel(root)  # new window
    KassenwartDashboard(kassenwart_window, username)

def open_finanzen_gui():
    """Opens the Finance GUI in a new window and passes the `root` instance."""
    finanzen_window = tk.Toplevel(root)
    finanzen_window.title("Vereinskassen-System - Finanzen Dashboard")
    FinanzenDashboard(finanzen_window, root)

def go_back_to_login(window):
    """Closes an open window and displays the login window again."""
    window.destroy()
    root.deiconify()

# Create GUI
root = tk.Tk()
root.title("Login - Vereinskassen-System")
root.geometry("300x200")

tk.Label(root, text="Benutzername:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Passwort:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()