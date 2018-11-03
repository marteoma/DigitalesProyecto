from time import sleep
import os

class audio:

   def __init__(self, song):
      self.song = song

   def play(self):
      os.system('mpg123 -q {}'.formate(song))

   def stop(self):
      pass
