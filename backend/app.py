from flask import Flask, request ,jsonify
from flask_cors import CORS
from database import conn,cursor
import sys
import os
import threading
import time


sys.path.append(
    os.path.abspath("../ai-model")
)

from predict_api import (
    start_camera,
    stop_camera,
    get_prediction
)
# Shared variables
latest_prediction = {
    "gesture": None,
    "confidence": 0
}

running = False
camera_thread = None

def prediction_loop():
    global latest_prediction, running

    last_saved = None

    while running:

        gesture, confidence = get_prediction()

        print("Prediction:", gesture, confidence)   # <-- ADD THIS

        latest_prediction = {
            "gesture": gesture,
            "confidence": confidence
        }

        if gesture is not None and gesture != last_saved:

            cursor.execute(
                """
                INSERT INTO translations
                (gesture, translation)
                VALUES (?, ?)
                """,
                (gesture, gesture)
            )

            conn.commit()

            last_saved = gesture

        time.sleep(0.1)

app=Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "SignVision Backend Running"

@app.route("/start", methods=["POST"])
def start_prediction():
    global running, camera_thread

    if not running:
        running = True

        start_camera()      

        camera_thread = threading.Thread(
            target=prediction_loop,
            daemon=True
        )

        camera_thread.start()

    return jsonify({
        "message": "Prediction Started"
    })

@app.route("/latest_prediction")
def latest():

    return jsonify({
        "translation": latest_prediction["gesture"],
        "confidence": latest_prediction["confidence"]
    })

@app.route("/stop", methods=["POST"])
def stop_prediction():
    global running

    running = False

    stop_camera()      

    return jsonify({
        "message": "Prediction Stopped"
    })



@app.route("/history")
def history():
    cursor.execute(
        "SELECT * FROM translations"
    )

    rows = cursor.fetchall()

    result =[]

    for row in rows:
        result.append({
            "id":row[0],
            "gesture":row[1],
            "translation":row[2]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)