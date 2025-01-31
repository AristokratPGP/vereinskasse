__author__ = "7985984, Saghdaou, 8441241, Fischer"
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import accounts_manager

class FinanzenDashboard:
    def __init__(self, root, login_root):
        """Initializes the Finance dashboard window."""
        self.root = root
        self.login_root = login_root
        self.root.title("Vereinskassen-System - Finanzen Dashboard")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Finanzen Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=0, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=0)

    def show_dashboard(self):
        """Returns from 'view_overview' to the financial dashboard."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Deletes the current widgets

        # Dashboard headline
        tk.Label(self.root, text="Finanzen Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        # Buttons for the main options of the dashboard
        tk.Button(self.root, text="Gesamtübersicht aller Konten", command=self.view_overview).pack(pady=5, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5, fill="x")
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5, fill="x")

    def view_overview(self):
        """Displays an overview of all existing accounts with name and balance."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Deletes the old widgets to display the overview

        tk.Label(self.root, text="Kontenübersicht", font=("Arial", 14, "bold")).pack(pady=10)

        manager = accounts_manager.AccountManager()  # Create instance of the AccountManager class
        accounts_data = manager.get_all_accounts_summary()  # Get all accounts

        # Check whether an error has occurred (e.g. no accounts available)
        if "error" in accounts_data:
            tk.Label(self.root, text="Keine Konten vorhanden.", fg="red").pack(pady=5)
            tk.Button(self.root, text="Zurück", command=self.__init__).pack(pady=10)
            return

        # Iterate through all accounts and create buttons
        for account in accounts_data["accounts"]:
            account_name = account["name"]  # Verwende den "name"-Key direkt
            btn = tk.Button(
                self.root,
                text=f"{account_name}: {account['balance']}€",  # Anzeigeformat anpassen
                command=lambda acc=account_name: self.view_account_history(acc)
            )
            btn.pack(pady=2, fill="x")

        # Show total of all accounts
        tk.Label(self.root, text=f"Gesamtsumme aller Konten: {accounts_data['total_balance']}€",
                 font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(self.root, text="Zurück", command=self.show_dashboard).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)           # Back to overview

    def view_account_history(self, account_name):
        """Shows the transaction history for a specific account."""
        # Create new window for the history
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Historie für {account_name}")
        history_window.geometry("500x400")

        tk.Label(history_window, text=f"Historie: {account_name}", font=("Arial", 14, "bold")).pack(pady=10)


        manager = accounts_manager.AccountManager()
        transactions = manager.get_transaction_history(account_name)

        if "error" in transactions:
            tk.Label(history_window, text=transactions["error"], fg="red", font=("Arial", 12)).pack(pady=10)
        elif not transactions:
            tk.Label(history_window, text="Keine Transaktionen vorhanden.", fg="red", font=("Arial", 12)).pack(pady=10)
        else:
            # Scrollable Frame
            canvas = tk.Canvas(history_window)
            scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            # Connect Scrollbar with Canvas
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Show transactions
            for transaction in transactions:

                trans_frame = tk.Frame(scrollable_frame, bg="#f9f9f9", bd=1, relief="solid", padx=10, pady=5)
                trans_frame.pack(fill="x", pady=5)

                # Transaction details
                tk.Label(trans_frame, text=f"date: {transaction['date']}", anchor="w", bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"type: {transaction['type']}, amount: {transaction['amount']}€", anchor="w",
                         bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"source: {transaction['source']}", anchor="w", bg="#f9f9f9").pack(
                    anchor="w")
                if transaction['note']:
                    tk.Label(trans_frame, text=f"note: {transaction['note']}", anchor="w", bg="#f9f9f9").pack(
                        anchor="w")

    def logout(self):
        """Closes the finance window and displays the login window again."""
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()

            if self.login_root:
                self.login_root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanzenDashboard(root)
    root.mainloop()