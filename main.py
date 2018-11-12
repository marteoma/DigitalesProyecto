import RPi.GPIO as gpio
import time
import threading
from ultrasonido import ultrasonido
from servomotor import servo
from sonido import audio
from myfirebase import firebase

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

ppir1 = 7
ppir2 = 8

pinServo = 10

motor = servo(40)
ultrasonidoPuerta1 = ultrasonido(triggerPuerta1, echoPuerta1)
ultrasonidoPuerta2 = ultrasonido(triggerPuerta2, echoPuerta2)
ultrasonidoComida = ultrasonido(triggerComida, echoComida)

gpio.setup(ppir1, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(ppir2, gpio.IN, pull_up_down = gpio.PUD_DOWN)

gpio.setup(pinBombillo1, gpio.OUT)
gpio.setup(pinBombillo2, gpio.OUT)

def sensorPuerta1():
    while True:
        global motor
        distance = ultrasonidoPuerta1.distance()
        if (distance < 11):            
            motor.setAngle(0)
            time.sleep(1.5)
            motor.setAngle(90)
        # else:
        #     motor.setAngle(0)		
        # time.sleep(1) #Retardo para evitar sobrecarga

def sensorPuerta2():
    while True:
        global motor
        distance = ultrasonidoPuerta2.distance()
        if (distance < 11):
            motor.setAngle(90)
            time.sleep(1.5)
            motor.setAngle(0)
        # else:
        #     motor.setAngle(0)		
        # time.sleep(1) #Retardo para evitar sobrecarga

		
def sensorComida():
    while True:
        pass

def pir1():
    while True:
        if gpio.input(ppir1):
            gpio.output(pinBombillo1, 1)
            gpio.output(pinBombillo2, 0)
        else:
            gpio.output(pinBombillo1, 0)

def pir2():
    while True:
        if gpio.input(ppir2):
            gpio.output(pinBombillo2, 1)
            gpio.output(pinBombillo1, 0)
        else:
            gpio.output(pinBombillo2, 0)

def takePicture():
    while True:
        

tpir1 = threading.Thread(target = pir1)
tpir1.start()
tpir2 = threading.Thread(target = pir2)
tpir2.start()
tsensorPuerta1 = threading.Thread(target = sensorPuerta1)
tsensorPuerta1.start()
tsensorPuerta2 = threading.Thread(target = sensorPuerta2)
tsensorPuerta2.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Fin por consola")
    gpio.cleanup()
