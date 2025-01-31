import tkinter as tk
from tkinter import messagebox
import os
import sys
from user_manager import UserManager
from finanzen_gui import FinanzenDashboard
from kassenwart_gui import KassenwartDashboard

# Betriebssystem prüfen
IS_WINDOWS = sys.platform.startswith("win")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Basisverzeichnis des Skripts


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

            # Verstecke das Login-Fenster anstatt es zu zerstören
            root.withdraw()

            # Richtige GUI starten
            if role == "Administrator":
                open_admin_gui()
            elif role == "Kassenwart":
                root.withdraw()  # Versteckt das Login-Fenster
                open_kassenwart_gui(username)
            elif role == "Referent-Finanzen":
                open_finanzen_gui()
        else:
            print("[DEBUG] Passwort stimmt nicht überein!")  # Debugging
            messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")
    else:
        print("[DEBUG] Benutzer nicht gefunden!")  # Debugging
        messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")

def open_admin_gui():
    """Öffnet die Administrator-GUI in einem neuen Fenster."""
    admin_window = tk.Toplevel(root)
    admin_window.title("Administrator - Vereinskassen-System")
    tk.Label(admin_window, text="Willkommen in der Admin-GUI!", font=("Arial", 14)).pack(pady=20)
    tk.Button(admin_window, text="Zurück", command=lambda: go_back_to_login(admin_window)).pack(pady=20)

def open_kassenwart_gui(username):
    """Öffnet die Kassenwart-GUI mit dem richtigen Dashboard."""
    kassenwart_window = tk.Toplevel(root)  # Neues Fenster
    KassenwartDashboard(kassenwart_window, username)

def open_finanzen_gui():
    """Öffnet die Finanz-GUI in einem neuen Fenster und übergibt die `root`-Instanz."""
    finanzen_window = tk.Toplevel(root)
    finanzen_window.title("Vereinskassen-System - Finanzen Dashboard")
    FinanzenDashboard(finanzen_window, root)  # `root` als Argument übergeben

def go_back_to_login(window):
    """Schließt ein geöffnetes Fenster und zeigt das Login-Fenster wieder an."""
    window.destroy()
    root.deiconify()

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