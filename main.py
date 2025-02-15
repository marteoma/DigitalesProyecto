import RPi.GPIO as gpio
import time
import threading
import pyrebase
import os
from ultrasonido import ultrasonido
from servomotor import servo
from sonido import audio

config = {
    "apiKey": "AIzaSyAgdjZBh3K8KI3oienmO-OJjSg_063kDVg",
    "authDomain": "mascotas-digitales.firebaseapp.com",
    "databaseURL": "https://mascotas-digitales.firebaseio.com",
    "projectId": "mascotas-digitales",
    "storageBucket": "mascotas-digitales.appspot.com",
    "messagingSenderId": "509567001748"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()

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
            motor.setAngle(90)
            time.sleep(1.5)
            motor.setAngle(0)
            db.child("Salidas").child("fecha").set(time.strftime("%d-%m-%Y"))

def sensorPuerta2():
    while True:
        global motor
        distance = ultrasonidoPuerta2.distance()
        if (distance < 11):
            os.system('streamer -c /dev/video0 -b 16 -o capture.jpeg')
            storage.child("fotos/foto.jpeg").put("capture.jpeg")
            db.child("Entradas").child("Imagen").set(True)
            puerta = db.child("Entradas").child("Puerta").get()
            while puerta != True:
                puerta = db.child("Entradas").child("Puerta").get()
            db.child("Entradas").child("Puerta").set(False)
            motor.setAngle(0)
            time.sleep(1.5)
            motor.setAngle(90)       

		
def sensorComida():
    while True:
        if ultrasonidoComida.distance() < 11:
            db.child("comida").child("fecha").set(time.strftime("%d-%m-%Y"))
            time.sleep(3)

def pir1():
    while True:
        if gpio.input(ppir1):
            gpio.output(pinBombillo1, 1)
            gpio.output(pinBombillo2, 0)
            db.child("posiciones").child("principal").set(True)
            db.child("posiciones").child("secundaria").set(False)
        else:
            gpio.output(pinBombillo1, 0)

def pir2():
    while True:
        if gpio.input(ppir2):
            gpio.output(pinBombillo2, 1)
            gpio.output(pinBombillo1, 0)
            db.child("posiciones").child("principal").set(False)
            db.child("posiciones").child("secundaria").set(True)
        else:
            gpio.output(pinBombillo2, 0)

def takePicture():
    while True:
        if (ultrasonidoPuerta2.distance() < 11:
            os.system('streamer -c /dev/video0 -b 16 -o capture.jpeg')
            storage.child("fotos/foto.jpeg").put("capture.jpeg")

tpir1 = threading.Thread(target = pir1)
tpir1.start()
tpir2 = threading.Thread(target = pir2)
tpir2.start()
tsensorPuerta1 = threading.Thread(target = sensorPuerta1)
tsensorPuerta1.start()
tsensorPuerta2 = threading.Thread(target = sensorPuerta2)
tsensorPuerta2.start()
tsensorComida = threading.Thread(target = sensorComida)
tsensorComida.start()

def stop():
    time.sleep(10)
    os.system("pkill mpg123")

def stream_audio(message):
    if message["data"]:
        storage.child("audio/a.mp3").download("a.mp3")
        a = audio("a.mp3")
        t = threading.Thread(target=stop)
        t.start()
        a.play()
    else:
        os.system("pkill mpg123")
stream = db.child("audio").stream(stream_audio)            

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Fin por consola")
    gpio.cleanup()
