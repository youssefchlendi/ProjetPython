import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
import sqlite3
from tkinter import ttk

# Load the saved regression model
MODEL_PATH = "work_hours_regression.pkl"

def predict_work_hours_interface():
  try:
    model = joblib.load(MODEL_PATH)
  except Exception as e:
    messagebox.showerror("Error", f"Failed to load regression model: {e}")
  def predict():
    try:
      # Get inputs
      num_operations = int(num_operations_entry.get().strip())
      operation_type = operation_type_combobox.get().strip()

      # Prepare input for prediction
      input_data = np.array([[num_operations, operation_types.index(operation_type)]])

      # Predict total work hours
      prediction = model.predict(input_data)[0]
      result_label.config(text=f"Predicted Total Work Hours: {prediction:.2f}", fg="green")

    except ValueError:
      messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except Exception as e:
      messagebox.showerror("Prediction Error", f"An error occurred: {e}")

  # Interface for Regression Prediction
  root = tk.Toplevel()
  root.title("Predict Total Work Hours")
  root.geometry("400x300")

  tk.Label(root, text="Number of Operations:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
  num_operations_entry = tk.Entry(root)
  num_operations_entry.grid(row=0, column=1, padx=10, pady=10)

  tk.Label(root, text="Operation Type:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
  def fetch_operation_types():
    conn = sqlite3.connect('viticulture.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT type FROM operations")
    operation_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return operation_types

  operation_types = fetch_operation_types()
  operation_type_combobox = ttk.Combobox(root, values=operation_types)
  operation_type_combobox.grid(row=1, column=1, padx=10, pady=10)

  predict_button = tk.Button(root, text="Predict", command=predict)
  predict_button.grid(row=2, column=1, pady=20)

  result_label = tk.Label(root, text="Predicted Total Work Hours: ", font=("Helvetica", 12))
  result_label.grid(row=3, column=0, columnspan=2, pady=10)

  root.mainloop()
  
if __name__ == "__main__":
  predict_work_hours_interface()
