import RPi.GPIO as GPIO
import time

BTN1 = 23
BTN2 = 24

LED1 = 25
LED2 = 8

SCREEN = 17

GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

GPIO.setup(SCREEN, GPIO.OUT)

GPIO.output(LED1, 0)
GPIO.output(LED2, 0)

GPIO.output(SCREEN, 0)

# while True:
#     if GPIO.input(BTN1) == 1:
#         GPIO.output(LED1, 1)
#     else:
#         GPIO.output(LED1, 0)
#
#     if GPIO.input(BTN2) == 1:
#         GPIO.output(LED2, 1)
#     else:
#         GPIO.output(LED2, 0)
#
#     time.sleep(0.1)
