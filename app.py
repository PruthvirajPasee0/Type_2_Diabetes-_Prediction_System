from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load("diabetes_model.pkl")  # Save your trained model using joblib.dump(logR, "diabetes_model.pkl")

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Prediction</title>
    <style>
        body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 200vh;
    background-color: #f4f4f9;
}

h1 {
    text-align: center;
    color: #333;
}

form {
    background: #fff;
    padding: 20px 40px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
}

label {
    font-size: 16px;
    color: #555;
    display: block;
    margin-bottom: 8px;
}

input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

button {
    display: block;
    width: 100%;
    padding: 10px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #0056b3;
}

    </style>
</head>
<body>
    <h1>Diabetes Prediction Form</h1>
    <form action="/predict" method="post">
        <label for="Pregnancies">Pregnancies:</label>
        <input type="number" id="Pregnancies" name="Pregnancies" required><br><br>

        <label for="Glucose">Glucose:</label>
        <input type="number" id="Glucose" name="Glucose" required><br><br>

        <label for="BloodPressure">Blood Pressure:</label>
        <input type="number" id="BloodPressure" name="BloodPressure" required><br><br>

        <label for="SkinThickness">Skin Thickness:</label>
        <input type="number" id="SkinThickness" name="SkinThickness" required><br><br>

        <label for="Insulin">Insulin:</label>
        <input type="number" id="Insulin" name="Insulin" required><br><br>

        <label for="BMI">BMI:</label>
        <input type="number" id="BMI" step="0.1" name="BMI" required><br><br>

        <label for="DiabetesPedigreeFunction">Diabetes Pedigree Function:</label>
        <input type="number" id="DiabetesPedigreeFunction" step="0.01" name="DiabetesPedigreeFunction" required><br><br>

        <label for="Age">Age:</label>
        <input type="number" id="Age" name="Age" required><br><br>

        <button type="submit">Predict</button>
    </form>
</body>
</html>

    '''

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract data from form
        data = [
            float(request.form["Pregnancies"]),
            float(request.form["Glucose"]),
            float(request.form["BloodPressure"]),
            float(request.form["SkinThickness"]),
            float(request.form["Insulin"]),
            float(request.form["BMI"]),
            float(request.form["DiabetesPedigreeFunction"]),
            float(request.form["Age"]),
        ]

        # Reshape the data for prediction
        data = np.array(data).reshape(1, -1)

        # Make a prediction
        prediction = model.predict(data)[0]

        # Determine the outcome
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return f"<h1>The Prediction is: {result}</h1>"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
