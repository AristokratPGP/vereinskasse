import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class KassenwartDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Kassenwart Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Kassenwart Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Einzahlung tätigen", command=self.deposit_money).pack(pady=0,fill="x")
        tk.Button(self.root, text="Auszahlung tätigen", command=self.withdraw_money).pack(pady=0,fill="x")
        tk.Button(self.root, text="Umbuchung zwischen Konten", command=self.transfer_money).pack(pady=0,fill="x")
        tk.Button(self.root, text="Transaktionshistorie anzeigen", command=self.show_transactions).pack(pady=0,fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)


    def deposit_money(self):
        messagebox.showinfo("Einzahlung", "Funktion für Einzahlung wird implementiert")

    def withdraw_money(self):
        messagebox.showinfo("Auszahlung", "Funktion für Auszahlung wird implementiert")

    def transfer_money(self):
        messagebox.showinfo("Umbuchung", "Funktion für Umbuchung wird implementiert")

    def show_transactions(self):
        messagebox.showinfo("Transaktionshistorie", "Funktion zur Anzeige der Transaktionshistorie")

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
    app = KassenwartDashboard(root)
    root.mainloop()