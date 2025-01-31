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

    def get_amount(self, prompt: str):
        """Zeigt einen Dialog zur Eingabe eines Betrags und validiert die Eingabe."""
        while True:
            amount_str = simpledialog.askstring("Betragseingabe", prompt)
            if amount_str is None:  # Benutzer hat Abbrechen gedrückt
                return None
            try:
                amount = float(amount_str)
                if amount > 0:
                    return amount
                else:
                    messagebox.showerror("Fehler", "Der Betrag muss positiv sein!")
            except ValueError:
                messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")

    def withdraw_money(self):
        """Ermöglicht dem Kassenwart eine Auszahlung."""
        print("[DEBUG] Auszahlung wurde angeklickt.")

        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine zugewiesenen Konten!")
            return

        account = simpledialog.askstring("Konto auswählen", "Von welchem Konto soll abgehoben werden?",
                                         initialvalue=self.allowed_accounts[0])
        if account not in self.allowed_accounts:
            messagebox.showerror("Fehler", "Ungültiges Konto ausgewählt.")
            return

        amount = self.get_amount("Gib den Auszahlungsbetrag ein:")
        if amount is None:
            return

        note = simpledialog.askstring("Notiz", "Gibt es eine Notiz zur Auszahlung?")

        result = self.account_manager.withdraw(account, amount, note)
        print(f"[DEBUG] Auszahlungsergebnis: {result}")

        messagebox.showinfo("Auszahlung", result.get("success", result.get("error", "Fehler")))

    def transfer_money(self):
        """Ermöglicht dem Kassenwart eine Umbuchung zwischen seinen Konten."""
        print("[DEBUG] Umbuchung wurde angeklickt.")

        if len(self.allowed_accounts) < 2:
            messagebox.showerror("Fehler", "Mindestens zwei Konten sind erforderlich für eine Umbuchung!")
            return

        from_account = simpledialog.askstring("Von Konto", "Von welchem Konto soll das Geld transferiert werden?",
                                              initialvalue=self.allowed_accounts[0])
        if from_account not in self.allowed_accounts:
            messagebox.showerror("Fehler", "Ungültiges Ausgangskonto.")
            return

        to_account = simpledialog.askstring("Zielkonto", "Auf welches Konto soll das Geld transferiert werden?",
                                            initialvalue=self.allowed_accounts[1])
        if to_account not in self.allowed_accounts or from_account == to_account:
            messagebox.showerror("Fehler", "Ungültiges Zielkonto.")
            return

        amount = self.get_amount("Gib den Transferbetrag ein:")
        if amount is None:
            return

        note = simpledialog.askstring("Notiz", "Gibt es eine Notiz zur Umbuchung?")

        result = self.account_manager.transfer(from_account, to_account, amount, note)
        print(f"[DEBUG] Umbuchungsergebnis: {result}")

        messagebox.showinfo("Umbuchung", result.get("success", result.get("error", "Fehler")))

    def deposit_money(self):
        """Ermöglicht dem Kassenwart eine Einzahlung auf ein bestimmtes Konto."""
        print("[DEBUG] Einzahlung wurde angeklickt.")

        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine zugewiesenen Konten!")
            return

        account = simpledialog.askstring("Konto auswählen", "Auf welches Konto soll eingezahlt werden?",
                                         initialvalue=self.allowed_accounts[0])
        if account not in self.allowed_accounts:
            messagebox.showerror("Fehler", "Ungültiges Konto ausgewählt.")
            return

        amount = self.get_amount("Gib den Einzahlungsbetrag ein:")
        if amount is None:
            return

        source = simpledialog.askstring("Quelle", "Woher kommt das Geld?")
        note = simpledialog.askstring("Notiz", "Gibt es eine Notiz zur Einzahlung?")

        result = self.account_manager.deposit(account, amount, source, note)
        print(f"[DEBUG] Einzahlungsergebnis: {result}")

        messagebox.showinfo("Einzahlung", result.get("success", result.get("error", "Fehler")))

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