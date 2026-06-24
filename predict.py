import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3
import time

model = load_model("models/sign_model.h5")

engine = pyttsx3.init()

last_spoken = ""
last_time = 0

labels = ["hello", "yes", "no", "help", "thankyou"]

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = []

            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            if len(landmarks) == 63:

                prediction = model.predict(
                    np.array([landmarks]),
                    verbose=0
                )

                confidence = np.max(prediction)
                gesture_name = labels[np.argmax(prediction)]
                gesture = f"{gesture_name} ({confidence:.2f})"

                current_time = time.time()

                speech_text = gesture_name
                if gesture_name == "thankyou":
                    speech_text = "thank you"

                if confidence > 0.65 and (
                    gesture_name != last_spoken or current_time - last_time > 3
                ):
                    engine.say(speech_text)
                    engine.runAndWait()

                    last_spoken = gesture_name
                    last_time = current_time

                cv2.putText(
                    frame,
                    gesture,
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

    cv2.imshow("SignVision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()