from flask import Flask, request, jsonify
import joblib
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load("sentiment_analysis_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Initialize Firebase
cred = credentials.Certificate("sentiment-analyzer-aab5e-firebase-adminsdk-fbsvc-a83c047aff.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # Vectorize the input text
    text_vectorized = vectorizer.transform([text])

    # Predict sentiment
    prediction = model.predict(text_vectorized)[0]
    sentiment = "positive" if prediction == 1 else "negative"

    return jsonify({"sentiment": sentiment, "confidence": 1.0})  # Logistic Regression doesn't give probabilities directly

@app.route('/save_to_firebase', methods=['POST'])
def save_to_firebase():
    data = request.json
    db.collection('sentiments').add(data)
    return jsonify({"message": "Data saved successfully"})

# Required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
