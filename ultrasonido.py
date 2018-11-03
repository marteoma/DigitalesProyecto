import RPi.GPIO as gpio
import time

class ultrasonido:
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

    def distance(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        gpio.output(self.trigger, 0)
        time.sleep(50e-6)
        gpio.output(self.trigger, 1)
        time.sleep(10e-6)
        gpio.output(self.trigger, 0)
        while gpio.input(self.echo) == 0:
            pass
        ti = time.time()
        while gpio.input(self.echo) == 1:
            pass
        tf = time.time()
        d = 17000 * (tf - ti) #Distancia
        return round(d, 2)
