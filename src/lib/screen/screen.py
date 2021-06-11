from settings import settings
from src.service.gpio import Gpio


class Screen:
    SCREEN = settings['screen']['pin']

    def __init__(self, gpio: Gpio):
        self.GPIO = gpio
        self.GPIO.setup(self.SCREEN, self.GPIO.OUT)

    def screen_on(self):
        self.GPIO.output(self.SCREEN, 1)

    def screen_off(self):
        self.GPIO.output(self.SCREEN, 0)
