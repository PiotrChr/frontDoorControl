import matplotlib.pyplot as plt
import numpy
import random
import time

dataset_a = []
dataset_b = []
dataset_c = []
index = []

i = 0
plt.ion()
fig, axs = plt.subplots(3)

while True:
    dataset_a.append(random.random())
    dataset_b.append(random.random())
    dataset_c.append(random.random())
    index.append(i)

    axs[0].plot(dataset_a)
    axs[1].plot(dataset_b)
    axs[2].plot(dataset_c)

    plt.draw()
    plt.pause(0.0001)
    # plt.clf()
    time.sleep(0.02)
