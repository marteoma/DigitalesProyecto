import RPi.GPIO as gpio
import time
import threading
from ultrasonido import ultrasonido
from servomotor import servo
from sonido import audio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

pinBombillo1 = 33
pinBombillo2 = 40

triggerPuerta1 = 38
echoPuerta1 = 37
triggerPuerta2 = 36
echoPuerta2 = 35
triggerComida = 32
echoComida = 31

pir1 = 7
pir2 = 8

pinServo = 10

motor = servo(40)
ultrasonidoPuerta1 = ultrasonido(triggerPuerta1, echoPuerta1)
ultrasonidoPuerta2 = ultrasonido(triggerPuerta2, echoPuerta2)
ultrasonidoComida = ultrasonido(triggerComida, echoComida)

def sensorPuerta1():
    while True:
        global motor
        distance = ultrasonidoPuerta1.distance()
        if (distance < 6):
            motor.setAngle(90)
        else:
            motor.setAngle(0)		
        time.sleep(1) #Retardo para evitar sobrecarga

def sensorPuerta2():
    while True:
        global motor
        distance = ultrasonidoPuerta2.distance()
        if (distance < 6):
            motor.setAngle(90)
        else:
            motor.setAngle(0)		
        time.sleep(1) #Retardo para evitar sobrecarga

		
def sensorComida():
    while True:
        pass        

def pir1():

def pir2():
    
		



try:
    while True:
        pass
except KeyboardInterrupt:
    print("Fin por consola")
    gpio.cleanup()
