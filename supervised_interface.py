import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd

# Load the model and encoders once for efficiency
MODEL_PATH = "treatment_effectiveness_model.pkl"
ENCODER_PATH = "label_encoders.pkl"

def predict_effectiveness_interface():
    try:
        model = joblib.load(MODEL_PATH)
        label_encoders = joblib.load(ENCODER_PATH)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model or encoders: {e}")
    def predict():
        try:
            # Gather inputs from the UI
            maladie_input = maladie_combobox.get().strip()
            stade_input = stade_combobox.get().strip()
            methode_input = methode_combobox.get().strip()

            # Validate inputs
            if not maladie_input or not stade_input or not methode_input:
                messagebox.showerror("Error", "All fields are required.")
                return

            # Prepare input data
            input_data = pd.DataFrame([[maladie_input, stade_input, methode_input]], 
                                    columns=['maladie', 'stade', 'methode'])
            for col in ['maladie', 'stade', 'methode']:
                if input_data[col][0] not in label_encoders[col].classes_:
                    messagebox.showerror("Error", f"Invalid value for {col}: '{input_data[col][0]}'")
                    return
                input_data[col] = label_encoders[col].transform([input_data[col][0]])

            # Predict effectiveness
            result = model.predict(input_data)
            labels = {2: "Highly Effective", 1: "Effective", 0: "Partially Effective", -1: "Ineffective", -2: "Failed"}
            prediction = labels.get(result[0], "Unknown")

            # Set color based on result
            if result[0] >= 1:  # Positive outcomes: Effective or Highly Effective
                color = "green"
            elif result[0] == 0:  # Neutral outcome: Partially Effective
                color = "orange"
            else:  # Negative outcomes: Ineffective or Failed
                color = "red"

            # Display prediction result
            result_label.config(text=f"Prediction: {prediction}", fg=color)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    # Main prediction window
    root = tk.Toplevel()
    root.title("Predict Treatment Effectiveness")
    root.geometry("400x300")

    # Input Labels and Fields
    tk.Label(root, text="Maladie:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    maladie_combobox = ttk.Combobox(root, values=list(label_encoders['maladie'].classes_))
    maladie_combobox.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Stade:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    stade_combobox = ttk.Combobox(root, values=list(label_encoders['stade'].classes_))
    stade_combobox.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Méthode:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    methode_combobox = ttk.Combobox(root, values=list(label_encoders['methode'].classes_))
    methode_combobox.grid(row=2, column=1, padx=10, pady=10)

    # Predict Button
    predict_button = tk.Button(root, text="Predict", command=predict)
    predict_button.grid(row=3, column=1, pady=20)

    # Prediction Result
    result_label = tk.Label(root, text="Prediction: ", font=("Helvetica", 12))
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    predict_effectiveness_interface()