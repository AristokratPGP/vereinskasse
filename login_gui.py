import tkinter as tk
from tkinter import messagebox
from login_backend import load_users, hash_password

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    users = load_users()
    
    if username in users and users[username].password_hash == hash_password(password):
        messagebox.showinfo("Login Erfolgreich", f"Willkommen, {username}! Rolle: {users[username].role}")
    else:
        messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort")

def create_login_gui():
    global entry_username, entry_password
    
    root = tk.Tk()
    root.title("Vereinskassen-System Login")
    root.geometry("300x200")
    
    tk.Label(root, text="Benutzername:").pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)
    
    tk.Label(root, text="Passwort:").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)
    
    tk.Button(root, text="Login", command=login).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_login_gui()




