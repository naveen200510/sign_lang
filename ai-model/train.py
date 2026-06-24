import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

DATASET_PATH = "dataset"

labels = ["hello", "yes", "no", "help", "thankyou"]

X = []
y = []

for label_index, label in enumerate(labels):

    folder = os.path.join(DATASET_PATH, label)

    for file in os.listdir(folder):

        if file.endswith(".npy"):

            data = np.load(os.path.join(folder, file))

            X.append(data)
            y.append(label_index)

X = np.array(X)
y = np.array(y)

print("X shape:", X.shape)
print("y shape:", y.shape)

y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = Sequential()

model.add(Dense(128, activation="relu", input_shape=(63,)))
model.add(Dense(64, activation="relu"))
model.add(Dense(5, activation="softmax"))

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    X_train,
    y_train,
    epochs=50,
    validation_data=(X_test, y_test)
)

loss, accuracy = model.evaluate(X_test, y_test)

print("Accuracy:", accuracy)

model.save("models/sign_model.h5")

print("Model saved!")