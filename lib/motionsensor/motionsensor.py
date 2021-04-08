import RPi.GPIO as GPIO
import time
import threading
import time
from settings import settings

lock = threading.Lock()


class MotionSensor:
    def __init__(self, off_handler=None, on_handler=None):
        self.IN_PIN = settings['motion']['pin']
        self.stop = False
        self.current_read = 0
        self.off_handler = off_handler
        self.on_handler = on_handler
        self.t = None

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN_PIN, GPIO.IN)

    def stop(self):
        self.stop = True

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
            args=(
                self.off_handler,
                self.on_handler,
                self.current_read,
                self.stop
            )
        )
        self.t.start()

    def worker(self, off_handler, on_handler, current_read, stop):
        while True and not stop:
            current_read = GPIO.input(self.IN_PIN)
            if current_read == 1:
                on_handler()
            if current_read == 0:
                off_handler()

            time.sleep(1)
