import sqlite3
import tkinter as tk
from tkinter import messagebox

def mettre_a_jour_email_config(email, password):
    conn = sqlite3.connect('viticulture.db')
    c = conn.cursor()
    # Supprimer les anciennes configurations si elles existent
    c.execute("DELETE FROM email_settings")
    # Insérer les nouvelles configurations
    c.execute("INSERT INTO email_settings (id, email, password) VALUES (1, ?, ?)", (email, password))
    conn.commit()
    conn.close()

def interface_email_config():
    root = tk.Tk()
    root.title("Configuration de l'Email")
    root.geometry("400x200")

    tk.Label(root, text="Adresse Email").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Mot de Passe").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def sauvegarder():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse email et un mot de passe.")
            return

        mettre_a_jour_email_config(email, password)
        messagebox.showinfo("Succès", "Configuration de l'email mise à jour.")
        root.destroy()

    tk.Button(root, text="Sauvegarder", command=sauvegarder).grid(row=2, column=1, pady=20)
    root.mainloop()

# Tester l'interface de configuration en exécutant le fichier directement
if __name__ == "__main__":
    interface_email_config()
