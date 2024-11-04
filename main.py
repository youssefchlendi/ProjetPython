import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import messagebox
from temps import interface_saisie_temps
from phytosanitaires import interface_phytosanitaire
from reports import interface_generer_rapport
from notifications import envoyer_notification
from initialisation_db import creer_db
from gestion_employes_operations import interface_creer_employe, interface_creer_operation
from EmailConfig import interface_email_config  # Importer correctement depuis EmailConfig.py
import sqlite3
from analyse import AnalyseDonnees  # Importer la classe AnalyseDonnees

 
def connexion_db():
    return sqlite3.connect('viticulture.db')

def consulter_donnees(table_name, columns):
    root = tk.Toplevel()
    root.title(f"Consultation de la Table {table_name}")
    
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(expand=True, fill="both")
    
    # Récupérer les données de la table
    conn = connexion_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    
    # Insérer les données dans le Treeview
    for row in rows:
        tree.insert("", "end", values=row)
    
    root.mainloop()
# Fonction pour ouvrir l'interface de configuration de l'email
def ouvrir_interface_email_config():
    interface_email_config()  # Appelle la fonction depuis EmailConfig.py

analyse_donnees = AnalyseDonnees()

# Fonction principale pour créer la fenêtre avec le menu
def main():
    root = tk.Tk()
    root.title("Application de Gestion en Viticulture")
    root.geometry("600x400")
    
    tk.Label(root, text="Bienvenue dans le système de gestion de viticulture", font=("Helvetica", 16)).pack(pady=20)

    # Menu principal
    menu_bar = tk.Menu(root)

    # Menu Gestion
    menu_gestion = tk.Menu(menu_bar, tearoff=0)
    menu_gestion.add_command(label="Créer un Employé", command=interface_creer_employe)
    menu_gestion.add_command(label="Créer une Opération", command=interface_creer_operation)
    menu_gestion.add_command(label="Quitter", command=root.quit)
    menu_bar.add_cascade(label="Gestion", menu=menu_gestion)

    # Menu Consultation
    menu_consultation = tk.Menu(menu_bar, tearoff=0)
    menu_consultation.add_command(label="Consulter Employés", command=lambda: consulter_donnees("employes", ["id", "nom", "poste"]))
    menu_consultation.add_command(label="Consulter Opérations", command=lambda: consulter_donnees("operations", ["id", "nom", "type"]))
    menu_consultation.add_command(label="Consulter Temps de Travail", command=lambda: consulter_donnees("temps_travail", ["id", "employe_id", "operation_id", "heures"]))
    menu_consultation.add_command(label="Consulter Phytosanitaires", command=lambda: consulter_donnees("phytosanitaires", ["id", "employe_id", "operation_id", "maladie", "stade", "methode", "observation", "application_date"]))
    menu_bar.add_cascade(label="Consultation", menu=menu_consultation)

    # Menu Travail
    menu_travail = tk.Menu(menu_bar, tearoff=0)
    menu_travail.add_command(label="Saisie des Temps de Travail", command=interface_saisie_temps)
    menu_travail.add_command(label="Enregistrement Opérations Phytosanitaires", command=interface_phytosanitaire)
    menu_bar.add_cascade(label="Travail", menu=menu_travail)

    # Menu Rapports
    menu_rapport = tk.Menu(menu_bar, tearoff=0)
    menu_rapport.add_command(label="Générer Rapport Mensuel", command=interface_generer_rapport)
    menu_bar.add_cascade(label="Rapports", menu=menu_rapport)

    # Menu Notifications
    menu_notification = tk.Menu(menu_bar, tearoff=0)
    menu_notification.add_command(label="Envoyer Notification de Saisie", command=lambda: envoyer_notification(["exemple@mail.com"]))
    menu_notification.add_command(label="Configuration Email", command=interface_email_config)
    menu_bar.add_cascade(label="Notifications", menu=menu_notification)

    # Nouveau Menu Analyse
    menu_analyse = tk.Menu(menu_bar, tearoff=0)
    menu_analyse.add_command(label="Synthèse Annuelle des Travaux", command=analyse_donnees.afficher_synthese_annuelle)
    menu_analyse.add_command(label="Afficher Graphique des Travaux", command=analyse_donnees.afficher_graphique_synthese)
    menu_bar.add_cascade(label="Analyse", menu=menu_analyse)

    # Configurer le menu
    root.config(menu=menu_bar)
    root.mainloop()

# Lancer l'application principale
if __name__ == "__main__":
    main()