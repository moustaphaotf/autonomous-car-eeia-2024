import  argparse 
import time
import os 
import csv
import cv2
from datetime import datetime
import struct 
import numpy as np
import subprocess
import math

myDirectory = os.path.join(os.getcwd(), "Data")

countFolder = 0

imgList =  []
steeringList = []
accelerateList = []

val_servo = 30
val_moteur = 0

FRAME_WIDTH = 160
FRAME_HEIGHT = 120



def setup():
    # time.sleep(2)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 25)
    print("La vitesse de capture d'images est de :",cap.get (cv2.CAP_PROP_FPS), "FPS")
    
    return cap 

def detect_edges (images):
    grayscale_image  = cv2.cvtColor(images , cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image,(5,5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    return edges

if __name__ == "__main__":
    cap , ser  = setup()


    while 1 :
        print("dfq")
        _ , img = cap.read()
        #img.shape)
        #print(img.shape)
        if _ :
            img = detect_edges(img)
            #print(img.shape)
            
            #img = cv2.flip(img, -1)
            cv2.imshow("Flux", img)
            
            while 1:
                if ser.in_waiting > 0:
                    try :
                        b = ser.readline()[:-2]
                        val_moteur, val_servo =  struct.unpack("ff" , b) 
                        #print(val_moteur,val_servo)
                        
                    
                        #print("succes")
                        break
                    except:
                        print("erreur")
                        

                else:
                    #print("pas de donnée")
                    continue
                    

                
            
            
             

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        
    cv2.destroyAllWindows()
    