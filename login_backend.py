import csv
import hashlib
import secrets
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

CSV_FILE = "users.csv"

class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role

def load_users():
    users = {}
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Header überspringen
        for row in reader:
            username, password_hash, role = row
            users[username] = User(username, password_hash, role)
    return users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return secrets.token_hex(16)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            
            username = data.get("username")
            password = data.get("password")
            users = load_users()
            
            if username in users and users[username].password_hash == hash_password(password):
                token = generate_token()
                response = {"message": "Login erfolgreich", "token": token, "role": users[username].role}
                self.send_response(200)
            else:
                response = {"message": "Ungültige Zugangsdaten"}
                self.send_response(401)
            
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
