import smbus

bus = smbus.SMBus(1)

I2C_DOOR_ADDRESS = 11
OPEN_CMD = 100
CLOSE_CMD = 101


def convert_strings_to_bytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted


def open_door(opened_handler=None, closed_handler=None):
    bytes_to_send = [OPEN_CMD]

    bus.write_i2c_block_data(I2C_DOOR_ADDRESS, 0x00, bytes_to_send)


open_door()
