import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras import layers, models
from tensorflow import lite

import cv2
import os
import pandas as pd

def load_data_from_csv(csv_file):
    # Load the CSV file
    data = pd.read_csv(csv_file)
    
    # Initialize lists for images and labels
    images = []
    labels = []

    # Iterate over each row in the CSV
    for index, row in data.iterrows():
        # Read the image file
        frame = cv2.imread(row['file_path'])
        
        # Resize the image to 32x32 pixels
        image = cv2.resize(frame, (32, 32))
        
        # Append the image and label to the lists
        images.append(image)
        labels.append(row['label'])
    
    # Convert lists to NumPy arrays
    return np.array(images), np.array(labels)


print("loading images")
images, labels = load_data_from_csv('image_labels.csv')

print("Images loaded")
# Normalize images
images = images / 255.0

# Binarize labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
print(labels)
# Split dataset
X_train, X_test, y_train, y_test = train_test_split(images, labels,shuffle=True, test_size=0.2, random_state=42)

print("data splitted")

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(lb.classes_), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("Model created")


print("Model training")

history = model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test))

print("Training done")


test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f'Test accuracy: {test_acc:.2f}')

# model.save(f'traffic_sign_recognition_model_now.keras')
converter = lite.TFLiteConverter.from_keras_model(model)
tflitemodel = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflitemodel)

print("Model saved")
