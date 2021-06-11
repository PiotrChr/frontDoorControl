from src.lib.motionsensor import motionsensor
from src.service import baseService
import threading
import time

lock = threading.Lock()


class MotionController(baseService.BaseService):
    def __init__(
            self,
            motion_sensor: motionsensor.MotionSensor
    ) -> None:
        super().__init__()

        self.motion_sensor = motion_sensor
        self.stop = False
        self.off_handler = None
        self.on_handler = None
        self.t = None

    def set_handlers(self, off_handler=None, on_handler=None):
        self.off_handler = off_handler
        self.on_handler = on_handler

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
                self.stop
            )
        )
        self.t.start()

    def worker(self, off_handler, on_handler, stop):
        while True and not stop:
            current_read = self.motion_sensor.read()
            if current_read == 1:
                on_handler()
            if current_read == 0:
                off_handler()

            time.sleep(0.2)
