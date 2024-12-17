import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cluster_operations():
    # Connect to database
    conn = sqlite3.connect("viticulture.db")

    # Query to calculate total work hours and frequency for each operation
    query = """
        SELECT operations.id AS operation_id, operations.nom AS operation_name,
               SUM(temps_travail.heures) AS total_hours, 
               COUNT(temps_travail.id) AS frequency
        FROM temps_travail
        JOIN operations ON temps_travail.operation_id = operations.id
        GROUP BY operations.id, operations.nom
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    print("Operation Work Data:")
    print(data.head())

    # Features for clustering
    X = data[['total_hours', 'frequency']]

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['cluster'] = kmeans.fit_predict(X)

    # Save results to the database
    conn = sqlite3.connect("viticulture.db")
    data.to_sql("operation_work_clusters", conn, if_exists="replace", index=False)
    conn.close()
    print("Operation work clusters saved to 'operation_work_clusters' table.")

    # Plot the clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(data['total_hours'], data['frequency'], c=data['cluster'], cmap='viridis', s=100)
    plt.xlabel("Total Hours Spent")
    plt.ylabel("Frequency")
    plt.title("Operation-Based Clustering")
    plt.colorbar(label="Cluster")
    plt.show()
