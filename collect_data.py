import cv2
import mediapipe as mp
import numpy as np
import os

GESTURE = "no"  # change later

SAVE_PATH = f"dataset/{GESTURE}"

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

sample_count = len(os.listdir(SAVE_PATH))

print("Press SPACE to record a sample")
print("Press Q to quit")

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    landmarks = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

    cv2.putText(
        frame,
        f"Gesture: {GESTURE}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Samples: {sample_count}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Collect Data", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):

        if len(landmarks) == 63:

            sample_count += 1

            np.save(
                os.path.join(
                    SAVE_PATH,
                    f"sample_{sample_count}.npy"
                ),
                np.array(landmarks)
            )

            print(f"Saved sample {sample_count}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()