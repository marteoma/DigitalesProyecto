import pyrebase

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
##storage.child("pruebas/prueba1.py").put("d.mp3")

def stream_user(message):    
    print(message)
stream = db.child("users").stream(stream_user)
