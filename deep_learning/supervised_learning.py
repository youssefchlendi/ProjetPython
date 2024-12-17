import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_and_save_model():
  # Connect to the database and load data
  def load_data():
    conn = sqlite3.connect("viticulture.db")
    query = "SELECT maladie, stade, methode, observation FROM phytosanitaires"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

  # Function to generate labels
  def label_effectiveness(obs, stade, maladie):
    """
    Generate effectiveness labels based on observation, stage, and disease severity.
    """
    # Define disease severity levels
    mild_diseases = ["Powdery Mildew", "Downy Mildew", "Black Rot", "Phomopsis Cane and Leaf Spot"]
    moderate_diseases = ["Anthracnose", "Grapevine Leafroll Disease", "Esca", "Eutypa Dieback"]
    severe_diseases = [
      "Botrytis Bunch Rot", "Fanleaf Degeneration", "Crown Gall",
      "Grapevine Trunk Diseases", "Grapevine Yellow Speckle Viroid",
      "Grapevine Red Blotch Disease"
    ]

    # Clean observation
    obs = obs.strip().lower()

    # Assign labels
    if obs == "success":
      if maladie in mild_diseases and stade == "early":
        return 2  # Highly Effective
      elif maladie in moderate_diseases and stade in ["early", "mid"]:
        return 1  # Effective
      elif maladie in severe_diseases:
        return 0  # Partially Effective
    elif obs == "alive":
      return 0  # Partially Effective
    elif obs == "failure":
      return -1  # Ineffective
    elif obs == "dead":
      return -2  # Failed
    
    return -1  # Default to Ineffective

  # Load data and apply the labeling function
  data = load_data()
  print("Data loaded successfully:")
  print(data.head())

  data['effectiveness'] = data.apply(
    lambda row: label_effectiveness(row['observation'], row['stade'], row['maladie']),
    axis=1
  )

  # Remove unknown labels (-1)
  print("Effectiveness label distribution before filtering:")
  print(data['effectiveness'].value_counts())

  data = data[data['effectiveness'] != -1]

  # Check label distribution
  print("Effectiveness label distribution after filtering:")
  print(data['effectiveness'].value_counts())

  # Encode categorical variables
  label_encoders = {}
  for col in ['maladie', 'stade', 'methode']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

  # Prepare features and target
  X = data[['maladie', 'stade', 'methode']]
  y = data['effectiveness']

  # Stratified train-test split
  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
  )

  # Check the label distribution in train and test sets
  print("Training set label distribution:")
  print(y_train.value_counts())
  print("Test set label distribution:")
  print(y_test.value_counts())

  # Train the Random Forest Classifier
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  # Predictions and evaluation
  y_pred = model.predict(X_test)

  # Dynamically set target names for classification report
  unique_classes = sorted(y_test.unique())
  labels_mapping = {
    2: "Highly Effective", 1: "Effective", 0: "Partially Effective",
    -1: "Ineffective", -2: "Failed"
  }
  target_names = [labels_mapping[label] for label in unique_classes]

  # Print evaluation metrics
  print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
  print("Classification Report:")
  print(classification_report(y_test, y_pred, target_names=target_names))

  # Save the model and encoders
  joblib.dump(model, "treatment_effectiveness_model.pkl")
  joblib.dump(label_encoders, "label_encoders.pkl")
  print("Model and encoders saved successfully.")

# Call the function to train and save the model
if __name__ == "__main__":
  train_and_save_model()
