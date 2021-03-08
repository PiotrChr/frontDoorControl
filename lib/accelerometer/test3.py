# Source: https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/

import smbus
import math
import time
import numpy as np
import matplotlib.pyplot as plt

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a,b):
    return math.sqrt((a*a)+(b*b))


def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)


def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


bus = smbus.SMBus(1)
address = 0x68       # via i2cdetect

dataset_x = []
dataset_y = []
dataset_z = []
index = []

frame_skip = 100

# plt.ion()
# fig, axs = plt.subplots(3)

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

scale_x = -0.02
scale_y = 0.02
scale_z = -0.88

x_numb = 0.01
y_numb = 0.01
z_numb = 0.02


def reduce_noise(ax, axis):
    if (axis == 'x' and (ax > x_numb or ax < x_numb)) \
      or (axis == 'y' and (ax > x_numb or ax < y_numb)) \
      or (axis == 'z' and (ax > x_numb or ax < z_numb)):
        return ax
    else:
        return 0


def plot():
    i = 0
    while True:
        # print("Gyroskop")
        # print("--------")

        # gyroskop_xout = read_word_2c(0x43)
        # gyroskop_yout = read_word_2c(0x45)
        # gyroskop_zout = read_word_2c(0x47)

        # print("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
        # print("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
        # print("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
        #
        # print("Beschleunigungssensor")
        # print("---------------------")

        beschleunigung_xout = read_word_2c(0x3b)
        beschleunigung_yout = read_word_2c(0x3d)
        beschleunigung_zout = read_word_2c(0x3f)

        beschleunigung_xout_skaliert = reduce_noise(round(float(beschleunigung_xout / 16384.0) + scale_x, 4), 'x')
        beschleunigung_yout_skaliert = reduce_noise(round(float(beschleunigung_yout / 16384.0) + scale_y, 4), 'y')
        beschleunigung_zout_skaliert = reduce_noise(round(float(beschleunigung_zout / 16384.0) + scale_z, 4), 'z')

        print(beschleunigung_xout_skaliert)   # x
        print(beschleunigung_yout_skaliert)  # y
        print(beschleunigung_zout_skaliert)  # z

        #
        # print(
        #     "X Rotation: ",
        #     get_x_rotation(
        #         beschleunigung_xout_skaliert,
        #         beschleunigung_yout_skaliert,
        #         beschleunigung_zout_skaliert
        #     )
        # )
        #
        # print(
        #     "Y Rotation: ",
        #     get_y_rotation(
        #         beschleunigung_xout_skaliert,
        #         beschleunigung_yout_skaliert,
        #         beschleunigung_zout_skaliert
        #     )
        # )
        # dataset_x.append(reduce_noise(beschleunigung_xout_skaliert))
        # dataset_y.append(reduce_noise(beschleunigung_yout_skaliert))
        # dataset_z.append(reduce_noise(beschleunigung_zout_skaliert))
        # index.append(i)

        # if i % frame_skip == 0:
        #     axs[0].plot(dataset_x)
        #     axs[1].plot(dataset_y)
        #     axs[2].plot(dataset_z)
        #
        #     plt.draw()
        #     plt.pause(0.0001)
        #
        # # plt.clf()
        #
        # i = i + 1
        time.sleep(0.05)


plot()
