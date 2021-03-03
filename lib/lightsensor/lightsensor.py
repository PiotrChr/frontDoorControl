import threading
import smbus
import time


class LightSensor:
    DEVICE = 0x23  # Default device I2C address
    POWER_DOWN = 0x00  # No active state
    POWER_ON = 0x01  # Power on
    RESET = 0x07  # Reset data register value
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23

    def __init__(self, sensor_handler):
        self.sensor_handler = sensor_handler
        self.current_read = None
        self.stop = False
        self.t = None
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

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

    @staticmethod
    def convert_to_number(data):
        # Simple function to convert 2 bytes of data
        # into a decimal number. Optional parameter 'decimals'
        # will round to specified number of decimal places.
        result = (data[1] + (256 * data[0])) / 1.2
        return result

    def read_light(self, addr=DEVICE):
        # Read data from I2C interface
        data = self.bus.read_i2c_block_data(
            addr,
            self.ONE_TIME_HIGH_RES_MODE_1
        )
        return self.convert_to_number(data)

    def worker(self, sensor_handler, current_read, stop):
        while True and not stop:
            current_read = self.read_light()
            sensor_handler(current_read)
            time.sleep(1)
