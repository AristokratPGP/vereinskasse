import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys


class FinanzenDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Finanzen Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Finanzen Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Status eines Vereinskontos anzeigen", command=self.view_account_status).pack(pady=0, fill="x")
        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=0, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)


    def view_account_status(self):
        self.user_window = tk.Toplevel(self.root)
        self.user_window.title("status einzelner Accounts")
        self.user_window.geometry("500x400")

        # Titel des Fensters
        tk.Label(self.user_window, text="Benutzerverwaltung", font=("Arial", 12, "bold")).pack(pady=10)

        # **Frame für den dynamischen Inhalt**
        self.content_frame = tk.Frame(self.user_window)
        self.content_frame.pack(pady=10, fill="both", expand=True)

        # Buttons zur Navigation
        tk.Button(self.user_window, text="Bestehende Benutzer ansehen", command=lambda: self.show_user()).pack(pady=0,
                                                                                                               fill="x")
        tk.Button(self.user_window, text="Benutzer hinzufügen", command=lambda: self.add_user()).pack(pady=20, fill="x")

    def view_overview(self):
        messagebox.showinfo("Gesamtübersicht", "Funktion zur Anzeige der Gesamtübersicht wird implementiert")

    def clear_frame(self):
        """Löscht alle Widgets im content_frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanzenDashboard(root)
    root.mainloop()