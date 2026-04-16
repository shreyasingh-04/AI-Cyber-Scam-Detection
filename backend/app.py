from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import pickle
import sys

app = Flask(__name__)
CORS(app)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add backend folder to path
sys.path.append(BASE_DIR)

# Model paths
model_path = os.path.join(BASE_DIR, "scam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Train model if not exists
if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("Model not found. Training model...")
    from backend import train_model

# Load model
model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


@app.route('/')
def home():
    return "AI Cyber Scam Detection API Running"


@app.route('/predict', methods=['POST'])
def predict():

    data = request.json
    message = data['message'].lower()

    vector = vectorizer.transform([message])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)

    confidence = max(probability[0]) * 100

    if prediction == 1:
        result = "Scam"
    elif confidence > 40:
        result = "Suspicious"
    else:
        result = "Safe"

    return jsonify({
        "message": message,
        "prediction": result,
        "confidence": f"{confidence:.2f}%"
    })


@app.route('/predict/<path:message>')
def predict_browser(message):

    message = message.lower()

    vector = vectorizer.transform([message])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)

    confidence = max(probability[0]) * 100

    if prediction == 1:
        result = "Scam"
    elif confidence > 40:
        result = "Suspicious"
    else:
        result = "Safe"

    return {
        "message": message,
        "prediction": result,
        "confidence": f"{confidence:.2f}%"
    }


if __name__ == "__main__":
    app.run(debug=True)
