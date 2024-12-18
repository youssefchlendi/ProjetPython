import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Connexion à la base de données
def connexion_db():
    return sqlite3.connect('viticulture.db')

# Interface pour ajouter un employé
def interface_creer_maladie():
    root = tk.Toplevel()
    root.title("Créer une Maladie")

    tk.Label(root, text="Nom de la maladie").grid(row=0, column=0)
    nom_entry = tk.Entry(root)
    nom_entry.grid(row=0, column=1)

    tk.Label(root, text="Gravité de la maladie").grid(row=1, column=0)
    gravity_entry = ttk.Combobox(root, values=["mild", "moderate", "severe"])
    gravity_entry.grid(row=1, column=1)

    def ajouter_maladie():
        nom = nom_entry.get().strip()
        gravity = gravity_entry.get().strip()

        # Vérification des champs vides
        if not nom:
            messagebox.showerror("Erreur", "Le champ 'Nom de la maladie' est obligatoire.")
            return
        if not gravity:
            messagebox.showerror("Erreur", "Le champ 'Gravité de la maladie' est obligatoire.")
            return
        if gravity not in ["mild", "moderate", "severe"]:
            messagebox.showerror("Erreur", "La gravité de la maladie doit être 'mild', 'moderate', ou 'severe'.")
            return

        try:
            # Enregistrement dans la base de données
            conn = connexion_db()
            c = conn.cursor()
            c.execute("INSERT INTO maladies (nom, gravite) VALUES (?, ?)", (nom, gravity))
            conn.commit()
            messagebox.showinfo("Succès", "Maladie ajoutée avec succès.")
            root.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()

    tk.Button(root, text="Ajouter Maladie", command=ajouter_maladie).grid(row=2, column=1)
    root.mainloop()

# Interface pour rechercher et afficher les maladies
def interface_rechercher_maladie():
 
    # show treeview with maladies, and a search bar to search for maladies
    root = tk.Toplevel()
    root.title("Rechercher une Maladie")
    
    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=["id", "nom", "gravite"], show='headings')
    tree.heading("id", text="ID")
    tree.heading("nom", text="Nom")
    tree.heading("gravite", text="Gravité")
    tree.column("id", anchor="center")
    tree.column("nom", anchor="center")
    tree.column("gravite", anchor="center")
    tree.pack(expand=True, fill="both")
    
    # Create a search bar
    search_var = tk.StringVar()
    search_entry = ttk.Entry(root, textvariable=search_var)
    search_entry.pack()
    
    def search_maladies():
        search_term = search_var.get()
        conn = connexion_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM maladies WHERE nom LIKE ?", (f"%{search_term}%",))
        rows = cursor.fetchall()
        conn.close()
        
        # Clear the treeview
        tree.delete(*tree.get_children())
        
        # Insert the search results into the treeview
        for row in rows:
            tree.insert("", "end", values=row)
            
    search_button = ttk.Button(root, text="Rechercher", command=search_maladies)
    search_button.pack()
    
    search_maladies()
    
    root.mainloop()