from time import sleep
import os

class audio:

   def __init__(self, song):
      self.song = song

   def play(self):
      os.system("mpg123 --loop 10 -q {}".format(self.song))

   def stop(self):
      pass
