from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
model_path = os.path.join(BASE_DIR, "../model/scam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "../model/vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


# Home Route
@app.route('/')
def home():
    return render_template("index.html")


# POST API Route
@app.route('/predict', methods=['POST'])
def predict():

    data = request.json
    message = data['message'].lower()

    vector = vectorizer.transform([message])

    probability = model.predict_proba(vector)
    scam_probability = probability[0][1] * 100

    if scam_probability > 70:
        result = "Scam"
    elif scam_probability > 40:
        result = "Suspicious"
    else:
        result = "Safe"

    return jsonify({
        "message": message,
        "prediction": result,
        "confidence": f"{scam_probability:.2f}%"
    })


# Browser Testing Route (Optional but useful)
@app.route('/predict/<path:message>')
def predict_browser(message):

    message = message.lower()
    vector = vectorizer.transform([message])

    probability = model.predict_proba(vector)
    scam_probability = probability[0][1] * 100

    if scam_probability > 70:
        result = "Scam"
    elif scam_probability > 40:
        result = "Suspicious"
    else:
        result = "Safe"

    return jsonify({
        "message": message,
        "prediction": result,
        "confidence": f"{scam_probability:.2f}%"
    })


# Run App
if __name__ == "__main__":
    app.run(debug=True)
