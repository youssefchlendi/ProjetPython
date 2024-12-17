import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

def cluster_employee_work_patterns():
    # Connect to database
    conn = sqlite3.connect("viticulture.db")

    # Query to calculate total work hours and number of operations per employee
    query = """
        SELECT employes.id AS employe_id, employes.nom, 
               SUM(temps_travail.heures) AS total_hours, 
               COUNT(DISTINCT temps_travail.operation_id) AS num_operations
        FROM temps_travail
        JOIN employes ON temps_travail.employe_id = employes.id
        GROUP BY employes.id, employes.nom
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    print("Employee Work Data:")
    print(data.head())

    # Features for clustering
    X = data[['total_hours', 'num_operations']]

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['cluster'] = kmeans.fit_predict(X)

    # Save results to the database
    conn = sqlite3.connect("viticulture.db")
    data.to_sql("employee_work_clusters", conn, if_exists="replace", index=False)
    conn.close()
    print("Employee work clusters saved to 'employee_work_clusters' table.")

    # Plot the clusters
    jitter_x = data['total_hours'] + np.random.uniform(-0.3, 0.3, size=len(data))
    jitter_y = data['num_operations'] + np.random.uniform(-0.1, 0.1, size=len(data))

    # Plot the clusters with jitter
    plt.figure(figsize=(8, 6))
    plt.scatter(jitter_x, jitter_y, c=data['cluster'], cmap='viridis', s=100, alpha=0.7, edgecolor='k')
    plt.xlabel("Total Work Hours")
    plt.ylabel("Number of Operations")
    plt.title("Employee Work Patterns Clustering")
    plt.colorbar(label="Cluster")
    plt.show()
