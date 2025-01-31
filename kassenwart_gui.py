__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import subprocess
import os
import sys
from user_manager import UserManager
from accounts_manager import AccountManager

class KassenwartDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.user_manager = UserManager()
        self.account_manager = AccountManager()

        # Lade die erlaubten Konten für den Benutzer
        self.allowed_accounts = self.user_manager.get_kassenwart_accounts(username).get("accounts", [])
        print(f"[DEBUG] Erlaubte Konten für {username}: {self.allowed_accounts}")

        self.root.title(f"Kassenwart - Vereinskassen-System ({username})")
        self.root.geometry("400x400")

        # GUI-Elemente hinzufügen
        self.render_dashboard()

    def render_dashboard(self):
        """Rendert das Haupt-Dashboard der Kassenwart-GUI."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Lösche alle bestehenden Widgets

        # Begrüßungstext
        tk.Label(self.root, text=f"Willkommen, {self.username}!", font=("Arial", 14, "bold")).pack(pady=20)

        # Wenn keine Konten verfügbar sind
        if not self.allowed_accounts:
            tk.Label(self.root, text="Keine zugewiesenen Konten gefunden!", fg="red", font=("Arial", 12, "bold")).pack(pady=20)
            tk.Button(self.root, text="Zurück", command=self.logout).pack(pady=10)
            return

        # Buttons für Aktionen
        tk.Button(self.root, text="Einzahlung tätigen", command=self.deposit_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Auszahlung tätigen", command=self.withdraw_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Umbuchung zwischen Konten", command=self.transfer_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Transaktionshistorie anzeigen", command=self.show_transactions).pack(pady=5, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)

    def deposit_money(self):
        """Lässt den Kassenwart Geld auf sein Konto einzahlen."""

        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine zugewiesenen Konten!")
            return

        account = self.allowed_accounts[0]  # Kassenwart hat nur Zugriff auf sein Konto
        amount = self.get_amount("Gib den Einzahlungsbetrag ein:")
        if amount is None:
            return

        source = simpledialog.askstring("Quelle", "Woher kommt das Geld?")
        note = simpledialog.askstring("Notiz", "Gibt es eine Notiz zur Einzahlung?")

        result = self.account_manager.deposit(account, amount, source, note)
        print(f"[DEBUG] Einzahlungsergebnis: {result}")

        messagebox.showinfo("Einzahlung", result.get("success", result.get("error", "Fehler")))

    def withdraw_money(self):
        print("[DEBUG] Auszahlung wurde angeklickt.")
        messagebox.showinfo("Auszahlung", "Funktion für Auszahlung wird implementiert.")

    def transfer_money(self):
        print("[DEBUG] Umbuchung wurde angeklickt.")
        messagebox.showinfo("Umbuchung", "Funktion für Umbuchung wird implementiert.")

    def show_transactions(self):
        """Zeigt die Transaktionshistorie für das Konto des Kassenwarts."""

        # Prüfe, ob der Kassenwart Zugriff auf ein oder mehrere Konten hat
        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine Konten zugewiesen!")
            return

        # Falls der Kassenwart nur ein Konto hat, wähle es direkt
        if len(self.allowed_accounts) == 1:
            account = self.allowed_accounts[0]
        else:
            # Falls mehrere Konten verfügbar sind, kann er eines auswählen
            account = simpledialog.askstring(
                "Konto auswählen",
                "Wähle ein Konto zur Anzeige der Transaktionshistorie:",
                initialvalue=self.allowed_accounts[0]
            )

        if not account or account not in self.allowed_accounts:
            messagebox.showerror("Fehler", "Ungültige Kontoauswahl.")
            return

        # Transaktionshistorie abrufen
        transactions = self.account_manager.get_transaction_history(account)
        print(f"[DEBUG] Transaktionshistorie für {account}: {transactions}")

        if "error" in transactions:
            messagebox.showerror("Fehler", transactions["error"])
            return

        # Neues Fenster für die Transaktionshistorie
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Transaktionshistorie - {account}")
        history_window.geometry("600x400")

        # Überschrift
        tk.Label(history_window, text=f"Transaktionshistorie für Konto: {account}", font=("Arial", 14, "bold")).pack(
            pady=10)

        # Falls keine Transaktionen vorhanden sind
        if not transactions:
            tk.Label(history_window, text="Keine Transaktionen gefunden!", fg="red").pack(pady=10)
        else:
            # Transaktionen anzeigen
            for transaction in transactions:
                text = (
                    f"Datum: {transaction['date']}, "
                    f"Typ: {transaction['type']}, "
                    f"Betrag: {transaction['amount']}€, "
                    f"Quelle: {transaction['source']}, "
                    f"Notiz: {transaction['note']}"
                )
                tk.Label(history_window, text=text, anchor="w", justify="left", wraplength=580).pack(pady=2)

        # Schließen-Button
        tk.Button(history_window, text="Schließen", command=history_window.destroy).pack(pady=10)

    def logout(self):
        print("[DEBUG] Logout wurde angeklickt.")
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()
            root.deiconify()  # Zeigt das Login-Fenster wieder an

if __name__ == "__main__":
    # Test-Modus: Standard-Benutzer für Direktstart
    test_username = "Lisa"  # Standard-Benutzername für Testzwecke
    print(f"[DEBUG] Starte Kassenwart-GUI im Testmodus für Benutzer: {test_username}")

    root = tk.Tk()
    app = KassenwartDashboard(root, test_username)
    root.mainloop()