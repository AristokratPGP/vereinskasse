import json
import os
import datetime
from typing import List, Dict

class Konto:
    """Repräsentiert ein Abteilungskonto mit Saldo und Transaktionen."""

    def __init__(self, abteilung: str, saldo: float = 0.0, transaktionen=None):
        self.abteilung = abteilung
        self.saldo = saldo
        self.transaktionen = transaktionen if transaktionen else []

    def to_dict(self) -> Dict:
        """Gibt das Konto als Dictionary zurück."""
        return {
            "saldo": self.saldo,
            "transaktionen": self.transaktionen
        }

    def __repr__(self):
        return f"Konto(abteilung={self.abteilung}, saldo={self.saldo}, transaktionen={len(self.transaktionen)})"


class Transaktion:
    """Repräsentiert eine Transaktion für ein Konto."""

    def __init__(self, konto: str, typ: str, betrag: float, quelle: str, notiz: str = "", zielkonto: str = None):
        self.konto = konto
        self.typ = typ
        self.betrag = betrag
        self.quelle = quelle
        self.notiz = notiz
        self.zielkonto = zielkonto
        self.datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Gibt die Transaktion als Dictionary zurück."""
        return {
            "datum": self.datum,
            "konto": self.konto,
            "typ": self.typ,
            "betrag": self.betrag,
            "quelle": self.quelle,
            "notiz": self.notiz,
            "zielkonto": self.zielkonto,
        }

    def __repr__(self):
        return f"Transaktion({self.typ}, {self.betrag}€, {self.konto} -> {self.zielkonto if self.zielkonto else '-'})"


class AccountManager:
    """Verwaltet Konten und Transaktionen über die JSON-Datei."""

    JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Lädt die Konten und Transaktionen aus der JSON-Datei."""
        print("[DEBUG] Lade Daten aus JSON...")
        try:
            with open(AccountManager.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[DEBUG] Fehler: JSON-Datei nicht gefunden oder ungültig. Neue Datei wird erstellt.")
            return {"konten": {}, "users": {}}

    def save_data(self):
        """Speichert die Daten in die JSON-Datei."""
        print("[DEBUG] Speichere Daten in JSON...")
        with open(AccountManager.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def create_account(self, name: str) -> Dict:
        """Erstellt ein neues Abteilungskonto."""
        print(f"[DEBUG] Erstelle Konto: {name}")

        if name in self.data["konten"]:
            return {"error": f"Konto '{name}' existiert bereits."}

        self.data["konten"][name] = {"saldo": 0, "transaktionen": []}
        self.save_data()
        return {"success": f"Konto '{name}' erfolgreich erstellt."}

    def delete_account(self, name: str) -> Dict:
        """Löscht ein Konto, wenn der Saldo null ist."""
        print(f"[DEBUG] Lösche Konto: {name}")

        if name not in self.data["konten"]:
            return {"error": f"Konto '{name}' existiert nicht."}

        if self.data["konten"][name]["saldo"] > 0:
            return {"error": f"Konto '{name}' hat noch Guthaben und kann nicht gelöscht werden."}

        del self.data["konten"][name]
        self.save_data()
        return {"success": f"Konto '{name}' erfolgreich gelöscht."}

    def deposit(self, name: str, amount: float, quelle: str, notiz: str = "") -> Dict:
        """Zahlt Geld auf ein Konto ein."""
        print(f"[DEBUG] Einzahlung: {amount}€ auf '{name}'")

        if name not in self.data["konten"]:
            return {"error": f"Konto '{name}' existiert nicht."}
        
        if amount <= 0:
            return {"error": "Betrag muss positiv sein."}

        self.data["konten"][name]["saldo"] += amount
        transaction = Transaktion(name, "Einzahlung", amount, quelle, notiz).to_dict()
        self.data["konten"][name]["transaktionen"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ auf '{name}' eingezahlt.", "transaction": transaction}

    def withdraw(self, name: str, amount: float, notiz: str = "") -> Dict:
        """Hebt Geld von einem Konto ab."""
        print(f"[DEBUG] Auszahlung: {amount}€ von '{name}'")

        if name not in self.data["konten"]:
            return {"error": f"Konto '{name}' existiert nicht."}

        if amount <= 0:
            return {"error": "Betrag muss positiv sein."}

        if self.data["konten"][name]["saldo"] < amount:
            return {"error": "Nicht genügend Guthaben."}

        self.data["konten"][name]["saldo"] -= amount
        transaction = Transaktion(name, "Auszahlung", amount, "Konto", notiz).to_dict()
        self.data["konten"][name]["transaktionen"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ von '{name}' ausgezahlt.", "transaction": transaction}

    def get_transaction_history(self, name: str) -> List[Dict]:
        """Gibt die Transaktionshistorie eines Kontos zurück."""
        print(f"[DEBUG] Lade Transaktionshistorie für Konto: {name}")

        if name not in self.data["konten"]:
            return {"error": f"Konto '{name}' existiert nicht."}

        return self.data["konten"][name]["transaktionen"]

    def transfer(self, from_account: str, to_account: str, amount: float, notiz: str = "") -> Dict:
        """Überweist Geld zwischen zwei Konten."""
        print(f"[DEBUG] Überweisung: {amount}€ von '{from_account}' nach '{to_account}'")

        if from_account not in self.data["konten"] or to_account not in self.data["konten"]:
            return {"error": "Eines der Konten existiert nicht."}

        if amount <= 0:
            return {"error": "Betrag muss positiv sein."}

        if self.data["konten"][from_account]["saldo"] < amount:
            return {"error": "Nicht genügend Guthaben für die Überweisung."}

        self.data["konten"][from_account]["saldo"] -= amount
        self.data["konten"][to_account]["saldo"] += amount
        transaction = Transaktion(from_account, "Umbuchung", amount, "Intern", notiz, to_account).to_dict()
        self.data["konten"][from_account]["transaktionen"].append(transaction)
        self.data["konten"][to_account]["transaktionen"].append(transaction)
        self.save_data()
        return {"success": f"{amount}€ von '{from_account}' auf '{to_account}' überwiesen.", "transaction": transaction}

    def export_account_to_txt(self, name: str):
        """Speichert ein Konto mit Kontostand und Transaktionen in eine .txt-Datei."""
        print(f"[DEBUG] Exportiere Konto '{name}' nach .txt")

        if name not in self.data["konten"]:
            print(f"[ERROR] Konto '{name}' existiert nicht.")
            return

        konto = self.data["konten"][name]
        filename = f"{name}_konto.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Konto: {name}\n")
            file.write(f"Aktueller Kontostand: {konto['saldo']}€\n")
            file.write("\n--- Transaktionen ---\n")
            for t in konto["transaktionen"]:
                file.write(f"{t['datum']} | {t['typ']}: {t['betrag']}€ | Quelle: {t['quelle']} | Notiz: {t['notiz']} | Ziel: {t['zielkonto'] if t['zielkonto'] else '-'}\n")

        print(f"[DEBUG] Konto '{name}' wurde in '{filename}' gespeichert.")

    def get_all_accounts_summary(self):
        """Gibt eine Liste aller Vereinskonten mit aktuellem Kassenstand und die Gesamtsumme aller Konten aus."""
        print("[DEBUG] Erstelle Übersicht aller Vereinskonten...")

        if not self.data["konten"]:
            print("[ERROR] Keine Konten gefunden.")
            return {"error": "Keine Konten vorhanden."}

        total_sum = 0
        konten_list = []

        for name, konto in self.data["konten"].items():
            saldo = konto["saldo"]
            total_sum += saldo
            konten_list.append(f"{name}: {saldo}€")

        print(f"[DEBUG] Gesamtsumme aller Konten: {total_sum}€")

        return {
            "konten": konten_list,
            "gesamt_summe": total_sum
        }


def main():
    manager = AccountManager()

    print("\n### Konto erstellen ###")
    print(manager.create_account("Tanzen"))  # Erfolgreich
    print(manager.create_account("Tanzen"))  # Fehler: Konto existiert bereits

    print("\n### Geld einzahlen ###")
    print(manager.deposit("Tanzen", 200, "Mitgliedsbeitrag"))  # Erfolgreich
    print(manager.deposit("NichtVorhanden", 100, "Spende"))  # Fehler: Konto existiert nicht
    print(manager.deposit("Tanzen", -50, "Spende"))  # Fehler: Betrag negativ

    print("\n### Geld auszahlen ###")
    print(manager.withdraw("Tanzen", 50, "Trikots"))  # Erfolgreich
    print(manager.withdraw("Tanzen", 500, "Miete"))  # Fehler: Nicht genügend Guthaben
    print(manager.withdraw("NichtVorhanden", 10, "Test"))  # Fehler: Konto existiert nicht

    print("\n### Konto-Export testen ###")
    manager.export_account_to_txt("Tanzen")  # Erfolgreich
    manager.export_account_to_txt("NichtVorhanden")  # Fehler: Konto existiert nicht

    print("\n### Übersicht aller Konten ###")
    summary = manager.get_all_accounts_summary()
    print("\n".join(summary["konten"]))
    print(f"Gesamtsumme aller Konten: {summary['gesamt_summe']}€")

    print("\n### Konto löschen ###")
    print(manager.create_account("Testkonto"))
    print(manager.delete_account("Testkonto"))  # Erfolgreich
    print(manager.delete_account("Tanzen"))  # Fehler: Konto hat noch Guthaben


if __name__ == "__main__":
    main()

