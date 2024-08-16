from machine import Pin,PWM,ADC
import time
from moteur import Moteur
from servo import Servo

class Voiture:
    def __init__(self,motArriere1,motArriere2,volant):
        self.motArriere1 = Moteur(motArriere1[0],motArriere1[1],motArriere1[2])
        self.motArriere2 = Moteur(motArriere2[0],motArriere2[1],motArriere2[2])
       
        self.volant = Servo(volant)
        
        
    def conduire(self, val_1, val_2):
        if val_1 < -20:
            
            self.motArriere1.reculer(-val_1)
            self.motArriere2.reculer(-val_1)
        elif val_1> 20:
            self.motArriere1.avancer(val_1)
            self.motArriere2.avancer(val_1)
            
        else :
            #pass
            self.motArriere1.stop() #arrêter les moteurs
            self.motArriere2.stop() #arrêter les moteurs
        
            
        self.volant.write_angle(val_2)
            
    
     
    
    


