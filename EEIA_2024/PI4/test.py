import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import cv2
import os


model = tf.keras.models.load_model('traffic_sign_recognition_model_now.keras')

def detect_circle(image):
    global counter

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Filtrer par couleur (rouge pour le panneau de signalisation)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2

    # Appliquer le masque pour extraire les parties rouges
    res = cv2.bitwise_and(image, image, mask=mask)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Utiliser la transformation de Hough pour détecter les cercles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=100, param2=30, minRadius=10, maxRadius=100)

    # Si au moins un cercle est détecté
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        # Trouver le plus grand cercle détecté
        max_circle = max(circles, key=lambda c: c[2])  # c[2] est le rayon du cercle

        # Dessiner uniquement le plus grand cercle détecté
        x, y, r = max_circle
        cv2.rectangle(image, (x - r, y - r), (x + r, y + r), (0, 220, 0), 2)  # Dessiner un carré vert autour du cercle

        # Extraire la région d'intérêt (le panneau détecté)
        roi = image[y - r:y + r, x - r:x + r]

        # Enregistrer l'image si elle n'est pas vide
        if roi.size > 0:
            print(roi.shape)
            return (True, roi)

    return (False, None)


def recognize_traffic_sign(image, model):
    image = cv2.resize(image, (32, 32))
    image = np.expand_dims(image, axis=0) / 255
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Example: Using a camera to capture and recognize traffic signs
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    status, image = detect_circle(frame)
    if status:
        sign = recognize_traffic_sign(image, model)

        if sign == 0:
            text= "Stop"
        elif sign == 2:
            text= "60"
        elif sign == 1:
            text= "30"

        cv2.putText(frame, f"Panneau: {text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    
    cv2.imshow('Traffic Sign Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()