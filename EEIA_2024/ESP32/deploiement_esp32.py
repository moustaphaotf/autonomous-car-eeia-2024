from voiture import Voiture
from time import sleep ,sleep_ms
from machine import UART, Pin, ADC, time_pulse_us



data_fichier = ""  #declaration de la varialble de la base de donnée
led = Pin(2, Pin.OUT)

uart = UART(2, 9600) #Création de l'objet de communication série

y = Pin(5,Pin.IN)                #  crée l'objet de reception des commandes de l'axe y
x =Pin(18,Pin.IN)                #  crée l'objet de reception des commandes de l'axe x
val_moteur=0                          # variable de prétaitements des valeurs de l'axe x
val_servo=38                       # variable de prétaitements des valeurs de l'axe y

#########Création d'une fonction qui permet de changer d'intervalle bornée d'appartenance d'une variable à un autre intervalle######
def mape(x, in_min, in_max, out_min, out_max):
    v= ((x - in_min)*(out_max - out_min))/(in_max - in_min) + out_min
    return v



voiture = Voiture((15,14,19), (4,12,13),33) #Création d'une instance de la classe Voiture


voiture.conduire(val_moteur,val_servo)#initialisation des commandes de la voiture





####### Signe de demarrage de la collecte !!!!! allumage et extinction de la led blue de l'esp32 !!!!!
led.on()
sleep(1)
led.off()


while 1 :
    try:
        b = uart.readline()[:-2].split()
        #val_servo =int(mape(int(b[0]), 0,60,60,0))
        val_moteur =int(b[1])
        #val_servo = int(mape(val_servo, 0,60,60,0))
        #val_moteur = val_moteur*int(5/2)
        val_servo = int(b[0])
        #val_moteur=280
        #print(val_servo)
    except:
        pass
    #val_servo = val_servo*1.25
    #val_servo = int(mape(val_servo, -30,30,0,76))
#     
    if val_servo<0:
      val_servo = 0
    elif val_servo:
      val_servo=val_servo
    elif 76<val_servo:
        val_servo = 76
    #print(val_servo , val_moteur)
#     val_moteur = 250
    #val_servo = int(mape(val_servo, -30,30,0,76))
    #print(val_servo , val_moteur*0.5)
    sleep_ms(100)    
    voiture.conduire(100,val_servo )# Piloter la voiture avec les deux valeurs de moteurs
    
    
    
    


    


    
    









     




