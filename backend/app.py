from flask import Flask, request, jsonify
from flask_cors import CORS
from database import conn, cursor
import sys
import os
import base64
import cv2
import numpy as np

sys.path.append(
    os.path.abspath("../ai-model")
)

from predict_api import predict_gesture

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "SignVision Backend Running"

@app.route("/start", methods=["POST"])
def start_prediction():
    return jsonify({
        "message": "Prediction Started (Cloud Mock)"
    })

@app.route("/stop", methods=["POST"])
def stop_prediction():
    return jsonify({
        "message": "Prediction Stopped (Cloud Mock)"
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image data provided"}), 400

    image_data = data["image"]
    if "," in image_data:
        image_data = image_data.split(",")[1]

    try:
        # Decode base64 image data
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Failed to decode image"}), 400

        # Perform gesture prediction
        gesture, confidence = predict_gesture(frame)

        # Log translation to database if it's a new gesture
        if gesture is not None:
            cursor.execute(
                "SELECT gesture FROM translations ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            last_saved = row[0] if row else None

            if gesture != last_saved:
                cursor.execute(
                    """
                    INSERT INTO translations
                    (gesture, translation)
                    VALUES (?, ?)
                    """,
                    (gesture, gesture)
                )
                conn.commit()

        return jsonify({
            "translation": gesture,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history")
def history():
    cursor.execute(
        "SELECT * FROM translations"
    )

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "gesture": row[1],
            "translation": row[2]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)