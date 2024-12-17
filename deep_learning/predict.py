import joblib
import pandas as pd

def predict_effectiveness(maladie, stade, methode):
    """
    Predict the effectiveness of a treatment based on maladie, stade, and methode.
    """
    # Load the model and encoders
    model = joblib.load("treatment_effectiveness_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")

    # Prepare input data
    input_data = pd.DataFrame([[maladie, stade, methode]], columns=['maladie', 'stade', 'methode'])
    for col in ['maladie', 'stade', 'methode']:
        if input_data[col][0] in label_encoders[col].classes_:
            input_data[col] = label_encoders[col].transform([input_data[col][0]])
        else:
            raise ValueError(f"Invalid value '{input_data[col][0]}' for {col}. Check available options.")

    # Predict effectiveness
    result = model.predict(input_data)
    labels = {2: "Highly Effective", 1: "Effective", 0: "Partially Effective", -1: "Ineffective", -2: "Failed"}
    return labels.get(result[0], "Unknown")

# Example usage
try:
    prediction = predict_effectiveness("Eutypa Dieback", "mid", "spray biologique")
    print(f"Predicted Effectiveness: {prediction}")
except ValueError as e:
    print(e)
