from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("sentiment_model.h5")

# Load tokenizer
with open("tokenizer.json", "r") as f:
    tokenizer = tokenizer_from_json(json.load(f))

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get("text", "")

    # Tokenize input text
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=10)

    # Predict sentiment
    prediction = model.predict(padded_sequence)
    sentiment = "positive" if prediction[0] > 0.5 else "negative"

    return jsonify({"sentiment": sentiment, "confidence": float(prediction[0])})

@app.route('/save_to_firebase', methods=['POST'])
def save_to_firebase():
    data = request.json
    db.collection('sentiments').add(data)
    return jsonify({"message": "Data saved successfully"})

if __name__ == '__main__':
    app.run(debug=True)
