from fpdf import FPDF
import sqlite3
from tkinter import messagebox
import tkinter as tk
import os

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Fonction pour générer le rapport PDF
def generer_rapport():
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute('''SELECT e.nom, o.nom, t.heures FROM temps_travail t
                     JOIN employes e ON t.employe_id = e.id
                     JOIN operations o ON t.operation_id = o.id''')
        result = c.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {e}")
        return
    finally:
        if conn:
            conn.close()

    if not result:
        messagebox.showinfo("Information", "Aucune donnée disponible pour générer le rapport.")
        return

    try:
        # Création du PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport Mensuel des Travaux", ln=True, align='C')

        # Remplir le PDF avec les données
        for row in result:
            pdf.cell(200, 10, txt=f"Employé: {row[0]}, Opération: {row[1]}, Heures: {row[2]}", ln=True)

        # Définir le chemin de sauvegarde du fichier PDF
        output_path = os.path.join(os.getcwd(), "rapport_mensuel.pdf")
        pdf.output(output_path)
        messagebox.showinfo("Succès", f"Rapport généré avec succès sous le nom '{output_path}'.")

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {e}")

# Interface pour déclencher la génération du rapport
def interface_generer_rapport():
    root = tk.Toplevel()  # Utilisation de Toplevel pour éviter de fermer l'application principale
    root.title("Génération de Rapport")

    tk.Button(root, text="Générer Rapport Mensuel", command=generer_rapport).pack(pady=20)
    root.geometry("300x150")
    root.mainloop()

# Lancer l'interface pour la génération des rapports
if __name__ == "__main__":
    interface_generer_rapport()
