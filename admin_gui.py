__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Admin Dashboard")
        self.root.geometry("400x400")

        self.users = {}

        self.accounts = {}

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Konten verwalten", command=self.manage_account).pack(pady=0,fill="x")
        tk.Button(self.root, text="Benutzer verwalten", command=self.manage_users).pack(pady=0,fill="x")
        tk.Button(self.root, text="CSV-Daten exportieren", command=self.export_data).pack(pady=0,fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)

    def manage_account(self):
        self.user_window = tk.Toplevel(self.root)
        self.user_window.title("Konten verwalten")
        self.user_window.geometry("500x400")

        tk.Label(self.user_window, text="Konten verwalten", font=("Arial", 12, "bold")).pack(pady=10)

        self.content_frame = tk.Frame(self.user_window)
        self.content_frame.pack(pady=10, fill="both", expand=True)

        tk.Button(self.user_window, text="Bestehende Vereinskonto ansehen", command=lambda: self.show_user()).pack(pady=0, fill="x")
        tk.Button(self.user_window, text="Vereinskonto hinzufügen", command=lambda: self.add_user()).pack(pady=20, fill="x")

    def add_account(self):
        self.clear_frame()  # Löscht alten Inhalt

        tk.Label(self.content_frame, text="Vereinskonto hinzufügen", font=("Arial", 10)).pack(pady=5)

        tk.Label(self.content_frame, text="Kontoname:").pack()
        entry_name = tk.Entry(self.content_frame)
        entry_name.pack(pady=5)

        tk.Label(self.content_frame, text="Start Saldo").pack()
        entry_start_saldo = tk.Entry(self.content_frame)
        entry_start_saldo.pack(pady=5)

        tk.Label(self.content_frame, text="berechtigung: (1/2/3)").pack()
        entry_user_type = tk.Entry(self.content_frame)
        entry_user_type.pack(pady=5)

        tk.Button(self.content_frame, text="Speichern",
                  command=lambda: self.save_account(entry_name, entry_start_saldo)
                  ).pack(pady=10)

    def save_account(self, name_entry, start_saldo_entry):
        """Speichert einen neuen Benutzer in die Dummy-Dictionary"""
        name = name_entry.get()
        start_saldo = start_saldo_entry.get()


        if not name or not start_saldo:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt sein!")
            return

        # Benutzer zur Dictionary hinzufügen
        if name in self.users:
            messagebox.showerror("Fehler", "Benutzername existiert bereits!")
        else:
            self.accounts[name] = {"start saldo": start_saldo}
            messagebox.showinfo("Erfolg", f"Vereinskonto für '{name}' wurde hinzugefügt!")
            self.show_user()

    def show_account(self):
        self.clear_frame()  # Löscht alten Inhalt

        tk.Label(self.content_frame, text="Liste der accounts:", font=("Arial", 10)).pack(pady=5)
        # Beispielhafte Benutzerliste
        if not self.users:
            tk.Label(self.content_frame, text="Keine Benutzer vorhanden").pack()
        else:
            for username, details in self.users.items():
                # Erstelle einen Text mit den Details des Benutzers
                user_info = f"Benutzername: {username}, Rolle: {details['role']}"
                tk.Label(self.content_frame, text=user_info).pack()

    def manage_users(self):
        """Öffnet ein Fenster zur Benutzerverwaltung mit dynamischem Inhalt"""
        self.user_window = tk.Toplevel(self.root)
        self.user_window.title("Benutzer verwalten")
        self.user_window.geometry("500x400")

        # Titel des Fensters
        tk.Label(self.user_window, text="Benutzerverwaltung", font=("Arial", 12, "bold")).pack(pady=10)

        # **Frame für den dynamischen Inhalt**
        self.content_frame = tk.Frame(self.user_window)
        self.content_frame.pack(pady=10, fill="both", expand=True)

        # Buttons zur Navigation
        tk.Button(self.user_window, text="Bestehende Benutzer ansehen", command=lambda: self.show_user()).pack(pady=0, fill="x")
        tk.Button(self.user_window, text="Benutzer hinzufügen", command=lambda: self.add_user()).pack(pady=20, fill="x")


    def clear_frame(self):
        """Löscht alle Widgets im content_frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_user(self):
        self.clear_frame()  # Löscht alten Inhalt

        tk.Label(self.content_frame, text="Liste der Benutzer:", font=("Arial", 10)).pack(pady=5)
        # Beispielhafte Benutzerliste
        if not self.users:
            tk.Label(self.content_frame, text="Keine Benutzer vorhanden").pack()
        else:
            for username, details in self.users.items():
                # Erstelle einen Text mit den Details des Benutzers
                user_info = f"Benutzername: {username}, Rolle: {details['role']}"
                tk.Label(self.content_frame, text=user_info).pack()

    def add_user(self):
        self.clear_frame()  # Löscht alten Inhalt

        tk.Label(self.content_frame, text="Neuen Benutzer hinzufügen:", font=("Arial", 10)).pack(pady=5)

        tk.Label(self.content_frame, text="Benutzername:").pack()
        entry_name = tk.Entry(self.content_frame)
        entry_name.pack(pady=5)

        tk.Label(self.content_frame, text="Passwort:").pack()
        entry_password = tk.Entry(self.content_frame)
        entry_password.pack(pady=5)

        tk.Label(self.content_frame, text="berechtigung: (1/2/3)").pack()
        entry_user_type = tk.Entry(self.content_frame)
        entry_user_type.pack(pady=5)

        tk.Button(self.content_frame, text="Speichern",
                  command=lambda: self.save_user(entry_name, entry_password, entry_user_type)
                  ).pack(pady=10)

    def save_user(self, username_entry, password_entry, role_entry):
        """Speichert einen neuen Benutzer in die Dummy-Dictionary"""
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt sein!")
            return

        # Benutzer zur Dictionary hinzufügen
        if username in self.users:
            messagebox.showerror("Fehler", "Benutzername existiert bereits!")
        else:
            self.users[username] = {"password": password, "role": role}
            messagebox.showinfo("Erfolg", f"Benutzer '{username}' wurde hinzugefügt!")
            self.show_user()

    def export_data(self):
        messagebox.showinfo("Daten exportieren", "Funktion zum Exportieren der Daten als CSV")

    def logout(self):
        """Schließt das Fenster und öffnet die Login-GUI."""
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()  # Schließt das aktuelle Fenster

            # Betriebssystem prüfen
            IS_WINDOWS = sys.platform.startswith("win")
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            LOGIN_GUI_PATH = os.path.join(BASE_DIR, "login_gui.py")
            PYTHON_CMD = "python" if IS_WINDOWS else "python3"

            # Login GUI neu starten
            if IS_WINDOWS:
                subprocess.Popen([PYTHON_CMD, LOGIN_GUI_PATH], shell=True)
            else:
                subprocess.Popen([PYTHON_CMD, LOGIN_GUI_PATH])


# ✅ Stellt sicher, dass `admin_gui.py` nur startet, wenn es direkt ausgeführt wird
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()