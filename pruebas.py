import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

gpio.setup(33, gpio.OUT)

try:
    while True:
        gpio.output(33, 1)
        time.sleep(3)
        gpio.output(33, 0)
        time.sleep(3)
except KeyboardInterrupt:
    gpio.cleanup()
