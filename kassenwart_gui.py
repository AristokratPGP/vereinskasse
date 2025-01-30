import tkinter as tk
from tkinter import messagebox


class KassenwartDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Kassenwart Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Kassenwart Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="Einzahlung tätigen", command=self.deposit_money).pack(pady=5)
        tk.Button(self.root, text="Auszahlung tätigen", command=self.withdraw_money).pack(pady=5)
        tk.Button(self.root, text="Umbuchung zwischen Konten", command=self.transfer_money).pack(pady=5)
        tk.Button(self.root, text="Transaktionshistorie anzeigen", command=self.show_transactions).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=20)

    def deposit_money(self):
        messagebox.showinfo("Einzahlung", "Funktion für Einzahlung wird implementiert")

    def withdraw_money(self):
        messagebox.showinfo("Auszahlung", "Funktion für Auszahlung wird implementiert")

    def transfer_money(self):
        messagebox.showinfo("Umbuchung", "Funktion für Umbuchung wird implementiert")

    def show_transactions(self):
        messagebox.showinfo("Transaktionshistorie", "Funktion zur Anzeige der Transaktionshistorie")


if __name__ == "__main__":
    root = tk.Tk()
    app = KassenwartDashboard(root)
    root.mainloop()