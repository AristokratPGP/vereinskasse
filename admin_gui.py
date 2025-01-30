import tkinter as tk
from tkinter import messagebox


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Admin Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="Neues Vereinskonto anlegen", command=self.create_account).pack(pady=5)
        tk.Button(self.root, text="Benutzer verwalten", command=self.manage_users).pack(pady=5)
        tk.Button(self.root, text="CSV-Daten exportieren", command=self.export_data).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=20)

    def create_account(self):
        messagebox.showinfo("Konto erstellen", "Funktion zum Erstellen eines Vereinskontos")

    def manage_users(self):
        messagebox.showinfo("Benutzerverwaltung", "Funktion zur Verwaltung von Benutzern")

    def export_data(self):
        messagebox.showinfo("Daten exportieren", "Funktion zum Exportieren der Daten als CSV")


# ✅ Stellt sicher, dass `admin_gui.py` nur startet, wenn es direkt ausgeführt wird
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()