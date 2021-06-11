import RPi.GPIO as GPIO

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

while True:
    red = GPIO.input(23)
    black = GPIO.input(24)

    print(red)
    time.sleep(0.1)
