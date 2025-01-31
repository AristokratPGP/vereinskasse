__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from user_manager import UserManager
from accounts_manager import AccountManager

class KassenwartDashboard:
    """
    Dashboard for treasurers to manage club accounts.
    """
    def __init__(self, root, username):
        """Initializes the treasurer dashboard window."""
        self.root = root
        self.username = username
        self.user_manager = UserManager()
        self.account_manager = AccountManager()

        # Load the allowed accounts for the user
        self.allowed_accounts = self.user_manager.get_kassenwart_accounts(username).get("accounts", [])
        print(f"[DEBUG] Erlaubte Konten für {username}: {self.allowed_accounts}")

        self.root.title(f"Kassenwart - Vereinskassen-System ({username})")
        self.root.geometry("400x400")

        # Add GUI elements
        self.render_dashboard()

    def render_dashboard(self):
        """Renders the main dashboard of the cashier GUI."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Lösche alle bestehenden Widgets

        # Welcome text
        tk.Label(self.root, text=f"Willkommen, {self.username}!", font=("Arial", 14, "bold")).pack(pady=20)

        # If no accounts are available
        if not self.allowed_accounts:
            tk.Label(self.root, text="Keine zugewiesenen Konten gefunden!", fg="red", font=("Arial", 12, "bold")).pack(pady=20)
            tk.Button(self.root, text="Zurück", command=self.logout).pack(pady=10)
            return

        # Buttons for actions
        tk.Button(self.root, text="Einzahlung tätigen", command=self.deposit_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Auszahlung tätigen", command=self.withdraw_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Umbuchung zwischen Konten", command=self.transfer_money).pack(pady=5, fill="x")
        tk.Button(self.root, text="Transaktionshistorie anzeigen", command=self.show_transactions).pack(pady=5, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)

    def deposit_money(self):
        """Has the treasurer deposit money into his account."""

        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine zugewiesenen Konten!")
            return

        account = self.allowed_accounts[0]  # Treasurer only has access to his account
        amount = self.get_amount("Gib den Einzahlungsbetrag ein:")
        if amount is None:
            return

        source = simpledialog.askstring("Quelle", "Woher kommt das Geld?")
        note = simpledialog.askstring("Notiz", "Gibt es eine Notiz zur Einzahlung?")

        result = self.account_manager.deposit(account, amount, source, note)
        print(f"[DEBUG] Einzahlungsergebnis: {result}")

        messagebox.showinfo("Einzahlung", result.get("success", result.get("error", "Fehler")))

    def get_amount(self, prompt: str):
        """Shows a dialog for entering an amount and validates the entry."""
        while True:
            amount_str = simpledialog.askstring("Betragseingabe", prompt)
            if amount_str is None:  # User has pressed Cancel
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
        """Allows the treasurer to make a payment."""
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
        """Allows the treasurer to transfer funds between his accounts."""
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



    def show_transactions(self):
        """Shows the transaction history for the cashier's account."""

        # Check whether the treasurer has access to one or more accounts
        if not self.allowed_accounts:
            messagebox.showerror("Fehler", "Du hast keine Konten zugewiesen!")
            return

        # If the treasurer only has one account, select it directly
        if len(self.allowed_accounts) == 1:
            account = self.allowed_accounts[0]
        else:
            # If several accounts are available, he can select one
            account = simpledialog.askstring(
                "Konto auswählen",
                "Wähle ein Konto zur Anzeige der Transaktionshistorie:",
                initialvalue=self.allowed_accounts[0]
            )

        if not account or account not in self.allowed_accounts:
            messagebox.showerror("Fehler", "Ungültige Kontoauswahl.")
            return


        transactions = self.account_manager.get_transaction_history(account)
        print(f"[DEBUG] Transaktionshistorie für {account}: {transactions}")

        if "error" in transactions:
            messagebox.showerror("Fehler", transactions["error"])
            return

        # New window for the transaction history
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Transaktionshistorie - {account}")
        history_window.geometry("600x400")


        tk.Label(history_window, text=f"Transaktionshistorie für Konto: {account}", font=("Arial", 14, "bold")).pack(
            pady=10)

        # If no transactions are available
        if not transactions:
            tk.Label(history_window, text="Keine Transaktionen gefunden!", fg="red").pack(pady=10)
        else:
            for transaction in transactions:
                text = (
                    f"Datum: {transaction['date']}, "
                    f"Typ: {transaction['type']}, "
                    f"Betrag: {transaction['amount']}€, "
                    f"Quelle: {transaction['source']}, "
                    f"Notiz: {transaction['note']}"
                )
                tk.Label(history_window, text=text, anchor="w", justify="left", wraplength=580).pack(pady=2)

        # Close button
        tk.Button(history_window, text="Schließen", command=history_window.destroy).pack(pady=10)


    def logout(self):
        """Closes the current window and displays the login window again."""
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()
            import login_gui
            login_gui.root.deiconify()


if __name__ == "__main__":
    test_username = "Lisa"
    print(f"[DEBUG] Starte Kassenwart-GUI im Testmodus für Benutzer: {test_username}")

    root = tk.Tk()
    app = KassenwartDashboard(root, test_username)
    root.mainloop()