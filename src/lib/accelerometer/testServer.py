#!/usr/bin/env python3
import accelerometer
import socket
import json
import time

HOST = '192.168.178.33'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

acc = accelerometer.Accelerometer()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        num = 1
        while True:
            acc_data = {
                'x': acc.acc_x(),
                'y': acc.acc_y(),
                'z': acc.acc_z()
            }
            data = (json.dumps(acc_data) + '\n').encode()
            conn.send(data)
            time.sleep(1)
