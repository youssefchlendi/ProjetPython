import smtplib
import sqlite3
from email.mime.text import MIMEText
from tkinter import messagebox
import tkinter as tk

def obtenir_email_config():
    conn = sqlite3.connect('viticulture.db')
    c = conn.cursor()
    # Récupérer l'email et le mot de passe pour l'id 1
    c.execute("SELECT email, password FROM email_settings WHERE id = 1")
    result = c.fetchone()
    conn.close()
    
    if result:
        email, password = result  # Décompose le tuple en deux variables
        print(f"Email récupéré : {email}")
        print(f"Mot de passe récupéré : {password}")  # Afficher le mot de passe dans la console
    else:
        email, password = None, None  # Valeurs par défaut si aucune donnée n'est trouvée
    
    return email, password

# Fonction pour envoyer une notification par email
def envoyer_notification(destinataires):
    # Récupérer l'email et le mot de passe de l'expéditeur
    email, password = obtenir_email_config()
    if not email or not password:
        messagebox.showerror("Erreur", "L'email ou le mot de passe de l'expéditeur n'est pas configuré.")
        return

    # Préparation du message
    msg = MIMEText("La saisie mensuelle a été effectuée.")
    msg['Subject'] = "Notification de saisie"
    msg['From'] = email
    msg['To'] = ", ".join(destinataires)

    try:
        # Connexion sécurisée au serveur SMTP de Gmail
        with smtplib.SMTP('smtp.gmail.com', 465) as server:
            server.login(email, password)  # Utilisation du mot de passe d'application spécifique
            server.sendmail(email, destinataires, msg.as_string())
        messagebox.showinfo("Succès", "Notification envoyée.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'envoi de l'email : {e}")

# Interface pour envoyer une notification
def interface_envoi_notification():
    root = tk.Tk()
    root.title("Envoi de Notification")
    root.geometry("400x200")

    tk.Label(root, text="Emails des destinataires (séparés par des virgules)").pack(pady=10)
    destinataires_entry = tk.Entry(root, width=50)
    destinataires_entry.pack(pady=5)

    def envoyer():
        destinataires_text = destinataires_entry.get().strip()
        if not destinataires_text:
            messagebox.showerror("Erreur", "Veuillez entrer au moins un email destinataire.")
            return
        
        # Transformer la chaîne en liste d'emails
        destinataires = [email.strip() for email in destinataires_text.split(",") if email.strip()]
        envoyer_notification(destinataires)

    tk.Button(root, text="Envoyer Notification", command=envoyer).pack(pady=20)
    root.mainloop()

# Lancer l'interface d'envoi de notification
if __name__ == "__main__":
    interface_envoi_notification()
