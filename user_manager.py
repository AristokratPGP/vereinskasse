import json
import os

class User:
    """Represents a user with their properties."""
    def __init__(self, username, password, role, accounts=None):
        self.username = username
        self.password = password
        self.role = role
        self.accounts = accounts if accounts is not None else []  # No accounts means access to all

    def has_access_to(self, account_name):
        """Checks if the user has access to a specific account."""
        return self.role != "Treasurer" or not self.accounts or account_name in self.accounts

    def to_dict(self):
        """Converts the User object into a dictionary."""
        return {
            "password": self.password,
            "role": self.role,
            "accounts": self.accounts
        }

    def __repr__(self):
        accounts_text = "All accounts" if not self.accounts and self.role == "Treasurer" else ", ".join(self.accounts)
        return f"User(username={self.username}, role={self.role}, accounts={accounts_text})"


class UserManager:
    JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")

    def __init__(self):
        self.data = self.load_data()
        self.users = self.load_users()

    def load_data(self):
        """Loads data from the JSON file."""
        print("[DEBUG] Loading data from JSON file...")
        try:
            with open(UserManager.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[DEBUG] Error: JSON file not found or invalid. Creating a new file.")
            return {"accounts": {}, "users": {}}

    def save_data(self):
        """Saves data to the JSON file."""
        print("[DEBUG] Saving data to JSON file...")
        self.data["users"] = {user.username: user.to_dict() for user in self.users.values()}
        with open(UserManager.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def load_users(self):
        """Loads all users into User objects."""
        print("[DEBUG] Loading users...")
        users_dict = self.data.get("users", {})
        users = {
            username: User(username, data["passwort"], data["rolle"], data["konten"])
                for username, data in users_dict.items()
            }
        print(f"[DEBUG] Loaded users: {users}")
        return users

    def add_user(self, username, password, role, accounts=None):
        """Adds a new user."""
        print(f"[DEBUG] Adding user: {username}, Role: {role}")
        
        if username in self.users:
            return "[ERROR] User already exists."

        if role not in ["Treasurer", "Finance-Referent", "Administrator"]:
            return "[ERROR] Invalid role."

        new_user = User(username, password, role, accounts if role == "Treasurer" else [])
        self.users[username] = new_user
        self.save_data()
        return f"User '{username}' added as '{role}'."

    def edit_user(self, username, new_username=None, new_password=None, new_role=None, new_accounts=None):
        """Edits an existing user."""
        print(f"[DEBUG] Editing user: {username}")

        if username not in self.users:
            return "[ERROR] User not found."

        user = self.users[username]

        if new_username:
            print(f"[DEBUG] Changing username to: {new_username}")
            self.users[new_username] = self.users.pop(username)
            user = self.users[new_username]
            user.username = new_username

        if new_password:
            print("[DEBUG] Changing password.")
            user.password = new_password

        if new_role:
            print(f"[DEBUG] Changing role to: {new_role}")
            if new_role not in ["Treasurer", "Finance-Referent", "Administrator"]:
                return "[ERROR] Invalid role."
            user.role = new_role

        if new_accounts is not None and user.role == "Treasurer":
            print(f"[DEBUG] Setting new accounts: {new_accounts}")
            user.accounts = new_accounts

        self.save_data()
        return f"User '{user.username}' updated."

    def delete_user(self, username):
        """Deletes a user."""
        print(f"[DEBUG] Deleting user: {username}")

        if username not in self.users:
            return "[ERROR] User not found."

        del self.users[username]
        self.save_data()
        return f"User '{username}' deleted."

    def list_users(self):
        """Lists all users."""
        print("[DEBUG] Listing all users...")
        if not self.users:
            return "No users available."
        
        return "\n".join([
            f"{user.username} ({user.role}) - Accounts: {'All accounts' if not user.accounts and user.role == 'Treasurer' else ', '.join(user.accounts)}"
            for user in self.users.values()
        ])


def main():
    """Tests all functions of the UserManager."""
    manager = UserManager()

    print("\n### Adding users ###")
    print(manager.add_user("Max", "max123", "Treasurer", []))  # Has access to all accounts
    print(manager.add_user("Anna", "anna456", "Finance-Referent"))
    print(manager.add_user("Tom", "tom789", "Administrator"))

    print("\n### Listing all users ###")
    print(manager.list_users())

    print("\n### Editing users ###")
    print(manager.edit_user("Max", new_password="newPassword"))
    print(manager.edit_user("Max", new_role="Finance-Referent"))
    print(manager.edit_user("Anna", new_accounts=["Basketball"]))  # Should have no effect

    print("\n### Listing all users after edits ###")
    print(manager.list_users())

    print("\n### Deleting users ###")
    print(manager.delete_user("Tom"))

    print("\n### Listing all users after deletion ###")
    print(manager.list_users())


if __name__ == "__main__":
    main()
