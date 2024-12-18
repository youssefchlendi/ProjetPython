import sqlite3

def creer_db():
    try:
        conn = sqlite3.connect('viticulture.db')
        c = conn.cursor()

        # Création de la table Employés
        c.execute('''CREATE TABLE IF NOT EXISTS employes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        poste TEXT NOT NULL
                    )''')
        
        # Création de la table Opérations
        c.execute('''CREATE TABLE IF NOT EXISTS operations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        type TEXT NOT NULL
                    )''')
        
        # Création de la table Temps de Travail
        c.execute('''CREATE TABLE IF NOT EXISTS temps_travail (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employe_id INTEGER NOT NULL,
                        operation_id INTEGER NOT NULL,
                        heures REAL NOT NULL,
                        FOREIGN KEY (employe_id) REFERENCES employes(id) ON DELETE CASCADE,
                        FOREIGN KEY (operation_id) REFERENCES operations(id) ON DELETE CASCADE
                    )''')
        
        # Création de la table Phytosanitaires
        c.execute('''CREATE TABLE IF NOT EXISTS phytosanitaires (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employe_id INTEGER NOT NULL,
                        operation_id INTEGER NOT NULL,
                        maladie TEXT,
                        stade TEXT,
                        methode TEXT,
                        observation TEXT,
                        application_date DATE DEFAULT CURRENT_DATE,
                        FOREIGN KEY (employe_id) REFERENCES employes(id) ON DELETE CASCADE,
                        FOREIGN KEY (operation_id) REFERENCES operations(id) ON DELETE CASCADE
                    )''')
        # Création de la table Phytosanitaires

        c.execute('''CREATE TABLE IF NOT EXISTS email_settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
        
        # Création de la table Maladies
        # Ce table contient 3 colonnes : id, nom, et gravite la gravité de la maladie peut être "mild", "moderate", ou "severe"
        c.execute('''CREATE TABLE IF NOT EXISTS maladies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        gravite TEXT NOT NULL
                    )''')
        
        # Commit des changements
        conn.commit()
        print("Base de données initialisée avec succès, y compris la table de configuration d'email.")

    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")
    
    finally:
        if conn:
            conn.close()

# Exécuter l'initialisation
if __name__ == "__main__":
    creer_db()
