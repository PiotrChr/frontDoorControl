from src.lib.lightsensor import lightsensor
from src.service import baseService
import time
import threading


class LightController(baseService.BaseService):
    def __init__(
            self,
            light_sensor: lightsensor.LightSensor
    ) -> None:
        super().__init__()

        self.light_sensor = light_sensor
        self.sensor_handler = None
        self.current_read = None
        self.stop = False
        self.t = None

    def set_handlers(self, handler=None):
        self.sensor_handler = handler

    def worker(self, sensor_handler, current_read, stop):
        while True and not stop:
            current_read = self.light_sensor.read_light()
            sensor_handler(current_read)
            time.sleep(1)

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
            args=(
                self.sensor_handler,
                self.current_read,
                self.stop,
            )
        )
        self.t.start()
