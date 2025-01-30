import tkinter as tk
from tkinter import messagebox
import subprocess  # Für das Starten der Admin-GUI
from user_manager import UserManager
import os
import sys

# Betriebssystem prüfen
IS_WINDOWS = sys.platform.startswith("win")  # True, wenn Windows

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Basisverzeichnis des Skripts
ADMIN_GUI_PATH = os.path.join(BASE_DIR, "admin_gui.py")
KASSENWART_GUI_PATH = os.path.join(BASE_DIR, "kassenwart_gui.py")
FINANZEN_GUI_PATH = os.path.join(BASE_DIR, "finanzen_gui.py")

# Wähle den richtigen Python-Befehl
PYTHON_CMD = "python" if IS_WINDOWS else "python3"

# Login-Funktion
def login():
    username = entry_username.get()
    password = entry_password.get()
    manager = UserManager() 
    users = manager.load_users()

    # Benutzer in der JSON-Struktur suchen
    role, bereich = None, None
    user_found = None

    for r, user_list in users.items():
        if r == "Kassenwart":  # Kassenwarte haben eine weitere Hierarchie
            for b, kassenwarte in user_list.items():
                for user in kassenwarte:
                    if user["Benutzername"] == username and user["Passwort"] == password:
                        role, bereich, user_found = r, b, user
                        break
        else:  # Für Administratoren und Referent-Finanzen
            for user in user_list:
                if user["Benutzername"] == username and user["Passwort"] == password:
                    role, user_found = r, user
                    break

    if user_found:
        message = f"Willkommen, {username}!\nRolle: {role}"
        if bereich:
            message += f"\nBereich: {bereich}"  # Bereich anzeigen, falls Kassenwart

        messagebox.showinfo("Login Erfolgreich", message)
        root.destroy()  # Schließt das Login-Fenster

        def start_gui(script_path):
            """Startet das jeweilige GUI-Skript mit der passenden Methode für Windows oder macOS/Linux"""
            if IS_WINDOWS:
                subprocess.Popen([PYTHON_CMD, script_path], shell=True)  # Windows mit shell=True
            else:
                subprocess.Popen([PYTHON_CMD, script_path])  # macOS/Linux ohne shell

        if role == "Administrator":
            start_gui(ADMIN_GUI_PATH)
        elif role == "Kassenwart":
            start_gui(KASSENWART_GUI_PATH)
        elif role == "Referent-Finanzen":
            start_gui(FINANZEN_GUI_PATH)
    else:
        messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")

# GUI erstellen
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
