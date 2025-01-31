__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import json
from user_manager import UserManager

# Betriebssystem prüfen
IS_WINDOWS = sys.platform.startswith("win")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Basisverzeichnis des Skripts
ADMIN_GUI_PATH = os.path.join(BASE_DIR, "admin_gui.py")
KASSENWART_GUI_PATH = os.path.join(BASE_DIR, "kassenwart_gui.py")
FINANZEN_GUI_PATH = os.path.join(BASE_DIR, "finanzen_gui.py")


# Login-Funktion
def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    manager = UserManager()
    users_dict = manager.load_users()  # Lade die Benutzer aus JSON

    if not username or not password:
        messagebox.showerror("Fehler", "Benutzername und Passwort eingeben!")
        return


   

    print(f"[DEBUG] Benutzername eingeben: {username}")
    print(f"[DEBUG] Passwort eingeben: {password}")

    # Prüfen, ob Benutzer existiert und Passwort übereinstimmt
    if username in users_dict:
        print(f"[DEBUG] Gefundener Benutzer: {users_dict[username]}")  # Debugging-Ausgabe
        print(f"[DEBUG] Erwartetes Passwort: {users_dict[username].password}")  # Erwartetes Passwort aus JSON

        if users_dict[username].password == password:
            role = users_dict[username].role
            konten = users_dict[username].accounts

            message = f"Willkommen, {username}!\nRolle: {role}"
            if konten:
                message += f"\nZugriff auf Konten: {', '.join(konten)}"

            messagebox.showinfo("Login Erfolgreich", message)
            root.destroy()  # Schließt das Login-Fenster

            def start_gui(script_path):
                """Startet das jeweilige GUI-Skript"""
                if IS_WINDOWS:
                    subprocess.Popen(["python", script_path], shell=True)
                else:
                    subprocess.Popen(["python3", script_path])

            # Richtige GUI starten
            if role == "Administrator":
                start_gui(ADMIN_GUI_PATH)
            elif role == "Kassenwart":
                start_gui(KASSENWART_GUI_PATH)
            elif role == "Referent-Finanzen":
                start_gui(FINANZEN_GUI_PATH)
        else:
            print("[DEBUG] Passwort stimmt nicht überein!")  # Debugging
            messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")
    else:
        print("[DEBUG] Benutzer nicht gefunden!")  # Debugging
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