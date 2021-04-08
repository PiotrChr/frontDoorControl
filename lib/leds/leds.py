from settings import settings
import RPi.GPIO as GPIO


class Leds:
    LED_RED = settings['led_red']['pin']
    LED_WHITE = settings['led_white']['pin']

    def __init__(self):
        GPIO.setup(self.LED_RED, GPIO.OUT)
        GPIO.setup(self.LED_WHITE, GPIO.OUT)

    def red_off(self):
        GPIO.output(self.LED_RED, 0)

    def white_off(self):
        GPIO.output(self.LED_WHITE, 0)

    def red_on(self):
        GPIO.output(self.LED_RED, 1)

    def white_on(self):
        GPIO.output(self.LED_WHITE, 1)
