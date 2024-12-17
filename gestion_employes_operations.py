import threading
import tkinter as tk
from tkinter import messagebox
import sqlite3

from deep_learning.regression_model import train_work_hours_regression

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Interface pour ajouter un employé
def interface_creer_employe():
    root = tk.Toplevel()
    root.title("Créer un Employé")

    tk.Label(root, text="Nom de l'employé").grid(row=0, column=0)
    nom_entry = tk.Entry(root)
    nom_entry.grid(row=0, column=1)

    tk.Label(root, text="Poste de l'employé").grid(row=1, column=0)
    poste_entry = tk.Entry(root)
    poste_entry.grid(row=1, column=1)

    def ajouter_employe():
        nom = nom_entry.get().strip()
        poste = poste_entry.get().strip()

        # Vérification des champs vides
        if not nom:
            messagebox.showerror("Erreur", "Le champ 'Nom de l'employé' est obligatoire.")
            return
        if not poste:
            messagebox.showerror("Erreur", "Le champ 'Poste de l'employé' est obligatoire.")
            return

        try:
            # Enregistrement dans la base de données
            conn = connexion_db()
            c = conn.cursor()
            c.execute("INSERT INTO employes (nom, poste) VALUES (?, ?)", (nom, poste))
            conn.commit()
            messagebox.showinfo("Succès", "Employé ajouté avec succès.")
            root.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()

    tk.Button(root, text="Ajouter Employé", command=ajouter_employe).grid(row=2, column=1)
    root.mainloop()

# Interface pour ajouter une opération
def interface_creer_operation():
    root = tk.Toplevel()
    root.title("Créer une Opération")

    tk.Label(root, text="Nom de l'opération").grid(row=0, column=0)
    nom_entry = tk.Entry(root)
    nom_entry.grid(row=0, column=1)

    tk.Label(root, text="Type d'opération").grid(row=1, column=0)
    type_entry = tk.Entry(root)
    type_entry.grid(row=1, column=1)

    def ajouter_operation():
        nom = nom_entry.get().strip()
        type_operation = type_entry.get().strip()

        # Vérification des champs vides
        if not nom:
            messagebox.showerror("Erreur", "Le champ 'Nom de l'opération' est obligatoire.")
            return
        if not type_operation:
            messagebox.showerror("Erreur", "Le champ 'Type d'opération' est obligatoire.")
            return

        try:
            # Enregistrement dans la base de données
            conn = connexion_db()
            c = conn.cursor()
            c.execute("INSERT INTO operations (nom, type) VALUES (?, ?)", (nom, type_operation))
            conn.commit()
            threading.Thread(target=train_work_hours_regression).start()        
            messagebox.showinfo("Succès", "Opération ajoutée avec succès.")
            root.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()

    tk.Button(root, text="Ajouter Opération", command=ajouter_operation).grid(row=2, column=1)
    root.mainloop()
