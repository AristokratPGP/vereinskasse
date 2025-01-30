import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

CSV_FILE = "users.csv"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

def load_users():
    users = {}
    print("Lade Benutzer aus CSV-Datei...")
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Header überspringen
            for row in reader:
                username, password, role = row
                users[username] = User(username, password, role)
        print("Benutzer erfolgreich geladen:", users.keys())
    except FileNotFoundError:
        print("Fehler: CSV-Datei nicht gefunden.")
    return users

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            
            username = data.get("username")
            password = data.get("password")
            print(f"Empfangene Login-Daten: Benutzername={username}, Passwort={password}")
            
            users = load_users()
            
            if username in users and users[username].password == password:
                response = {"message": "Login erfolgreich", "role": users[username].role}
                self.send_response(200)
                print("Login erfolgreich für Benutzer:", username)
            else:
                response = {"message": "Ungültige Zugangsdaten"}
                self.send_response(401)
                print("Login fehlgeschlagen für Benutzer:", username)
            
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))