# Maintenance Prediction API

This is a Flask-based REST API for predicting machine downtime based on maintenance data. It allows users to upload a dataset, train a logistic regression model, and make predictions.

## Features
- **Upload Dataset**: Upload CSV files containing maintenance data.
- **Train Model**: Train a logistic regression model using the uploaded dataset.
- **Predict Downtime**: Use the trained model to predict downtime based on input parameters.

---

## Code Structure
```
├── app.py                  # Main Flask application file
├── data/                  # Directory to store uploaded data
├── models/                # Directory to store trained models
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## Setup Instructions

### Prerequisites
1. Python 3.7 or higher.
2. `pip` (Python package manager).
3. (Optional) Postman for testing API endpoints.

### Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create necessary directories:
   ```bash
   mkdir data models
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

The app will be running on `http://127.0.0.1:5000` by default.

---

## API Endpoints

### 1. **Upload Dataset**
- **Endpoint**: `/upload`
- **Method**: POST
- **Description**: Upload a CSV file containing maintenance data.
- **Required Columns**:
  `Type`, `Air temperature [°C]`, `Process temperature [°C]`, `Rotational speed [rpm]`, `Torque [Nm]`, `Tool wear [min]`, `Target`, `Failure Type`, `Temperature difference [°C]`
- **Using Postman**:
  - Select "Body > form-data".
  - Key: `file` (type: File).
  - Value: Upload your CSV file.
  - Click "Send".
- **Without Postman**:
  - Use `curl`:
    ```bash
    curl -X POST -F "file=@<path-to-your-csv-file>" http://127.0.0.1:5000/upload
    ```

### 2. **Train Model**
- **Endpoint**: `/train`
- **Method**: POST
- **Description**: Train a logistic regression model using the uploaded dataset.
- **Using Postman**:
  - Select the "POST" method.
  - Enter `http://127.0.0.1:5000/train`.
  - Click "Send".
- **Without Postman**:
  - Use `curl`:
    ```bash
    curl -X POST http://127.0.0.1:5000/train
    ```

### 3. **Predict Downtime**
- **Endpoint**: `/predict`
- **Method**: POST
- **Description**: Predict downtime based on input parameters.
- **Required Inputs**:
  - `Air temperature [°C]`
  - `Process temperature [°C]`
  - `Rotational speed [rpm]`
  - `Torque [Nm]`
  - `Tool wear [min]`
  - `Temperature difference [°C]`
- **Using Postman**:
  - Select "Body > raw > JSON".
  - Example JSON body:
    ```json
    {
        "Air temperature [°C]": 300,
        "Process temperature [°C]": 310,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 50,
        "Tool wear [min]": 200,
        "Temperature difference [°C]": 10
    }
    ```
  - Click "Send".
- **Without Postman**:
  - Use `curl`:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{
        "Air temperature [°C]": 300,
        "Process temperature [°C]": 310,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 50,
        "Tool wear [min]": 200,
        "Temperature difference [°C]": 10
    }' \
    http://127.0.0.1:5000/predict
    ```

---

## Notes
1. Ensure the dataset contains all required columns before uploading.
2. Train the model before using the `/predict` endpoint.
3. The application saves uploaded files in the `data/` directory and trained models in the `models/` directory.

---

Feel free to reach out for any questions or improvements!

