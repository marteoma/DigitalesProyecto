import requests
try:
    from urllib.parse import urlencode, quote
except:
    from urllib import urlencode, quote
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

class firebase:
    def __init__(self, bucket:str, dburl:str, json:str):
        """
        Args:
            bucket: Dirección del bucket de almacenamiento
            dburl: Dirección de la base de datos
            json: nombre del archivo con las credenciales de firebase
        """
        self.bucketurl = bucket
        cred = credentials.Certificate('cred.json')
        self.app = firebase_admin.initialize_app(cred, {
            'storageBucket': bucket,
            'databaseURL': dburl
        })
        self.bucket = storage.bucket(app = self.app)
        self.db = db.reference('/')
  
    def get_url(self, path:str):
        """ Toma una dirección de archivo, y obtiene la URL de descarga
        Args:
            path: Dirección de cómo se encuetra el archivo en gcloud
        """
        if path.startswith('/'):
            path = path[1:]
        return "https://firebasestorage.googleapis.com/v0/b/{0}/o/{1}?alt=media".format(self.bucketurl, quote(path, safe=''))        

    def post(self, blob:str, output:str):
        """ Sube un archivo a gcloud
        Args:
            blob: Dirección a la que se subirá el archivo en gcloud            
            output: Nombre del archivo que se subirá
        """
        blob = self.bucket.blob(blob)
        blob.upload_from_filename(output)

    def fetch(self, path:str):
        """ Descarga un archivo de gcloud
        Args:
            path: Dirección del archivo en gcloud           
        """
        url = self.get_url(path)
        r =  requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path.split('/')[1], 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print(r)

    def write(self):
        pass
    
    def read(self):
        pass

# fir = firebase("prueba-storage-python.appspot.com", "https://prueba-storage-python.firebaseio.com", "cred.json")
# fir.fetch('audio/message.mp3')