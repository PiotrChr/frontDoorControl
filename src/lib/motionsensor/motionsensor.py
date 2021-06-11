from settings import settings
from src.service.gpio import Gpio


class MotionSensor:
    def __init__(self, gpio: Gpio):
        self.GPIO = gpio
        self.IN_PIN = settings['motion']['pin']
        self.stop = False

        self.t = None

        self.GPIO.setup(self.IN_PIN, self.GPIO.IN)

    def read(self):
        return self.GPIO.input(self.IN_PIN)

