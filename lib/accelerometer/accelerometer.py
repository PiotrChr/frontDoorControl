import smbus
import math


class Accelerometer:
    DEVICE = 0x68

    # Register
    POWER_MGMT_1 = 0x6b
    POWER_MGMT_2 = 0x6c

    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    ACC_X = 0x3b
    ACC_Y = 0x3d
    ACC_Z = 0x3f

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

    def gyro_x(self):
        self.read_word_2c(0x43)

    def gyro_y(self):
        self.read_word_2c(0x45)

    def gyro_z(self):
        self.read_word_2c(0x47)

