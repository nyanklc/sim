import numpy as np
import math

wheel_radius = 3 / 100  # m
wheel_circumreference = 2 * math.pi * wheel_radius  # m
step_count = 200

time_arr = np.load("./time_arr.npy")
lin_speed_arr = np.load("./lin_speed_arr.npy")
ang_speed_arr = np.load("./ang_speed_arr.npy")

def convert_to_step_counts(lin, ang):
    left = []
    right = []

    # # convert to velocity
    # for i in range(len(time_arr)):
    #     left.append(lin_speed_arr[i] * 1000 / math.pi + ang_speed_arr[i] * 75 / math.pi)  # rpm
    #     right.append(lin_speed_arr[i] * 1000 / math.pi - ang_speed_arr[i] * 75 / math.pi)  # rpm

    # convert to velocity
    for i in range(len(time_arr)):
        left.append(lin_speed_arr[i] + ang_speed_arr[i] * 15 / 200)  # m/s
        right.append(lin_speed_arr[i] - ang_speed_arr[i] * 15 / 200)  # m/s

    print("after vel")
    print(f"time: {time_arr}")
    print(f"printing left: {left}")
    print(f"printing right: {right}")

    # convert to distance
    for i in range(len(time_arr) - 1):
        left[i] *= time_arr[i] / 1000  # m
        right[i] *= time_arr[i] / 1000  # m

    print("after dist")
    print(f"printing left: {left}")
    print(f"printing right: {right}")

    # convert to step count
    for i in range(len(time_arr) - 1):
        left[i] = left[i] / wheel_circumreference * step_count
        right[i] = right[i] / wheel_circumreference * step_count

    return left, right

l, r = convert_to_step_counts(lin_speed_arr, ang_speed_arr)
l = [int(x // 5) for x in l]
r = [int(x // 5) for x in r]
for i in range(len(l)):
    if l[i] < 0:
        l[i] = 0
for i in range(len(r)):
    if r[i] < 0:
        r[i] = 0
print("\n\n\n\n\n\n STEP COUNTS:")
print(f"printing left: {l}")
print(f"printing right: {r}")
print(time_arr)

import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.4.1", 333))
socket_output_stream = sock.makefile('w')

print("sending left")
for i in range(len(l)):
    data_str = "{:.2f} ".format(l[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush()

time.sleep(2)

print("sending right")
for i in range(len(r)):
    data_str = "{:.2f} ".format(r[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush() 

time.sleep(2)

print("sending time")
for i in range(len(time_arr)):
    data_str = "{:.2f} ".format(time_arr[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush()