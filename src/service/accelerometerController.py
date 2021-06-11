from src.lib.accelerometer import accelerometer
from src.service import baseService
import threading
import time


class AccelerometerController(baseService.BaseService):
    def __init__(
            self,
            accelerometer_sensor: accelerometer.Accelerometer
    ) -> None:
        super().__init__()

        self.t = None
        self.stop = False
        self.handler = None
        self.accelerometer_sensor = accelerometer_sensor

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
            args=(
                self.handler,
                self.stop,
            )
        )
        self.t.start()

    def stop(self):
        self.stop = True

    def set_handlers(self, handler=None):
        self.handler = handler

    def worker(self, sensor_handler, stop):
        while True and not stop:
            sensor_handler(
                self.accelerometer_sensor.acc_x(),
                self.accelerometer_sensor.acc_y(),
                self.accelerometer_sensor.acc_z(),
                self.accelerometer_sensor.gyro_x(),
                self.accelerometer_sensor.gyro_y(),
                self.accelerometer_sensor.gyro_z()
            )
            time.sleep(0.1)
