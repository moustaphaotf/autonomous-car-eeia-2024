from tensorflow import lite
import time
import numpy as np
import pandas as pd # Importation de pandas pour pouvoir gérer les fichiers csv.
import os # Importation de os pour pouvoir gérer  les chemins et la création de fichier 
import cv2 # importation de cv2 pour la gestion de la caméra.
from datetime import datetime # Importation de datetime pour la gestion de la date.
import struct
import serial
#import Adafruit_ADS1x15 # Import the ADS1x15 module.
#import keyboard
#import tensorflow
import subprocess

FRAME_WIDTH = 160
FRAME_HEIGHT = 120

max_throttle = 792
max_sterring = 134

x1 = 0
y1 = (224-149)//2  # Centre la hauteur de l'image d'origine dans la hauteur de l'image recadrée
# Coordonnées du coin inférieur droit de la région à extraire
x2 = 224
y2 = y1 + 149
x_intercept = 1


ser = serial.Serial(
  port='/dev/ttyS0', # Change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1) ## Sur le raspberry pi 4 Pin RX = 10  Pin TX = 8 

# Load the TFLite model and allocate tensors.
interpreter_regression = lite.Interpreter(model_path="model_fusion5 .tflite")
#interpreter_classifiaction = lite.Interpreter(model_path='/home/pi/Voiture autonome/autonomous_car/code classifiaction/model__classification.tflite')

#interpreter_classifiaction.allocate_tensors()
interpreter_regression.allocate_tensors()

# Get input and output tensors.
input_details_regression = interpreter_regression.get_input_details()
output_details_regression = interpreter_regression.get_output_details()

#input_details_classification = interpreter_classifiaction.get_input_details()
#output_details_classification = interpreter_classifiaction.get_output_details()

def detect_edges (images):
    grayscale_image  = cv2.cvtColor(images , cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image,(5,5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    return edges

if __name__ == "__main__":

  subprocess.call(["figlet", "IA Car BE"])
  print("Initialisation de la prédiction...")
  #time.sleep(2)
  cap = cv2.VideoCapture(0)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
  cap.set(cv2.CAP_PROP_FPS, 25)
  print("La vitesse de capture d'images est de :",cap.get (cv2.CAP_PROP_FPS), "FPS")



  #cap = cv2.VideoCapture(0)
  while 1:
    _, img = cap.read()
    #img = cv2.flip(img, -1)
    #img_30_30 = cv2.resize(img, (30, 30))
    #print(_)
    # Redimensionner la frame à la taille d'entrée du modèle

    #img_30_30 = np.expand_dims(img_30_30, axis=0).astype('float32') / 255.0
    #interpreter_classifiaction.set_tensor(input_details_classification[0]['index'], img_30_30)
    #interpreter_classifiaction.invoke()
    #output_data_classification = interpreter_classifiaction.get_tensor(output_details_classification[0]['index'])

    # Obtenir le nom de la classe prédite
    #predicted_class_index = np.argmax(output_data_classification[0])
    #predicted_class = classes[predicted_class_index]
    #if predicted_class_index ==0 or predicted_class == 1:
      #throttle = 0

    #elif predicted_class_index == 2:
    #img = detect_line_send_angle(img,75,150)
    img = detect_edges(img)
    #print(img.shape)
    input_data_regression = img.astype('float32').reshape((1,120,160,1))

    interpreter_regression.set_tensor(input_details_regression[0]['index'], input_data_regression)

    interpreter_regression.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data_regression = interpreter_regression.get_tensor(output_details_regression[0]['index'])

    throttle =  output_data_regression[0][0]*792
    steering_angle = (((1 + output_data_regression[0][1])/2)*(134-30)) +30


    data = str(int(steering_angle))+ " " + str(int(throttle)) + "\r\n"
    ser.write(data.encode('utf-8'))  
    print(steering_angle,throttle)
    #cv2.putText(img, predicted_class, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Image", img)
    #cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      break
