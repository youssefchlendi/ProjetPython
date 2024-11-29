from fpdf import FPDF
import sqlite3
from tkinter import messagebox
import tkinter as tk
import os
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Fonction pour générer le rapport PDF
def generer_rapport():
    try:
        conn = connexion_db()
        c = conn.cursor()
        c.execute('''SELECT e.nom AS employe_nom, o.nom AS operation_nom, t.heures 
                     FROM temps_travail t
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
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Table of contents
        pdf.cell(200, 10, txt="Table des Matières", ln=True, align='C')
        pdf.ln(10)

        # Adding Table of Contents links
        toc = []
        toc.append(('Opération', pdf.page_no()))  # Dummy link for content sections

        # Split data by operation
        operations = {}
        for row in result:
            employe_nom, operation_nom, heures = row
            if operation_nom not in operations:
                operations[operation_nom] = []
            operations[operation_nom].append(row)
        
        # Add content to the report
        pdf.set_font("Arial", size=12)
        
        for i, (operation_nom, records) in enumerate(operations.items()):
            # Add Operation Header
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=f"Opération : {operation_nom}", ln=True, align='C')

            # Generate Table of Content for Operations
            toc.append((operation_nom, pdf.page_no()))

            # Generate the table for the current operation
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            for row in records:
                employe_nom, _, heures = row
                pdf.cell(200, 10, txt=f"Employé: {employe_nom}, Heures: {heures}", ln=True)
        
        # Second part: Group by Employee (Operator)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Par Employé", ln=True, align='C')

        # Group data by employee
        employees = {}
        for row in result:
            employe_nom, _, heures = row
            if employe_nom not in employees:
                employees[employe_nom] = []
            employees[employe_nom].append(row)

        # Generate content for Employees
        for employe_nom, records in employees.items():
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"Employé: {employe_nom}", ln=True)
            pdf.set_font("Arial", size=12)
            for row in records:
                _, operation_nom, heures = row
                pdf.cell(200, 10, txt=f"Opération: {operation_nom}, Heures: {heures}", ln=True)

        # Add Graphs to the report (e.g., bar chart for hours per operation)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Graphiques des Heures par Opération", ln=True, align='C')

        # Generate graph (hours per operation)
        # operations_hours = {}
        # for row in result:
        #     operation_nom, _, heures = row
        #     if operation_nom not in operations_hours:
        #         operations_hours[operation_nom] = 0
        #     operations_hours[operation_nom] += heures
        
        # # Plot graph
        # fig, ax = plt.subplots()
        # operations_list = list(operations_hours.keys())
        # heures_list = list(operations_hours.values())
        # ax.bar(operations_list, heures_list)

        # ax.set_xlabel("Opérations")
        # ax.set_ylabel("Heures Totales")
        # ax.set_title("Heures par Opération")

        # # Save the plot to a BytesIO object and embed in PDF
        # img_stream = BytesIO()
        # plt.savefig(img_stream, format='png')
        # img_stream.seek(0)
        # pdf.image(img_stream, x=10, y=30, w=190)

        # Save the PDF
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
