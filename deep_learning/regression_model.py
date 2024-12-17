import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def train_work_hours_regression():
    # Connect to the database and load data
    conn = sqlite3.connect("viticulture.db")
    query = """
        SELECT employes.id AS employe_id, COUNT(temps_travail.operation_id) AS num_operations, 
               operations.type AS operation_type, SUM(temps_travail.heures) AS total_hours
        FROM temps_travail
        JOIN employes ON temps_travail.employe_id = employes.id
        JOIN operations ON temps_travail.operation_id = operations.id
        GROUP BY employes.id, operations.type
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Preprocessing: Encode categorical 'operation_type'
    data['operation_type'] = pd.Categorical(data['operation_type']).codes

    # Features and target
    X = data[['num_operations', 'operation_type']]
    y = data['total_hours']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

    # Save the model
    joblib.dump(model, "work_hours_regression.pkl")
    print("Regression model saved as 'work_hours_regression.pkl'.")
