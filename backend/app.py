from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import sys

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

model_path = os.path.join(BASE_DIR, "scam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")


def load_model():
    global model, vectorizer

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Model not found. Training model...")
        import train_model

    model = pickle.load(open(model_path, "rb"))
    vectorizer = pickle.load(open(vectorizer_path, "rb"))


load_model()


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
