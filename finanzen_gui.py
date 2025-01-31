__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import accounts_manager

class FinanzenDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vereinskassen-System - Finanzen Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Finanzen Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=0, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)

    def view_overview(self):
        """Zeigt eine Übersicht aller existierenden Konten mit Namen und Saldo an."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Löscht die alten Widgets, um die Übersicht anzuzeigen

        tk.Label(self.root, text="Kontenübersicht", font=("Arial", 14, "bold")).pack(pady=10)

        manager = accounts_manager.AccountManager()  # Instanz der AccountManager-Klasse erstellen
        accounts_data = manager.get_all_accounts_summary()  # Holt alle Konten

        # Überprüfen, ob ein Fehler aufgetreten ist (z. B. keine Konten vorhanden)
        if "error" in accounts_data:
            tk.Label(self.root, text="Keine Konten vorhanden.", fg="red").pack(pady=5)
            tk.Button(self.root, text="Zurück", command=self.__init__).pack(pady=10)
            return

        # Durch alle Konten iterieren und Buttons erstellen
        for account in accounts_data["accounts"]:
            account_name = account.split(":")[0].strip()  # Nur den Kontonamen extrahieren (z. B. "Tanzen")
            btn = tk.Button(
                self.root,
                text=account,  # Der Button zeigt den Kontonamen und Saldo an (z. B. "Tanzen: 500€")
                command=lambda acc=account_name: self.view_account_history(acc)  # Aufruf der Methode mit Konto
            )
            btn.pack(pady=2, fill="x")

        # Gesamtsumme aller Konten anzeigen
        tk.Label(self.root, text=f"Gesamtsumme aller Konten: {accounts_data['total_balance']}€",
                 font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(self.root, text="Zurück", command=self.__init__).pack(pady=10)

    def view_account_history(self, account_name):
        """Zeigt die Transaktionshistorie für ein spezifisches Konto."""
        # Neues Fenster für die Historie erstellen
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Historie für {account_name}")
        history_window.geometry("500x400")

        tk.Label(history_window, text=f"Historie: {account_name}", font=("Arial", 14, "bold")).pack(pady=10)

        # Kontodaten laden
        manager = accounts_manager.AccountManager()
        transactions = manager.get_transaction_history(account_name)  # Transaktionen abrufen

        if "error" in transactions:
            tk.Label(history_window, text=transactions["error"], fg="red", font=("Arial", 12)).pack(pady=10)
        elif not transactions:
            tk.Label(history_window, text="Keine Transaktionen vorhanden.", fg="red", font=("Arial", 12)).pack(pady=10)
        else:
            # Scrollable Frame für die Transaktionsliste
            canvas = tk.Canvas(history_window)
            scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            # Verbinde Scrollbar mit Canvas
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Transaktionen anzeigen
            for transaction in transactions:
                # Frame für jede Transaktion
                trans_frame = tk.Frame(scrollable_frame, bg="#f9f9f9", bd=1, relief="solid", padx=10, pady=5)
                trans_frame.pack(fill="x", pady=5)

                # Transaktionsdetails
                tk.Label(trans_frame, text=f"Datum: {transaction['datum']}", anchor="w", bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"Typ: {transaction['typ']}, Betrag: {transaction['betrag']}€", anchor="w",
                         bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"Quelle: {transaction['quelle']}", anchor="w", bg="#f9f9f9").pack(
                    anchor="w")
                if transaction['notiz']:
                    tk.Label(trans_frame, text=f"Notiz: {transaction['notiz']}", anchor="w", bg="#f9f9f9").pack(
                        anchor="w")

        # Zurück-Button
        tk.Button(history_window, text="Schließen", command=history_window.destroy).pack(pady=10)

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