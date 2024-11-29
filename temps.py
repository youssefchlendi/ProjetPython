import tkinter as tk
from tkinter import messagebox,ttk
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

# Interface pour la saisie des temps
def interface_saisie_temps():
    root = tk.Toplevel()  # Utiliser Toplevel pour garder la fenêtre principale active
    root.title("Saisie des Temps de Travail")
    
    # Récupérer les employés et les opérations depuis la base de données
    employes = obtenir_employes()  # Liste des employés
    operations = obtenir_operations()  # Liste des opérations, à définir ci-dessous

    tk.Label(root, text="ID Employé").grid(row=0, column=0)
    employe_combobox = ttk.Combobox(root, values=[f"{emp[1]} ({emp[0]})" for emp in employes])  # Affiche le nom et l'id
    employe_combobox.grid(row=0, column=1)

    tk.Label(root, text="ID Opération").grid(row=1, column=0)
    operation_combobox = ttk.Combobox(root, values=[op[1] for op in operations])  # Liste des opérations
    operation_combobox.grid(row=1, column=1)

    tk.Label(root, text="Heures travaillées").grid(row=2, column=0)
    heures_entry = tk.Entry(root)
    heures_entry.grid(row=2, column=1)
    
    def sauvegarder():
        employe_id = employes[employe_combobox.current()][0]  # Récupère l'id de l'employé
        operation_id = operations[operation_combobox.current()][0]  # Récupère l'id de l'opération
        heures = heures_entry.get().strip()
        if not employe_id or not operation_id or not heures:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        try:
            # Conversion en int pour les ID et en float pour les heures
            employe_id_val = int(employe_id)
            operation_id_val = int(operation_id)
            heures_val = float(heures)
            
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
