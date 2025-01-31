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

    def load_data(self):
        """Loads accounts and transactions from the JSON file."""
        print("[DEBUG] Loading data from JSON...")
        try:
            with open(AccountManager.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[DEBUG] Error: JSON file not found or invalid. Creating a new file.")
            return {"accounts": {}, "users": {}}

    def save_data(self):
        """Saves data to the JSON file."""
        print("[DEBUG] Saving data to JSON...")
        with open(AccountManager.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def create_account(self, name: str) -> Dict:
        """Creates a new department account."""
        print(f"[DEBUG] Creating account: {name}")

        if name in self.data["accounts"]:
            return {"error": f"Account '{name}' already exists."}

        self.data["accounts"][name] = {"balance": 0, "transactions": []}
        self.save_data()
        return {"success": f"Account '{name}' successfully created."}

    def delete_account(self, name: str) -> Dict:
        """Deletes an account if the balance is zero."""
        print(f"[DEBUG] Deleting account: {name}")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        if self.data["accounts"][name]["balance"] > 0:
            return {"error": f"Account '{name}' still has funds and cannot be deleted."}

        del self.data["accounts"][name]
        self.save_data()
        return {"success": f"Account '{name}' successfully deleted."}

    def deposit(self, name: str, amount: float, source: str, note: str = "") -> Dict:
        """Deposits money into an account."""
        print(f"[DEBUG] Deposit: {amount}€ into '{name}'")

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
        print(f"[DEBUG] Withdrawal: {amount}€ from '{name}'")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        if amount <= 0:
            return {"error": "Amount must be positive."}

        if self.data["accounts"][name]["balance"] < amount:
            return {"error": "Insufficient funds."}

        self.data["accounts"][name]["balance"] -= amount
        transaction = Transaction(name, "Withdrawal", amount, "Account", note).to_dict()
        self.data["accounts"][name]["transactions"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ withdrawn from '{name}'.", "transaction": transaction}

    def get_transaction_history(self, name: str) -> List[Dict]:
        """Returns the transaction history of an account."""
        print(f"[DEBUG] Loading transaction history for account: {name}")

        if name not in self.data["accounts"]:
            return {"error": f"Account '{name}' does not exist."}

        return self.data["accounts"][name]["transactions"]

    def transfer(self, from_account: str, to_account: str, amount: float, note: str = "") -> Dict:
        """Transfers money between two accounts."""
        print(f"[DEBUG] Transfer: {amount}€ from '{from_account}' to '{to_account}'")

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
        print(f"[DEBUG] Exporting account '{name}' to .txt")

        if name not in self.data["accounts"]:
            print(f"[ERROR] Account '{name}' does not exist.")
            return

        account = self.data["accounts"][name]
        filename = f"{name}_account.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Account: {name}\n")
            file.write(f"Current Balance: {account['balance']}€\n")
            file.write("\n--- Transactions ---\n")
            for t in account["transactions"]:
                file.write(f"{t['date']} | {t['type']}: {t['amount']}€ | Source: {t['source']} | Note: {t['note']} | Target: {t['target_account'] if t['target_account'] else '-'}\n")

        print(f"[DEBUG] Account '{name}' was saved in '{filename}'.")

    def get_all_accounts_summary(self):
        """Returns a list of all accounts with their current balances and the total sum of all accounts."""
        print("[DEBUG] Creating summary of all accounts...")

        if not self.data["accounts"]:
            print("[ERROR] No accounts found.")
            return {"error": "No accounts available."}

        total_sum = sum(account["balance"] for account in self.data["accounts"].values())
        accounts_list = [f"{name}: {account['balance']}€" for name, account in self.data["accounts"].items()]

        print(f"[DEBUG] Total balance of all accounts: {total_sum}€")

        return {
            "accounts": accounts_list,
            "total_balance": total_sum
        }
