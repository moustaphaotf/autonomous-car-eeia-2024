from voiture import Voiture
from time import sleep, ticks_ms
from machine import UART, Pin, ADC, time_pulse_us
import ustruct


data_fichier = ""  #declaration de la varialble de la base de donnée
led = Pin(2, Pin.OUT)

uart = UART(2, 9600) #Création de l'objet de communication série
signal =Pin(34 , Pin.IN)

y = Pin(5,Pin.IN)                #  crée l'objet de reception des commandes de l'axe y
x =Pin(18,Pin.IN)                #  crée l'objet de reception des commandes de l'axe x
val_moteur=0                          # variable de prétaitements des valeurs de l'axe x
val_servo=38                         # variable de prétaitements des valeurs de l'axe y

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
    
    #voiture.conduire(-100, 0)
#     #t = ticks_ms()
    val_x = time_pulse_us(x, 1, 2005)#Prélecture sans enregistrement de la variable !!!! IMPORTANT CAR EVITE DES BUGS DE VALEURS
    val_x = time_pulse_us(x, 1, 2005) #lecture et enregistrement de la valeur reçu sur l'axe des x
    val_y = time_pulse_us(y, 1, 2005)#Prélecture sans enregistrement de la variable !!!! IMPORTANT CAR EVITE DES BUGS DE VALEURS
    val_y = time_pulse_us(y, 1, 2005) #lecture et enregistrement de la valeur reçu sur l'axe des y
    
    
    #### Prétraitement de la variable X et changement d'intervalle
    #print(val_y)
    if  val_y !=-1 and val_y !=-2 :
        val_moteur = val_y
        val_moteur = int(mape(val_moteur, 1000,2000,-500,500)) #conversion de [1000,2000] à [-500,500]
        
    
    
    
        #### Prétraitement de la variable Y et changement d'intervalle
    if val_x != -2:
        val_servo = val_x
        val_servo = int(mape(val_servo, 1000,2000,0,76))  #conversion de [1000,2000] à [55,115]
    #print("val_servo: ", val_servo, "val_moteur: ", val_moteur)
    voiture.conduire(val_moteur,val_servo)  # Piloter la voiture avec les deux valeurs de moteurs
    #voiture.conduire(0,90)
    #print(val_servo)
    if  signal.value():
        #print(ticks_ms()-t)
        data_fichier = ustruct.pack("ff", val_moteur, val_servo) #Compression des données avant l'envoie

        uart.write(data_fichier+"\r\n") # Envoie des informations compressée
    #    print(val_servo, val_moteur)
    else:
        continue
    
    


    


    
    









     



