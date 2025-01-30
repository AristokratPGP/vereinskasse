import tkinter as tk
from tkinter import messagebox


class FinanzenDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Finanzen Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Finanzen Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="Status eines Vereinskontos anzeigen", command=self.view_account_status).pack(pady=5)
        tk.Button(self.root, text="Transaktionshistorie eines Vereinskontos", command=self.view_transactions).pack(
            pady=5)
        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=20)

    def view_account_status(self):
        messagebox.showinfo("Konto-Status", "Funktion zur Anzeige des Konto-Status wird implementiert")

    def view_transactions(self):
        messagebox.showinfo("Transaktionshistorie", "Funktion zur Anzeige der Transaktionshistorie wird implementiert")

    def view_overview(self):
        messagebox.showinfo("Gesamtübersicht", "Funktion zur Anzeige der Gesamtübersicht wird implementiert")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanzenDashboard(root)
    root.mainloop()