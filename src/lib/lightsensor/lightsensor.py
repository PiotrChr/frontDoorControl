import smbus
from settings import settings


class LightSensor:
    DEVICE = settings['light']['addr']  # Default device I2C address
    POWER_DOWN = settings['light']['POWER_DOWN']
    POWER_ON = settings['light']['POWER_ON']  # Power on
    RESET = settings['light']['RESET']  # Reset data register value
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = settings['light']['CONTINUOUS_LOW_RES_MODE']
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = settings['light']['CONTINUOUS_HIGH_RES_MODE_1']
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = settings['light']['CONTINUOUS_HIGH_RES_MODE_2']
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = settings['light']['ONE_TIME_HIGH_RES_MODE_1']
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = settings['light']['ONE_TIME_HIGH_RES_MODE_2']
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = settings['light']['ONE_TIME_LOW_RES_MODE']

    def __init__(self):
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

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
