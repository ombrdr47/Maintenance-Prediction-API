from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

app = Flask(__name__)

# Constants
DATA_PATH = 'data/new_pred_maintenance.csv'
MODEL_PATH = 'models/downtime_model.pkl'

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        data = pd.read_csv(file)

        # Validate required columns
        required_columns = [
            "Type", "Air temperature [°C]", "Process temperature [°C]", 
            "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]", 
            "Target", "Failure Type", "Temperature difference [°C]"
        ]
        if not all(column in data.columns for column in required_columns):
            return jsonify({"error": f"Dataset must contain these columns: {', '.join(required_columns)}"}), 400

        # Save uploaded dataset
        data.to_csv(DATA_PATH, index=False)
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train', methods=['POST'])
def train():
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "No dataset uploaded"}), 400
    df = pd.read_csv(DATA_PATH)

    # Features and target
    X = df[[
        "Air temperature [°C]", "Process temperature [°C]", 
        "Rotational speed [rpm]", "Torque [Nm]", 
        "Tool wear [min]", "Temperature difference [°C]"
    ]]
    y = df["Failure Type"]

    try:
        # Train model
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

        # Save the trained model
        joblib.dump(model, MODEL_PATH)

        # Calculate metrics
        y_pred = model.predict(X)
        metrics = {
            "accuracy": accuracy_score(y, y_pred),
            "precision": precision_score(y, y_pred, average='weighted'),
            "recall": recall_score(y, y_pred, average='weighted'),
            "f1_score": f1_score(y, y_pred, average='weighted')
        }

        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()

    # Ensure model exists
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Model is not trained"}), 400

    # Validate input data
    required_inputs = [
        "Air temperature [°C]", "Process temperature [°C]", 
        "Rotational speed [rpm]", "Torque [Nm]", 
        "Tool wear [min]", "Temperature difference [°C]"
    ]
    if not all(key in input_data for key in required_inputs):
        return jsonify({"error": f"Missing required inputs: {', '.join(required_inputs)}"}), 400

    try:
        model = joblib.load(MODEL_PATH)

        # Prepare input for prediction
        input_features = [[
            input_data["Air temperature [°C]"], 
            input_data["Process temperature [°C]"], 
            input_data["Rotational speed [rpm]"], 
            input_data["Torque [Nm]"], 
            input_data["Tool wear [min]"], 
            input_data["Temperature difference [°C]"]
        ]]

        # Predict
        prediction_proba = model.predict_proba(input_features)[0]
        prediction = model.classes_[prediction_proba.argmax()]
        confidence = prediction_proba.max()
        result = "Yes" if prediction else "No"

        return jsonify({"Downtime": result, "Confidence": round(confidence, 2)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)