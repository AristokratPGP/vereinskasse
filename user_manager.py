import csv
import os

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_list(self):
        """Konvertiert das User-Objekt in eine Liste für CSV."""
        return [self.username, self.password, self.role]


class UserManager:
    CSV_FILE = os.path.join(os.path.dirname(__file__), "users.csv")
    HEADER = ["Benutzername", "Passwort", "Rolle"]

    def __init__(self):
        self.users = self.load_users() or {}

    def load_users(self):
        """Lädt Benutzer aus der CSV-Datei. Stellt sicher, dass der Header immer vorhanden ist."""
        users = {}
        print("Lade Benutzer aus CSV-Datei...")
        try:
            with open(UserManager.CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                # Überprüfe, ob der Header existiert, ansonsten Datei korrigieren
                if not rows or rows[0] != UserManager.HEADER:
                    print("Fehlender oder falscher Header. Datei wird korrigiert.")
                    self.save_users()  # Speichert mit korrektem Header
                    return {}

                # Lade Benutzer aus den weiteren Zeilen
                for row in rows[1:]:  # Erste Zeile (Header) überspringen
                    if len(row) == 3:
                        username, password, role = row
                        users[username] = User(username, password, role)
            print("Benutzer erfolgreich geladen:", users.keys())
        except FileNotFoundError:
            print("Fehler: CSV-Datei nicht gefunden. Neue Datei wird erstellt.")
            self.save_users()
        return users

    def save_users(self):
        """Speichert Benutzer in die CSV-Datei mit festem Header."""
        with open(UserManager.CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(UserManager.HEADER)  # Header schreiben
            for user in self.users.values():
                writer.writerow(user.to_list())

    def add_user(self, username, password, role):
        if username in self.users:
            return "Fehler: Benutzer existiert bereits."
        self.users[username] = User(username, password, role)
        self.save_users()
        return f"Benutzer '{username}' mit Rolle '{role}' hinzugefügt."

    def edit_user(self, username, new_username=None, new_password=None, new_role=None):
        if username not in self.users:
            return "Fehler: Benutzer nicht gefunden."

        user = self.users.pop(username)
        new_username = new_username or user.username
        new_password = new_password or user.password
        new_role = new_role or user.role

        self.users[new_username] = User(new_username, new_password, new_role)
        self.save_users()
        return f"Benutzer aktualisiert: {new_username}, Rolle: {new_role}"

    def delete_user(self, username):
        if username not in self.users:
            return "Fehler: Benutzer nicht gefunden."
        
        del self.users[username]
        self.save_users()
        return f"Benutzer '{username}' gelöscht."

    def list_users(self):
        if not self.users:
            return "Keine Benutzer vorhanden."
        return "\n".join([f"{user}: {info.role}" for user, info in self.users.items()])


def main():
    manager = UserManager()
    
    while True:
        print("\nBenutzerverwaltung:")
        print("1 - Benutzer hinzufügen")
        print("2 - Benutzer bearbeiten")
        print("3 - Benutzer löschen")
        print("4 - Benutzer anzeigen")
        print("5 - Beenden")
        choice = input("Wähle eine Option: ").strip()

        if choice == "1":
            username = input("Benutzername: ").strip()
            password = input("Passwort: ").strip()
            role = input("Rolle: ").strip()
            print(manager.add_user(username, password, role))
        
        elif choice == "2":
            username = input("Welcher Benutzer soll geändert werden? ").strip()
            new_username = input("Neuer Benutzername (leer lassen für keine Änderung): ").strip() or None
            new_password = input("Neues Passwort (leer lassen für keine Änderung): ").strip() or None
            new_role = input("Neue Rolle (leer lassen für keine Änderung): ").strip() or None
            print(manager.edit_user(username, new_username, new_password, new_role))
        
        elif choice == "3":
            username = input("Welchen Benutzer löschen? ").strip()
            print(manager.delete_user(username))

        elif choice == "4":
            print("\nBenutzerliste:")
            print(manager.list_users())

        elif choice == "5":
            print("Beende das Programm.")
            break
        
        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")

if __name__ == "__main__":
    main()
