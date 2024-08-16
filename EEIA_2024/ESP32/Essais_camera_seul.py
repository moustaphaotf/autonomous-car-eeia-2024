import  argparse 
import time
import os 
import csv
import serial
import cv2
from datetime import datetime
import struct 
import numpy as np
import pandas as pd
import gpiozero
import subprocess
import math

signal = gpiozero.LED(23)
myDirectory = os.path.join(os.getcwd(), "Data")

countFolder = 0

imgList =  []


FRAME_WIDTH = 160
FRAME_HEIGHT = 120


cmd_servo = ""
count = 0
while os.path.exists(os.path.join(myDirectory,f'IMG{str(countFolder)}')):# Rechercher la valeur du countFolder non exixtant en incrémentant le countFolder depuis 0 ;
        countFolder += 1 # Incrémentez tant que la valeur de countFolder n'est pas trouvée
newPath = myDirectory + "/IMG" +str(countFolder) # Créez le chemin du nouveau fichier IMG_.. d'index non existant.
os.makedirs(newPath) #Créez le fichier lui même.

    

def saveData(img): # Fonction de sauvegarde des images et des valeur de commandes.
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    fileName = os.path.join(newPath,f'Image_{timestamp} {count}.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    rawData = {'Image': imgList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=list(rawData.keys()))
    print('Log Saved')
    print('Total Images: ',len(imgList))

def setup():
    subprocess.call(["figlet", "IA Car BE"])
    print("Initialisation...")
    time.sleep(2)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 25)
    print("La vitesse de capture d'images est de :",cap.get (cv2.CAP_PROP_FPS), "FPS")
    

    
    ser = serial.Serial(
            port='/dev/ttyS0', # Change this according to connection methods, e.g. /dev/ttyUSB0
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1) ## Sur le raspberry pi 4 Pin RX = 10  Pin TX = 8 
    print("communication avec l'esp32 initialisé")
    return cap , ser


def detect_edges (images):
    grayscale_image  = cv2.cvtColor(images , cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image,(5,5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    return edges

if __name__ == "__main__":
    cap , ser  = setup()


    while 1 :
        _ , img = cap.read()
        if _ :
            img = detect_edges(img)
            cv2.imshow("Flux", img)             
                    
            saveData(img)                    
             
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    saveLog()
    cv2.destroyAllWindows()
    
