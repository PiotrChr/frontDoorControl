import sys
from socket import *
import json
import matplotlib.pyplot as plt
from collections import deque

frame_skip = 1

plt.ion()
fig, axs = plt.subplots(3)

dataset_x = deque([])
dataset_y = deque([])
dataset_z = deque([])

serverHost = '192.168.178.33'
# serverHost = '127.0.0.1'
serverPort = 65433

if len(sys.argv) > 1:
    serverHost = sys.argv[1]

sSock = socket(AF_INET, SOCK_STREAM)

sSock.connect((serverHost, serverPort))

line = ""
i = 0


def add_data(dataset, data_to_write):
    if len(dataset) >= 10:
        dataset.popleft()

    dataset.append(data_to_write)


while True:
    lines = sSock.recv(1048).decode().splitlines()
    for line in lines:
        data = json.loads(line)
        add_data(dataset_x, data['x'])
        add_data(dataset_y, data['y'])
        add_data(dataset_z, data['z'])

    if i % frame_skip == 0:
        axs[0].plot(dataset_x)
        axs[1].plot(dataset_y)
        axs[2].plot(dataset_z)

        plt.draw()
        plt.pause(0.0001)

    # plt.clf()

    i = i + 1