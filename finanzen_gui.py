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
        tk.Button(self.root, text="Transaktionshistorie eines Vereinskontos", command=self.view_transactions).pack(pady=0,fill="x")
        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=0, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)


    def view_account_status(self):
        messagebox.showinfo("Konto-Status", "Funktion zur Anzeige des Konto-Status wird implementiert")

    def view_transactions(self):
        messagebox.showinfo("Transaktionshistorie", "Funktion zur Anzeige der Transaktionshistorie wird implementiert")

    def view_overview(self):
        messagebox.showinfo("Gesamtübersicht", "Funktion zur Anzeige der Gesamtübersicht wird implementiert")

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