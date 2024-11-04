import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

class AnalyseDonnees:
    def __init__(self, db_path='viticulture.db'):
        self.db_path = db_path

    def connexion_db(self):
        return sqlite3.connect(self.db_path)

    def analyser_donnees_annuelles(self):
        conn = self.connexion_db()
        travaux_df = pd.read_sql_query('''
            SELECT o.nom AS operation, t.heures AS duree
            FROM temps_travail t
            JOIN operations o ON t.operation_id = o.id
        ''', conn)
        conn.close()
        
        # Calcul de la somme des durées par opération
        synthese = travaux_df.groupby('operation')['duree'].sum()
        
        # Sauvegarder la synthèse sous forme de CSV
        synthese.to_csv("synthese_annuelle_travaux.csv")
        return synthese

    def afficher_synthese_annuelle(self):
        synthese = self.analyser_donnees_annuelles()
        
        # Créer une fenêtre Tkinter pour afficher les données
        root = tk.Toplevel()
        root.title("Synthèse Annuelle des Travaux")
        root.geometry("400x300")
        
        # Création d'un Treeview pour afficher les résultats
        tree = ttk.Treeview(root, columns=("operation", "duree"), show="headings")
        tree.heading("operation", text="Opération")
        tree.heading("duree", text="Durée Totale (heures)")
        
        # Insérer les données de synthèse dans le Treeview
        for operation, duree in synthese.items():
            tree.insert("", "end", values=(operation, duree))
        
        tree.pack(expand=True, fill="both")
        
        # Bouton pour fermer la fenêtre
        tk.Button(root, text="Fermer", command=root.destroy).pack(pady=10)
        root.mainloop()

    def afficher_graphique_synthese(self):
        synthese = self.analyser_donnees_annuelles()
        
        # Création d'un graphique en barres
        plt.figure(figsize=(10, 6))
        synthese.plot(kind="bar", color="skyblue")
        plt.title("Synthèse Annuelle des Temps de Travaux par Opération")
        plt.xlabel("Opération")
        plt.ylabel("Durée Totale (heures)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
