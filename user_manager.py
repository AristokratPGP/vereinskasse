import json
import os

class User:
    """Repräsentiert einen Benutzer mit seinen Eigenschaften."""
    def __init__(self, username, password, role, konten=None):
        self.username = username
        self.password = password
        self.role = role
        self.konten = konten if konten is not None else []  # Keine Konten bedeutet Zugriff auf alle

    def has_access_to(self, konto_name):
        """Prüft, ob der Benutzer auf ein bestimmtes Konto Zugriff hat."""
        return self.role != "Kassenwart" or not self.konten or konto_name in self.konten

    def to_dict(self):
        """Wandelt das User-Objekt in ein Dictionary um."""
        return {
            "passwort": self.password,
            "rolle": self.role,
            "konten": self.konten
        }

    def __repr__(self):
        konten_text = "Alle Konten" if not self.konten and self.role == "Kassenwart" else ", ".join(self.konten)
        return f"User(username={self.username}, role={self.role}, konten={konten_text})"


class UserManager:
    JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")

    def __init__(self):
        self.data = self.load_data()
        self.users = self.load_users()

    def load_data(self):
        """Lädt die Daten aus der JSON-Datei."""
        print("[DEBUG] Lade Daten aus JSON-Datei...")
        try:
            with open(UserManager.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[DEBUG] Fehler: JSON-Datei nicht gefunden oder ungültig. Erstelle neue Datei.")
            return {"konten": {}, "users": {}}

    def save_data(self):
        """Speichert die Daten in die JSON-Datei."""
        print("[DEBUG] Speichere Daten in JSON-Datei...")
        self.data["users"] = {user.username: user.to_dict() for user in self.users.values()}
        with open(UserManager.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def load_users(self):
        """Lädt alle Benutzer in User-Objekte."""
        print("[DEBUG] Lade Benutzer...")
        users_dict = self.data.get("users", {})
        users = {
            username: User(username, data["passwort"], data["rolle"], data["konten"])
            for username, data in users_dict.items()
        }
        print(f"[DEBUG] Geladene Benutzer: {users}")
        return users

    def add_user(self, username, password, role, konten=None):
        """Fügt einen neuen Benutzer hinzu."""
        print(f"[DEBUG] Füge Benutzer hinzu: {username}, Rolle: {role}")
        
        if username in self.users:
            return "[ERROR] Benutzer existiert bereits."

        if role not in ["Kassenwart", "Referent-Finanzen", "Administrator"]:
            return "[ERROR] Ungültige Rolle."

        new_user = User(username, password, role, konten if role == "Kassenwart" else [])
        self.users[username] = new_user
        self.save_data()
        return f"Benutzer '{username}' als '{role}' hinzugefügt."

    def edit_user(self, username, new_username=None, new_password=None, new_role=None, new_konten=None):
        """Bearbeitet einen Benutzer."""
        print(f"[DEBUG] Bearbeite Benutzer: {username}")

        if username not in self.users:
            return "[ERROR] Benutzer nicht gefunden."

        user = self.users[username]

        if new_username:
            print(f"[DEBUG] Ändere Benutzername zu: {new_username}")
            self.users[new_username] = self.users.pop(username)
            user = self.users[new_username]
            user.username = new_username

        if new_password:
            print("[DEBUG] Ändere Passwort.")
            user.password = new_password

        if new_role:
            print(f"[DEBUG] Ändere Rolle zu: {new_role}")
            if new_role not in ["Kassenwart", "Referent-Finanzen", "Administrator"]:
                return "[ERROR] Ungültige Rolle."
            user.role = new_role

        if new_konten is not None and user.role == "Kassenwart":
            print(f"[DEBUG] Setze neue Konten: {new_konten}")
            user.konten = new_konten

        self.save_data()
        return f"Benutzer '{user.username}' wurde aktualisiert."

    def delete_user(self, username):
        """Löscht einen Benutzer."""
        print(f"[DEBUG] Lösche Benutzer: {username}")

        if username not in self.users:
            return "[ERROR] Benutzer nicht gefunden."

        del self.users[username]
        self.save_data()
        return f"Benutzer '{username}' gelöscht."

    def list_users(self):
        """Listet alle Benutzer auf."""
        print("[DEBUG] Liste alle Benutzer auf...")
        if not self.users:
            return "Keine Benutzer vorhanden."
        
        return "\n".join([
            f"{user.username} ({user.role}) - Konten: {'Alle Konten' if not user.konten and user.role == 'Kassenwart' else ', '.join(user.konten)}"
            for user in self.users.values()
        ])


def main():
    """Testet alle Funktionen des UserManagers."""
    manager = UserManager()

    print("\n### Benutzer hinzufügen ###")
    print(manager.add_user("Max", "max123", "Kassenwart", []))  # Hat Zugriff auf alle Konten
    print(manager.add_user("Anna", "anna456", "Referent-Finanzen"))
    print(manager.add_user("Tom", "tom789", "Administrator"))

    print("\n### Alle Benutzer anzeigen ###")
    print(manager.list_users())

    print("\n### Benutzer bearbeiten ###")
    print(manager.edit_user("Max", new_password="neuesPasswort"))
    print(manager.edit_user("Max", new_role="Referent-Finanzen"))
    print(manager.edit_user("Anna", new_konten=["Basketball"]))  # Sollte keinen Effekt haben

    print("\n### Alle Benutzer nach Bearbeitung anzeigen ###")
    print(manager.list_users())

    print("\n### Benutzer löschen ###")
    print(manager.delete_user("Tom"))

    print("\n### Alle Benutzer nach Löschen anzeigen ###")
    print(manager.list_users())


if __name__ == "__main__":
    main()
