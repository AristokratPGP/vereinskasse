import tkinter as tk
from tkinter import messagebox
import subprocess  # Für das Starten der Admin-GUI
from login_backend import load_users



# Login-Funktion
def login():
    username = entry_username.get()
    password = entry_password.get()
    users = load_users()

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        messagebox.showinfo("Login Erfolgreich", f"Willkommen, {username}!\nRolle: {role}")
        root.destroy()  # Schließt das Login-Fenster

        # 💡 Öffne die passende GUI nach erfolgreichem Login
        if role == "Administrator":
            subprocess.Popen(["python", "admin_gui.py"], shell=True)  # Startet das Admin-Dashboard
        elif role == "Kassenwart":
            subprocess.Popen(["python", "kassenwart_gui.py"], shell=True)
        elif role == "Referent-Finanzen":
            subprocess.Popen(["python", "finanzen_gui.py"], shell=True)
        else:
            messagebox.showerror("Fehler", "Unbekannte Rolle!")
    else:
        messagebox.showerror("Login Fehlgeschlagen", "Falscher Benutzername oder Passwort!")


# GUI erstellen
root = tk.Tk()
root.title("Login - Vereinskassen-System")
root.geometry("300x200")

tk.Label(root, text="Benutzername:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Passwort:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()




