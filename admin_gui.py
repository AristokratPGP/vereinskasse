__author__ = "7985984, Saghdaou, 8441241, Fischer"

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from user_manager import UserManager
import accounts_manager
from accounts_manager import AccountManager



class AdminUserManagement:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.root.title("Benutzerverwaltung - Admin")
        self.root.geometry("500x500")

        tk.Label(self.root, text="Benutzerverwaltung", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Benutzer hinzufügen", command=self.add_user).pack(pady=5, fill="x")
        tk.Button(self.root, text="Benutzer bearbeiten", command=self.edit_user).pack(pady=5, fill="x")
        tk.Button(self.root, text="Benutzer löschen", command=self.delete_user).pack(pady=5, fill="x")
        tk.Button(self.root, text="Alle Benutzer anzeigen", command=self.list_users).pack(pady=5, fill="x")
        tk.Button(self.root, text="Schließen", command=self.root.quit).pack(pady=20)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def add_user(self):
        """Ermöglicht dem Admin, einen neuen Benutzer hinzuzufügen."""
        username = simpledialog.askstring("Benutzer hinzufügen", "Benutzername eingeben:")
        if not username:
            return
        password = simpledialog.askstring("Passwort", "Passwort eingeben:", show='*')
        role = simpledialog.askstring("Rolle", "Rolle eingeben (Administrator, Treasurer, Finance-Referent):")

        if role not in ["Administrator", "Treasurer", "Finance-Referent"]:
            messagebox.showerror("Fehler", "Ungültige Rolle!")
            return

        accounts = []
        if role == "Treasurer":
            accounts_input = simpledialog.askstring("Konten", "Gib die Konten an, getrennt durch Kommas:")
            if accounts_input:
                accounts = [acc.strip() for acc in accounts_input.split(",")]

        result = self.user_manager.add_user(username, password, role, accounts)
        messagebox.showinfo("Benutzer hinzufügen", result)

    def edit_user(self):
        """Ermöglicht dem Admin, einen existierenden Benutzer zu bearbeiten."""
        username = simpledialog.askstring("Benutzer bearbeiten", "Welchen Benutzer möchtest du bearbeiten?")
        if not username or username not in self.user_manager.users:
            messagebox.showerror("Fehler", "Benutzer nicht gefunden!")
            return

        new_password = simpledialog.askstring("Neues Passwort",
                                              "Neues Passwort eingeben (leer lassen, um es zu behalten):", show='*')
        new_role = simpledialog.askstring("Neue Rolle", "Neue Rolle eingeben (leer lassen, um sie zu behalten):")

        if new_role == "Treasurer" or (not new_role and self.user_manager.users[username].role == "Treasurer"):
            accounts_input = simpledialog.askstring("Konten",
                                                    "Neue Konten angeben (leer lassen, um bestehende zu behalten):")
            if accounts_input:
                new_accounts = [acc.strip() for acc in accounts_input.split(",")]
        if new_role and new_role not in ["Administrator", "Treasurer", "Finance-Referent"]:
            messagebox.showerror("Fehler", "Ungültige Rolle!")
            return

        result = self.user_manager.edit_user(username, new_password=new_password if new_password else None,
                                             new_role=new_role if new_role else None)
        messagebox.showinfo("Benutzer bearbeiten", result)

    def delete_user(self):
        """Ermöglicht dem Admin, einen Benutzer zu löschen."""
        username = simpledialog.askstring("Benutzer löschen", "Welchen Benutzer möchtest du löschen?")
        if not username or username not in self.user_manager.users:
            messagebox.showerror("Fehler", "Benutzer nicht gefunden!")
            return

        if messagebox.askyesno("Bestätigung", f"Möchtest du den Benutzer '{username}' wirklich löschen?"):
            result = self.user_manager.delete_user(username)
            messagebox.showinfo("Benutzer löschen", result)

    def list_users(self):
        """Zeigt eine Liste aller Benutzer in einer übersichtlichen Tabelle an."""
        users_list = self.user_manager.users
        if not users_list:
            messagebox.showinfo("Benutzerliste", "Keine Benutzer vorhanden.")
            return

        list_window = tk.Toplevel(self.root)
        list_window.title("Benutzerliste")
        list_window.geometry("600x300")

        tk.Label(list_window, text="Benutzerliste", font=("Arial", 12, "bold")).pack(pady=10)

        columns = ("Benutzername", "Rolle", "Konten")
        tree = ttk.Treeview(list_window, columns=columns, show="headings")
        tree.heading("Benutzername", text="Benutzername")
        tree.heading("Rolle", text="Rolle")
        tree.heading("Konten", text="Konten")

        for user in users_list.values():
            tree.insert("", "end",
                        values=(user.username, user.role, ", ".join(user.accounts) if user.accounts else "-"))

        tree.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(list_window, text="Schließen", command=list_window.destroy).pack(pady=10)

    def logout(self):
        """Schließt das aktuelle Fenster und zeigt das Login-Fenster wieder an."""
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()  # Schließt das aktuelle Fenster
            import login_gui  # Stellt sicher, dass das Login-Fenster geladen wird
            login_gui.root.deiconify()  # Zeigt das Login-Fenster wieder an





class AdminAccountManagement:
    def __init__(self, root):
        self.root = root
        self.account_manager = AccountManager()
        self.root.title("Kontoverwaltung - Admin")
        self.root.geometry("500x500")

        tk.Label(self.root, text="Kontoverwaltung", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Konto hinzufügen", command=self.add_account).pack(pady=5, fill="x")
        tk.Button(self.root, text="Konto löschen", command=self.delete_account).pack(pady=5, fill="x")
        tk.Button(self.root, text="Kontenübersicht", command=self.show_account_summary).pack(pady=5, fill="x")
        tk.Button(self.root, text="Schließen", command=self.root.quit).pack(pady=20)

    def add_account(self):
        """Ermöglicht dem Admin, ein neues Vereinskonto zu erstellen."""
        account_name = simpledialog.askstring("Konto hinzufügen", "Name des neuen Kontos:")
        if not account_name:
            return

        result = self.account_manager.create_account(account_name)
        messagebox.showinfo("Konto hinzufügen", result.get("success", result.get("error", "Fehler beim Erstellen.")))

    def delete_account(self):
        """Ermöglicht dem Admin, ein Konto zu löschen, falls es ein Guthaben von 0€ hat."""
        account_name = simpledialog.askstring("Konto löschen", "Welches Konto möchtest du löschen?")
        if not account_name:
            return

        result = self.account_manager.delete_account(account_name)
        messagebox.showinfo("Konto löschen", result.get("success", result.get("error", "Fehler beim Löschen.")))

    def show_account_summary(self):
        """Zeigt eine Übersicht aller existierenden Konten mit Namen und Saldo in der GUI."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Löscht alle alten Widgets, um die Übersicht anzuzeigen

        tk.Label(self.root, text="Kontenübersicht", font=("Arial", 14, "bold")).pack(pady=10)

        accounts_data = self.account_manager.get_all_accounts_summary()  # Holt alle Konten

        # **Falls keine Konten existieren**
        if "error" in accounts_data:
            tk.Label(self.root, text="Keine Konten vorhanden.", fg="red").pack(pady=5)
            tk.Button(self.root, text="Zurück", command=self.return_to_dashboard).pack(pady=10)
            return

        # **Durch alle Konten iterieren und Buttons erstellen**
        for account in accounts_data["accounts"]:
            account_name = account["name"]  # Richtiger Zugriff auf den Kontonamen
            balance = account["balance"]  # Richtiger Zugriff auf den Saldo

            btn = tk.Button(
                self.root,
                text=f"{account_name}: {balance}€",  # Zeigt den Kontonamen und Saldo an
                command=lambda acc=account_name: self.view_account_history(acc)
            )
            btn.pack(pady=2, fill="x")

        # **Gesamtguthaben aller Konten anzeigen**
        tk.Label(self.root, text=f"Gesamtsumme aller Konten: {accounts_data['total_balance']}€",
                 font=("Arial", 12, "bold")).pack(pady=10)

        # **Zurück & Logout-Buttons**
        tk.Button(self.root, text="Zurück", command=self.return_to_dashboard).pack(pady=10)

    def view_account_history(self, account_name):
        """Zeigt die Transaktionshistorie für ein spezifisches Konto."""
        # Neues Fenster für die Historie erstellen
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Historie für {account_name}")
        history_window.geometry("500x400")

        tk.Label(history_window, text=f"Historie: {account_name}", font=("Arial", 14, "bold")).pack(pady=10)

        # Kontodaten laden
        transactions = self.account_manager.get_transaction_history(account_name)  # Transaktionen abrufen

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
                tk.Label(trans_frame, text=f"Datum: {transaction['date']}", anchor="w", bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"Typ: {transaction['type']}, Betrag: {transaction['amount']}€", anchor="w",
                         bg="#f9f9f9").pack(anchor="w")
                tk.Label(trans_frame, text=f"Quelle: {transaction['source']}", anchor="w", bg="#f9f9f9").pack(
                    anchor="w")
                if transaction['note']:
                    tk.Label(trans_frame, text=f"Notiz: {transaction['note']}", anchor="w", bg="#f9f9f9").pack(
                        anchor="w")

    def return_to_dashboard(self):
        """Schließt die aktuelle Ansicht und zeigt das Admin-Dashboard wieder an."""
        self.root.destroy()  # Kontenübersicht-Fenster schließen


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("400x300")

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Benutzerverwaltung", command=self.open_user_management).pack(pady=10, fill="x")
        tk.Button(self.root, text="Kontoverwaltung", command=self.open_account_management).pack(pady=10, fill="x")
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def open_user_management(self):
        """Öffnet das Benutzerverwaltungs-Fenster."""
        user_window = tk.Toplevel(self.root)
        AdminUserManagement(user_window)

    def open_account_management(self):
        """Öffnet das Kontoverwaltungs-Fenster."""
        account_window = tk.Toplevel(self.root)
        AdminAccountManagement(account_window)

    def logout(self):
        """Schließt das Admin-Dashboard und kehrt zum Login zurück."""
        if messagebox.askyesno("Logout", "Möchtest du dich wirklich ausloggen?"):
            self.root.destroy()
            import login_gui
            login_gui.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()

