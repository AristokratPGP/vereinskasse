import json
import os

class UserManager:
    JSON_FILE = os.path.join(os.path.dirname(__file__), "users.json")

    def __init__(self):
        self.users = self.load_users() or {
            "Referent-Finanzen": [],
            "Kassenwart": {},
            "Administrator": []
        }

    def load_users(self):
        """Lädt Benutzer aus der JSON-Datei."""
        print("Lade Benutzer aus JSON-Datei...")
        try:
            with open(UserManager.JSON_FILE, "r", encoding="utf-8") as file:
                print("JSON geladen!")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Fehler: JSON-Datei nicht gefunden oder ungültig. Neue Datei wird erstellt.")
            self.save_users()
            return None

    def save_users(self):
        """Speichert Benutzer in die JSON-Datei."""
        with open(UserManager.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4, ensure_ascii=False)

    def add_user(self, username, password, role, bereich=None):
        """Fügt einen neuen Benutzer hinzu, abhängig von der Rolle. Erlaubt nur gültige Rollen."""
        VALID_ROLES = ["Referent-Finanzen", "Kassenwart", "Administrator"]

        if role not in VALID_ROLES:
            return f"Fehler: Ungültige Rolle '{role}'. Erlaubte Rollen: {', '.join(VALID_ROLES)}."

        if role == "Kassenwart":
            if not bereich:
                return "Fehler: Bereich muss für Kassenwart angegeben werden."
            if bereich not in self.users["Kassenwart"]:
                self.users["Kassenwart"][bereich] = []
            self.users["Kassenwart"][bereich].append({"Benutzername": username, "Passwort": password})
        else:
            if any(user["Benutzername"] == username for user in self.users[role]):
                return "Fehler: Benutzer existiert bereits."
            self.users[role].append({"Benutzername": username, "Passwort": password})

        self.save_users()
        return f"Benutzer '{username}' als '{role}' hinzugefügt."

    def edit_user(self, username, new_username=None, new_password=None, role=None, bereich=None):
        """Bearbeitet einen Benutzer basierend auf Rolle und Bereich. Nur gültige Rollen erlaubt."""
        VALID_ROLES = ["Referent-Finanzen", "Kassenwart", "Administrator"]

        # Automatische Erkennung der aktuellen Rolle und Bereich
        detected_role, detected_bereich = self.find_user_role_and_area(username)

        if detected_role is None:
            return "Fehler: Benutzer nicht gefunden."

        # Falls keine neue Rolle angegeben wurde, bleibt die alte erhalten
        role = role or detected_role
        bereich = bereich or detected_bereich  # Bereich bleibt erhalten, außer neue Rolle ist Kassenwart

        # Sicherstellen, dass die neue Rolle gültig ist
        if role not in VALID_ROLES:
            return f"Fehler: Ungültige Rolle '{role}'. Erlaubte Rollen: {', '.join(VALID_ROLES)}."

        # Wenn die Rolle sich zu Kassenwart ändert, muss ein Bereich gesetzt werden
        if role == "Kassenwart" and detected_role != "Kassenwart":
            if not bereich:
                return "Fehler: Neuer Kassenwart benötigt einen Bereich."

        # Wenn die Rolle vorher Kassenwart war, aber jetzt nicht mehr, dann Bereich entfernen
        if detected_role == "Kassenwart" and role != "Kassenwart":
            bereich = None  # Bereich ist nur für Kassenwarte relevant

        # Bearbeitung für Kassenwart mit Bereichszuweisung
        if role == "Kassenwart":
            if bereich not in self.users["Kassenwart"]:
                self.users["Kassenwart"][bereich] = []  # Falls Bereich nicht existiert, erstelle ihn

            # Wenn Benutzer vorher KEIN Kassenwart war, müssen wir ihn von seiner alten Rolle entfernen
            if detected_role != "Kassenwart":
                self.users[detected_role] = [user for user in self.users[detected_role] if user["Benutzername"] != username]

            # Benutzer zu neuem Bereich hinzufügen
            self.users["Kassenwart"][bereich].append({
                "Benutzername": new_username or username,
                "Passwort": new_password or "Passwort unbekannt"
            })
            self.save_users()
            return f"Benutzer '{username}' wurde zu Kassenwart im Bereich '{bereich}' geändert."

        else:
            # Bearbeitung für andere Rollen (Referent-Finanzen, Administrator)
            for user in self.users[detected_role]:
                if user["Benutzername"] == username:
                    user["Benutzername"] = new_username or user["Benutzername"]
                    user["Passwort"] = new_password or user["Passwort"]
                    self.save_users()
                    return f"Benutzer '{username}' wurde als '{role}' aktualisiert."

        return "Fehler: Benutzer nicht gefunden."

    def find_user_role_and_area(self, username):
        """Findet die Rolle und den Bereich eines Benutzers automatisch."""
        for role, users in self.users.items():
            if role == "Kassenwart":
                for bereich, kassenwarte in users.items():
                    for user in kassenwarte:
                        if user["Benutzername"] == username:
                            return role, bereich  # Gefunden als Kassenwart mit Bereich
            else:
                for user in users:
                    if user["Benutzername"] == username:
                        return role, None  # Gefunden, aber kein Bereich nötig

        return None, None  # Benutzer nicht gefunden

    def delete_user(self, username):
        """Löscht einen Benutzer, indem die Rolle und ggf. der Bereich automatisch erkannt wird."""
        role, bereich = self.find_user_role_and_area(username)

        if role is None:
            return "Fehler: Benutzer nicht gefunden."

        if role == "Kassenwart":
            self.users["Kassenwart"][bereich] = [
                user for user in self.users["Kassenwart"][bereich] if user["Benutzername"] != username
            ]
            # Falls der Bereich leer ist, lösche den Bereich aus der Struktur
            if not self.users["Kassenwart"][bereich]:
                del self.users["Kassenwart"][bereich]
        else:
            self.users[role] = [user for user in self.users[role] if user["Benutzername"] != username]

        self.save_users()
        return f"Benutzer '{username}' gelöscht."

    def list_users(self):
        """Listet alle Benutzer auf."""
        output = []
        for role, users in self.users.items():
            if role == "Kassenwart":
                for bereich, kassenwarte in users.items():
                    for user in kassenwarte:
                        output.append(f"{user['Benutzername']} (Kassenwart - {bereich})")
            else:
                for user in users:
                    output.append(f"{user['Benutzername']} ({role})")
        return "\n".join(output) if output else "Keine Benutzer vorhanden."


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
            role = input("Rolle (Referent-Finanzen/Kassenwart/Administrator): ").strip()
            bereich = None
            if role == "Kassenwart":
                bereich = input("Bereich (z. B. Tanzen, Fußball): ").strip()
            print(manager.add_user(username, password, role, bereich))
        
        elif choice == "2":
            username = input("Welcher Benutzer soll geändert werden? ").strip()

            # Automatische Erkennung von Rolle und Bereich
            detected_role, detected_bereich = manager.find_user_role_and_area(username)

            if detected_role is None:
                print("Fehler: Benutzer nicht gefunden.")
            else:
                print(f"Aktuelle Rolle: {detected_role}")
                if detected_bereich:
                    print(f"Aktueller Bereich: {detected_bereich}")

                new_username = input("Neuer Benutzername (leer lassen für keine Änderung): ").strip() or None
                new_password = input("Neues Passwort (leer lassen für keine Änderung): ").strip() or None

                # Neue Rolle setzen, aber wenn leer bleibt die alte
                new_role = input("Neue Rolle (leer lassen für keine Änderung): ").strip() or detected_role

                # Falls die neue Rolle Kassenwart ist, kann der Bereich geändert werden
                new_bereich = None
                if new_role == "Kassenwart":
                    new_bereich = input("Neuer Bereich (leer lassen für aktuellen Bereich): ").strip() or detected_bereich

                print(manager.edit_user(username, new_username, new_password, new_role, new_bereich))
        
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
