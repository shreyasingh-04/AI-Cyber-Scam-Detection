from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import sys

app = Flask(__name__)
CORS(app)

# Get backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add backend to system path
sys.path.insert(0, BASE_DIR)

# Model paths
model_path = os.path.join(BASE_DIR, "scam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Train model if not exists
if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("Model not found. Training model...")
    import train_model   # <-- this now works

# Load model
model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


@app.route('/')
def home():
    return "AI Cyber Scam Detection Running"


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
