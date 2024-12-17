import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
from deep_learning.supervised_learning import train_and_save_model
import threading
# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')
  
def obtenir_operations():
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute("SELECT id, nom FROM operations")  # Sélectionne l'id et le nom de chaque opération
        result = c.fetchall()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
        return []
    finally:
        if conn:
            conn.close()
            
def obtenir_employes():
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute("SELECT id, nom FROM employes")  # Sélectionne l'id et le nom de chaque employé
        result = c.fetchall()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
        return []
    finally:
        if conn:
            conn.close()

# Enregistrement de l'opération phytosanitaire
def enregistrer_phytosanitaire(employe_id, operation_id, maladie, stade, methode, observation):
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute('''INSERT INTO phytosanitaires (employe_id, operation_id, maladie, stade, methode, observation) 
                     VALUES (?, ?, ?, ?, ?, ?)''', (employe_id, operation_id, maladie, stade, methode, observation))
        conn.commit()
        # call train_and_save_model in a separate thread to avoid blocking the UI
        threading.Thread(target=train_and_save_model).start()        
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

    # Récupérer les employés et les opérations depuis la base de données
    employes = obtenir_employes()  # Liste des employés
    operations = obtenir_operations()  # Liste des opérations, à définir ci-dessous

    tk.Label(root, text="ID Employé").grid(row=0, column=0)
    employe_combobox = ttk.Combobox(root, values=[f"{emp[1]} ({emp[0]})" for emp in employes])  # Affiche le nom et l'id
    employe_combobox.grid(row=0, column=1)

    tk.Label(root, text="ID Opération").grid(row=1, column=0)
    operation_combobox = ttk.Combobox(root, values=[op[1] for op in operations])  # Liste des opérations
    operation_combobox.grid(row=1, column=1)

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
            if not employe_combobox.get().strip():
                raise ValueError("Le champ 'ID Employé' est obligatoire.")
            if not operation_combobox.get().strip():
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
            employe_id_val = int(employes[employe_combobox.current()][0])
            operation_id_val = int(operations[operation_combobox.current()][0])

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
