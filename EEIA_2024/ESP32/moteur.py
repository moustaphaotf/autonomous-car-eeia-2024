from machine import Pin,PWM
import time

class Moteur:
    def __init__(self,pin1,pin2,en):
        
        self.en  = PWM(Pin(en), freq=50)
        self.pin1 = Pin(pin1,Pin.OUT)
        self.pin2 = Pin(pin2,Pin.OUT)
        
    def avancer(self,vitesse):
        self.en.duty(vitesse)
        self.pin1.on()
        self.pin2.off()
        
    def reculer(self,vitesse):
        self.en.duty(vitesse)
        self.pin1.off()
        self.pin2.on()
        
            
    def stop(self):
        self.en.duty(0)
        self.pin1.off()
        self.pin2.off()

