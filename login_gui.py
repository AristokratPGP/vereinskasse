import tkinter as tk
from tkinter import messagebox
import subprocess  # Für das Starten der Admin-GUI
from login_backend import load_users
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
    users = load_users()

    print(f"Eingegebene Login-Daten: Benutzername={username}, Passwort={password}")

    if username in users and users[username].password == password:
        role = users[username].role
        messagebox.showinfo("Login Erfolgreich", f"Willkommen, {username}!\nRolle: {role}")
        root.destroy()  # Schließt das Login-Fenster

        print(f"Basisverzeichnis: {BASE_DIR}")  # Debugging
        if not os.path.exists(ADMIN_GUI_PATH):
            print(f"Fehler: Datei '{ADMIN_GUI_PATH}' wurde nicht gefunden.")
            return

        def start_gui(script_path):
            """Startet das jeweilige GUI-Skript mit der passenden Methode für Windows oder macOS/Linux"""
            if IS_WINDOWS:
                print(f"Starte {script_path} unter Windows...")
                subprocess.Popen([PYTHON_CMD, script_path], shell=True)  # Windows mit shell=True
            else:
                print(f"Starte {script_path} unter macOS/Linux...")
                subprocess.Popen([PYTHON_CMD, script_path])  # macOS/Linux ohne shell

        if role == "Administrator":
            print("Administrator-Login erkannt. Starte Admin-GUI...")
            start_gui(ADMIN_GUI_PATH)
        elif role == "Kassenwart":
            print("Kassenwart-Login erkannt. Starte Kassenwart-GUI...")
            start_gui(KASSENWART_GUI_PATH)
        elif role == "Referent-Finanzen":
            print("Referent-Finanzen-Login erkannt. Starte Finanzen-GUI...")
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
