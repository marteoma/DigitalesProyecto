import pyrebase
from sonido import audio
import os
import threading
import time
config = {
    "apiKey": "AIzaSyAMTu6x5C8BT3F3rUgXmZTA8UocJO-29Rk",
    "authDomain": "prueba-storage-python.firebaseapp.com",
    "databaseURL": "https://prueba-storage-python.firebaseio.com",
    "projectId": "prueba-storage-python",
    "storageBucket": "prueba-storage-python.appspot.com",
    "messagingSenderId": "572392876919"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
a = audio("d.mp3")
##storage.child("pruebas/prueba1.py").put("d.mp3")

def stop():
    time.sleep(5)
    os.system("pkill mpg123")


def stream_user(message):
    print(message)
    if message["data"]:
        t = threading.Thread(target=stop)
        t.start()
        a.play()
stream = db.child("audio").stream(stream_user)
