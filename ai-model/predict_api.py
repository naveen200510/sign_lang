import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sign_model.h5"
)

model = load_model(MODEL_PATH)

labels = [
    "hello",
    "yes",
    "no",
    "help",
    "thankyou"
]

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def predict_gesture(frame):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if not results.multi_hand_landmarks:
        return None, 0

    hand_landmarks = results.multi_hand_landmarks[0]

    landmarks = []

    for lm in hand_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])

    prediction = model.predict(
        np.array([landmarks]),
        verbose=0
    )

    confidence = float(np.max(prediction))

    gesture = labels[np.argmax(prediction)]

    return gesture, confidence

cap = None


def start_camera():
    global cap

    if cap is None:
        cap = cv2.VideoCapture(0)


def stop_camera():
    global cap

    if cap is not None:
        cap.release()
        cap = None

    cv2.destroyAllWindows()


def get_prediction():

    global cap

    if cap is None:
        return None, 0

    success, frame = cap.read()

    if not success:
        return None, 0

    return predict_gesture(frame)