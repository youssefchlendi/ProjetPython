import sqlite3
from faker import Faker

# Initialize Faker and database connection
fake = Faker()
db = sqlite3.connect('viticulture.db')  # Replace with your actual database path
cursor = db.cursor()

# Seed employes Table
def seed_employes(n=50):
    for _ in range(n):
        nom = fake.name()
        poste = fake.job()
        cursor.execute("INSERT INTO employes (nom, poste) VALUES (?, ?)", (nom, poste))
    db.commit()
    print(f"{n} employes seeded successfully.")

# Seed operations Table
def seed_operations():
    if cursor.execute("SELECT * FROM operations").fetchone():
        print("Operations table already seeded.")
        return
    operations = [
        ("taille", "regular"),
        ("Récolte", "regular"),
        ("Traitement phytosanitaire", "phytosanitary")
    ]
    cursor.executemany("INSERT INTO operations (nom, type) VALUES (?, ?)", operations)
    db.commit()
    print("Operations seeded successfully.")

# Seed temps_travail Table
def seed_temps_travail(n=100):
    cursor.execute("SELECT id FROM employes")
    employe_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM operations")
    operation_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        employe_id = fake.random.choice(employe_ids)
        operation_id = fake.random.choice(operation_ids)
        heures = round(fake.random.uniform(1.0, 8.0), 2)
        cursor.execute(
            "INSERT INTO temps_travail (employe_id, operation_id, heures) VALUES (?, ?, ?)",
            (employe_id, operation_id, heures)
        )
    db.commit()
    print(f"{n} work hours seeded in temps_travail.")

# Seed phytosanitaires Table
def seed_phytosanitaires(n=30):
    cursor.execute("SELECT id FROM employes")
    employe_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM operations WHERE type = 'phytosanitary'")
    operation_ids = [row[0] for row in cursor.fetchall()]

    diseases = ["Powdery Mildew", "Downy Mildew", "Botrytis Bunch Rot"]
    stages = ["early", "mid", "late"]
    methods = ["spray biologique", "fongicide chimique", "taille et fungicide"]

    for _ in range(n):
        employe_id = fake.random.choice(employe_ids)
        operation_id = fake.random.choice(operation_ids)
        maladie = fake.random.choice(diseases)
        stade = fake.random.choice(stages)
        methode = fake.random.choice(methods)
        observation = fake.sentence()
        randomDate = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute(
            "INSERT INTO phytosanitaires (employe_id, operation_id, maladie, stade, methode, observation, application_date) VALUES (?, ?, ?, ?, ?, ?,?)",
            (employe_id, operation_id, maladie, stade, methode, observation, randomDate)
        )
    db.commit()
    print(f"{n} phytosanitary records seeded.")

# Seed email_settings Table
def seed_email_settings(n=1):
    for _ in range(n):
        email = fake.email()
        password = fake.password()
        cursor.execute("INSERT INTO email_settings (email, password) VALUES (?, ?)", (email, password))
    db.commit()
    print(f"{n} email settings seeded.")

# Run all seeders
seed_employes(50)
seed_operations()
seed_temps_travail(100)
seed_phytosanitaires(30)
seed_email_settings(1)

# Close the database connection
cursor.close()
db.close()
