import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Enregistrement de l'opération phytosanitaire
def enregistrer_phytosanitaire(employe_id, operation_id, maladie, stade, methode, observation):
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute('''INSERT INTO phytosanitaires (employe_id, operation_id, maladie, stade, methode, observation) 
                     VALUES (?, ?, ?, ?, ?, ?)''', (employe_id, operation_id, maladie, stade, methode, observation))
        conn.commit()
        messagebox.showinfo("Succès", "Opération phytosanitaire enregistrée.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite lors de l'enregistrement : {e}")
    finally:
        if conn:
            conn.close()

# Interface pour la saisie des opérations phytosanitaires
def interface_phytosanitaire():
    root = tk.Toplevel()  # Utilisation de Toplevel pour éviter de fermer la fenêtre principale
    root.title("Saisie des Opérations Phytosanitaires")

    # Champs de saisie
    tk.Label(root, text="ID Employé").grid(row=0, column=0)
    employe_id = tk.Entry(root)
    employe_id.grid(row=0, column=1)

    tk.Label(root, text="ID Opération").grid(row=1, column=0)
    operation_id = tk.Entry(root)
    operation_id.grid(row=1, column=1)

    tk.Label(root, text="Maladie").grid(row=2, column=0)
    maladie = tk.Entry(root)
    maladie.grid(row=2, column=1)

    tk.Label(root, text="Stade").grid(row=3, column=0)
    stade = tk.Entry(root)
    stade.grid(row=3, column=1)

    tk.Label(root, text="Méthode").grid(row=4, column=0)
    methode = tk.Entry(root)
    methode.grid(row=4, column=1)

    tk.Label(root, text="Observation").grid(row=5, column=0)
    observation = tk.Entry(root)
    observation.grid(row=5, column=1)

    # Fonction de sauvegarde avec validation
    def sauvegarder_phytosanitaire():
        try:
            # Vérification des champs vides
            if not employe_id.get().strip():
                raise ValueError("Le champ 'ID Employé' est obligatoire.")
            if not operation_id.get().strip():
                raise ValueError("Le champ 'ID Opération' est obligatoire.")
            if not maladie.get().strip():
                raise ValueError("Le champ 'Maladie' est obligatoire.")
            if not stade.get().strip():
                raise ValueError("Le champ 'Stade' est obligatoire.")
            if not methode.get().strip():
                raise ValueError("Le champ 'Méthode' est obligatoire.")
            if not observation.get().strip():
                raise ValueError("Le champ 'Observation' est obligatoire.")
            
            # Validation des types
            employe_id_val = int(employe_id.get())
            operation_id_val = int(operation_id.get())

            # Enregistrement si toutes les validations sont réussies
            enregistrer_phytosanitaire(employe_id_val, operation_id_val, maladie.get(), stade.get(), methode.get(), observation.get())
            root.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except sqlite3.Error as db_error:
            messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite lors de l'enregistrement : {db_error}")

    tk.Button(root, text="Enregistrer", command=sauvegarder_phytosanitaire).grid(row=6, column=1)
    root.mainloop()

# Lancer l'interface pour les opérations phytosanitaires
if __name__ == "__main__":
    interface_phytosanitaire()
