import RPi.GPIO as gpio

class servo:
    def __init__(self, puerto):
        gpio.setmode(gpio.BOARD)
        gpio.setup(puerto, gpio.OUT)
        self.motor = gpio.PWM(puerto, 50)
        self.motor.start(self.dutty(0))

    def dutty(self, angle):
        dmin = 2.5
        dmax = 12.5
        return ((angle * (dmax - dmin)) / 180) + dmin

    def setAngle(self, angle):
        self.motor.ChangeDutyCycle(self.dutty(angle))
