import smbus
import math
from settings import settings


class Accelerometer:
    DEVICE = settings['acc']['addr']

    # Register
    POWER_MGMT_1 = settings['acc']['POWER_MGMT_1']
    POWER_MGMT_2 = settings['acc']['POWER_MGMT_2']

    GYRO_X = settings['acc']['GYRO_X']
    GYRO_Y = settings['acc']['GYRO_Y']
    GYRO_Z = settings['acc']['GYRO_Z']

    ACC_X = settings['acc']['ACC_X']
    ACC_Y = settings['acc']['ACC_Y']
    ACC_Z = settings['acc']['ACC_Z']

    SCALE_X = -0.02
    SCALE_Y = 0.02
    SCALE_Z = -0.88

    SCALING = True

    NUMB_X = 0.02
    NUMB_Y = 0.02
    NUMB_Z = 0.03

    GYRO_16B_CONV = 131
    ACC_16B_CONV = 16384.0

    def __init__(self):
        self.stop = False
        self.bus = smbus.SMBus(1)

        self.bus.write_byte_data(self.DEVICE, self.POWER_MGMT_1, 0)

    def read_byte(self, reg):
        return self.bus.read_byte_data(self.DEVICE, reg)

    def read_word(self, reg):
        h = self.bus.read_byte_data(self.DEVICE, reg)
        l = self.bus.read_byte_data(self.DEVICE, reg+1)

        return (h << 8) + l

    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    @staticmethod
    def dist(a, b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y,z))

        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))

        return math.degrees(radians)

    def normalize(self, value):
        return round(value, 5)

    def gyro_x(self):
        return self.read_word_2c(self.GYRO_X) / self.GYRO_16B_CONV

    def gyro_y(self):
        return self.read_word_2c(self.GYRO_Y) / self.GYRO_16B_CONV

    def gyro_z(self):
        return self.read_word_2c(self.GYRO_Z) / self.GYRO_16B_CONV

    def denoise(self, ax, axis):
        if (axis == 'x' and (ax > self.NUMB_X or ax < -self.NUMB_X)) \
                or (axis == 'y' and (ax > self.NUMB_Y or ax < -self.NUMB_Y)) \
                or (axis == 'z' and (ax > self.NUMB_Z or ax < -self.NUMB_Z)):
            return ax
        else:
            return 0

    def scale(self, value):
        if self.SCALING:
            return value
        else:
            return 0

    def x(self):
        print(self.read_word_2c(self.ACC_X))
        return self.read_word_2c(self.ACC_X)

    def y(self):
        return self.read_word_2c(self.ACC_X)

    def z(self):
        return self.read_word_2c(self.ACC_X)

    def acc_x(self):
        return self.normalize(
            float(self.x() / self.ACC_16B_CONV) + self.scale(self.SCALE_X)
        )

    def acc_y(self):
        return self.normalize(
            float(self.y() / self.ACC_16B_CONV) + self.scale(self.SCALE_Y)
        )

    def acc_z(self):
        return self.normalize(
            float(self.z() / self.ACC_16B_CONV) + self.scale(self.SCALE_Y)
        )

    def rot_x(self):
        return self.get_x_rotation(
            self.x() / self.ACC_16B_CONV,
            self.y() / self.ACC_16B_CONV,
            self.z() / self.ACC_16B_CONV
        )

    def rot_y(self):
        return self.get_y_rotation(
            self.x() / self.ACC_16B_CONV,
            self.y() / self.ACC_16B_CONV,
            self.z() / self.ACC_16B_CONV
        )
