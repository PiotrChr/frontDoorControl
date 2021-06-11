import smbus


class DoorOpener:
    I2C_DOOR_ADDRESS = 11
    OPEN_CMD = 100
    CLOSE_CMD = 101

    STATUS_OPEN = 'OPEN'
    STATUS_CLOSED = 'CLOSED'

    def __init__(self):
        self.bus = smbus.SMBus(1)

    @staticmethod
    def convert_strings_to_bytes(src):
        converted = []
        for b in src:
            converted.append(ord(b))
        return converted

    def open_door(self, opened_handler=None, closed_handler=None):
        print("opening door")
        bytes_to_send = [self.OPEN_CMD]

        self.bus.write_i2c_block_data(self.I2C_DOOR_ADDRESS, 0x00, bytes_to_send)
