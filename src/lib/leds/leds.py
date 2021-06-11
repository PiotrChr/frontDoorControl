from settings import settings

from src.service.gpio import Gpio


class Leds:
    LED_RED = settings['led_red']['pin']
    LED_WHITE = settings['led_white']['pin']

    def __init__(self, gpio: Gpio):
        self.GPIO = gpio
        self.GPIO.setup(self.LED_RED, self.GPIO.OUT)
        self.GPIO.setup(self.LED_WHITE, self.GPIO.OUT)

    def red_off(self):
        self.GPIO.output(self.LED_RED, 0)

    def white_off(self):
        self.GPIO.output(self.LED_WHITE, 0)

    def red_on(self):
        self.GPIO.output(self.LED_RED, 1)

    def white_on(self):
        self.GPIO.output(self.LED_WHITE, 1)
