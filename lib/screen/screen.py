from settings import settings
import RPi.GPIO as GPIO


class Screen:
    SCREEN = settings['screen']['pin']

    def __init__(self):
        GPIO.setup(self.SCREEN, GPIO.OUT)

    def screen_on(self):
        GPIO.output(self.SCREEN, 1)

    def screen_off(self):
        GPIO.output(self.SCREEN, 0)
