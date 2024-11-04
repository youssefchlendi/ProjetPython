import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Fonction pour enregistrer le temps de travail
def enregistrer_temps(employe_id, operation_id, heures):
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute("INSERT INTO temps_travail (employe_id, operation_id, heures) VALUES (?, ?, ?)", (employe_id, operation_id, heures))
        conn.commit()
        messagebox.showinfo("Succès", "Temps de travail enregistré.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
    finally:
        if conn:
            conn.close()

# Interface pour la saisie des temps
def interface_saisie_temps():
    root = tk.Toplevel()  # Utiliser Toplevel pour garder la fenêtre principale active
    root.title("Saisie des Temps de Travail")

    tk.Label(root, text="ID Employé").grid(row=0, column=0)
    employe_id = tk.Entry(root)
    employe_id.grid(row=0, column=1)

    tk.Label(root, text="ID Opération").grid(row=1, column=0)
    operation_id = tk.Entry(root)
    operation_id.grid(row=1, column=1)

    tk.Label(root, text="Heures").grid(row=2, column=0)
    heures = tk.Entry(root)
    heures.grid(row=2, column=1)

    def sauvegarder():
        # Vérification des champs vides
        if not employe_id.get().strip():
            messagebox.showerror("Erreur", "Le champ 'ID Employé' est obligatoire.")
            return
        if not operation_id.get().strip():
            messagebox.showerror("Erreur", "Le champ 'ID Opération' est obligatoire.")
            return
        if not heures.get().strip():
            messagebox.showerror("Erreur", "Le champ 'Heures' est obligatoire.")
            return

        try:
            # Conversion en int pour les ID et en float pour les heures
            employe_id_val = int(employe_id.get())
            operation_id_val = int(operation_id.get())
            heures_val = float(heures.get())
            
            # Vérification de la plage de valeur pour les heures
            if heures_val <= 0 or heures_val > 24:
                messagebox.showerror("Erreur", "Le champ 'Heures' doit être un nombre positif et ne pas dépasser 24.")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les champs 'ID Employé', 'ID Opération' et 'Heures'.")
            return

        # Enregistrement des données dans la base de données
        enregistrer_temps(employe_id_val, operation_id_val, heures_val)
        root.destroy()

    tk.Button(root, text="Enregistrer", command=sauvegarder).grid(row=3, column=1)
    root.mainloop()

# Lancer l'interface
if __name__ == "__main__":
    interface_saisie_temps()
