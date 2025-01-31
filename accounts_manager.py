import json
import os
import datetime
from typing import List, Dict

class Account:
    """Represents a department account with balance and transactions."""

    def __init__(self, department: str, balance: float = 0.0, transactions=None):
        self.department = department
        self.balance = balance
        self.transactions = transactions if transactions else []

    def to_dict(self) -> Dict:
        """Returns the account as a dictionary."""
        return {
            "balance": self.balance,
            "transactions": self.transactions
        }

    def __repr__(self):
        return f"Account(department={self.department}, balance={self.balance}, transactions={len(self.transactions)})"


class Transaction:
    """Represents a transaction for an account."""

    def __init__(self, account: str, type: str, amount: float, source: str, note: str = "", target_account: str = None):
        self.account = account
        self.type = type
        self.amount = amount
        self.source = source
        self.note = note
        self.target_account = target_account
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Returns the transaction as a dictionary."""
        return {
            "date": self.date,
            "account": self.account,
            "type": self.type,
            "amount": self.amount,
            "source": self.source,
            "note": self.note,
            "target_account": self.target_account,
        }

    def __repr__(self):
        return f"Transaction({self.type}, {self.amount}€, {self.account} -> {self.target_account if self.target_account else '-'})"


class AccountManager:
    """Manages accounts and transactions via the JSON file."""

    JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")

    def __init__(self):
        self.data = self.load_data()

        if "accounts" not in self.data or not isinstance(self.data["accounts"], dict):
            print(" Fehler: `accounts` fehlt oder ist ungültig. Initialisiere es neu.")
            self.data["accounts"] = {}

        print(" self.data nach Laden:", self.data)

    def load_data(self):
        """Loads accounts and transactions from the JSON file."""
        print(" Loading data from JSON...")
        try:
            with open(AccountManager.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(" [ERROR] JSON file not found or invalid. Creating a new file.")
            return {"accounts": {}, "users": {}}

    def save_data(self):
        """Saves data to the JSON file."""
        print(" Saving data to JSON...")
        try:
            with open(AccountManager.JSON_FILE, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"[ERROR] Could not save data: {e}")

    def create_account(self, name: str) -> Dict:
        """Creates a new department account."""
        print(f" Creating account: {name}")

        if name in self.data["accounts"]:
            return {"error": f"Account '{name}' already exists."}

        self.data["accounts"][name] = {"balance": 0, "transactions": []}
        self.save_data()
        return {"success": f"Account '{name}' successfully created."}

    def delete_account(self, name: str) -> Dict:
        """Deletes an account if the balance is zero."""
        print(f" Deleting account: {name}")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        if self.data["accounts"][name]["balance"] != 0:
            return {"error": f"Account '{name}' still has a non-zero balance and cannot be deleted."}


        del self.data["accounts"][name]
        self.save_data()
        return {"success": f"Account '{name}' successfully deleted."}

    def deposit(self, name: str, amount: float, source: str, note: str = "") -> Dict:
        """Deposits money into an account."""
        print(f" Deposit: {amount}€ into '{name}'")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}
        
        if amount <= 0:
            return {"error": "Amount must be positive."}

        self.data["accounts"][name]["balance"] += amount
        transaction = Transaction(name, "Deposit", amount, source, note).to_dict()
        self.data["accounts"][name]["transactions"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ deposited into '{name}'.", "transaction": transaction}

    def withdraw(self, name: str, amount: float, note: str = "") -> Dict:
        """Withdraws money from an account."""
        print(f" Withdrawal: {amount}€ from '{name}'")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        if amount <= 0:
            return {"error": "Amount must be positive."}

        new_balance = self.data["accounts"][name]["balance"] - amount
        if new_balance < 0:
            return {"error": "Insufficient funds. Withdrawal denied."}

        self.data["accounts"][name]["balance"] -= amount
        transaction = Transaction(name, "Withdrawal", amount, "Account", note).to_dict()
        self.data["accounts"][name]["transactions"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ withdrawn from '{name}'.", "transaction": transaction}

    def get_transaction_history(self, name: str) -> List[Dict]:
        """Returns the transaction history of an account."""
        print(f" Loading transaction history for account: {name}")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        return self.data["accounts"][name]["transactions"]

    def transfer(self, from_account: str, to_account: str, amount: float, note: str = "") -> Dict:
        """Transfers money between two accounts."""
        print(f" Transfer: {amount}€ from '{from_account}' to '{to_account}'")

        if from_account not in self.data["accounts"] or to_account not in self.data["accounts"]:
            return {"error": "One of the accounts does not exist."}

        if amount <= 0:
            return {"error": "Amount must be positive."}

        if self.data["accounts"][from_account]["balance"] < amount:
            return {"error": "Insufficient funds for transfer."}

        self.data["accounts"][from_account]["balance"] -= amount
        self.data["accounts"][to_account]["balance"] += amount
        transaction = Transaction(from_account, "Transfer", amount, "Internal", note, to_account).to_dict()
        self.data["accounts"][from_account]["transactions"].append(transaction)
        self.data["accounts"][to_account]["transactions"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ transferred from '{from_account}' to '{to_account}'.", "transaction": transaction}

    def export_account_to_txt(self, name: str):
        """Saves an account with its balance and transactions to a .txt file."""
        print(f" Exporting account '{name}' to .txt")

        if name not in self.data["accounts"]:
            print(f"[ERROR] Account '{name}' does not exist.")
            return

        account = self.data["accounts"][name]
        filename = f"{name}_account.txt"

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Account: {name}\n")
                file.write(f"Current Balance: {account['balance']}€\n")
                file.write("\n--- Transactions ---\n")
                for t in account["transactions"]:
                    file.write(f"{t['date']} | {t['type']}: {t['amount']}€ | Source: {t['source']} | Note: {t['note']} | Target: {t['target_account'] if t['target_account'] else '-'}\n")
        except IOError as e:
            print(f"[ERROR] Could not export account: {e}")

        print(f" Account '{name}' was saved in '{filename}'.")

    def get_all_accounts_summary(self):
        """Gibt eine Liste aller Konten mit Saldo und Gesamtsumme zurück."""
        print(" Erstelle Konto-Übersicht...")

        if "accounts" not in self.data or not isinstance(self.data["accounts"], dict):
            print("[ERROR] `accounts` fehlt oder ist ungültig.")
            return {"error": "No accounts available."}

        if not self.data["accounts"]:  # Falls die Accounts-Liste leer ist
            print("[ERROR] Keine Konten vorhanden.")
            return {"error": "No accounts available."}

        total_sum = sum(account["balance"] for account in self.data["accounts"].values())
        accounts_list = [f"{name}: {account['balance']}€" for name, account in self.data["accounts"].items()]

        print(f" Gesamtguthaben: {total_sum}€")

        return {
            "accounts": accounts_list,
            "total_balance": total_sum
        }