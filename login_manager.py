import json
from http.server import BaseHTTPRequestHandler
from user_manager import UserManager



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            
            username = data.get("username")
            password = data.get("password")
            print(f"Empfangene Login-Daten: Benutzername={username}, Passwort={password}")
            
            users = UserManager.load_users()
            
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