import socket
import plotext as plt
import numpy as np
import time
import sys
import threading
import os

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

global_data = []
new_data = False

def plot_data():
    global new_data
    global global_data
    while True:
        if (new_data == True):
            #print("t1 " + str(len(global_data)))
            new_data = False
            h = 15
            plot_array = convert_data_to_plot_array(h)
            os.system("clear")
            sys.stdout.write("\r")
            for i in range(h):
                temp = ""
                for j in range(len(plot_array)):
                    temp += plot_array[j][-(i+1)]
                sys.stdout.write(temp + "\n")
            sys.stdout.flush()

def convert_data_to_plot_array(data, h):
    # x -> nr of elements from global_data
    # y -> proportional chunks of data of height h
    result = []
    max_gd = 1.0
    for i in range(len(data)):
        if (max(data) == 0):
            max_gd = 1
        else:
            max_gd = max(data)
        temp = int(h*(data[i]/max_gd))
        result += ["▓" * temp + "░" * (h - temp)]
    return result


def display_animation():
    animation = "|/-\\"
    start_time = time.time()
    while True:
        for i in range(4):
            time.sleep(0.2)  # Feel free to experiment with the speed here
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        if time.time() - start_time > 10:  # The animation will last for 10 seconds
            break
    sys.stdout.write("\rDone!")

def receive_messages():
    global new_data
    global global_data
    while True:
        if (new_data == False):
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            #print("received message: %s" % data)
            data = data.decode()
            binned_fft = data.split('Δ')
            binned_fft = np.array(binned_fft[:-1]).astype(float)
            global_data = binned_fft
            new_data = True
            #print("t2 " + str(len(global_data)))
        #print(binned_fft)
        #print(binned_fft)
        #print("End Of Items in Array")
        #x = np.arange(len(binned_fft))

def doit():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print("received message: %s" % data)
        data = data.decode()
        binned_fft = data.split('Δ')
        binned_fft = np.array(binned_fft[:-1]).astype(float)
        #global_data = binned_fft

        h = 15
        plot_array = convert_data_to_plot_array(binned_fft, h)
        #os.system("clear")
        sys.stdout.write("\r")
        for i in range(h):
            temp = ""
            for j in range(len(plot_array)):
                temp += plot_array[j][-(i+1)]
            sys.stdout.write(temp + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    doit()

'''
if __name__ == "__main__":
    t1 = threading.Thread(target=plot_data)
    t2 = threading.Thread(target=receive_messages)
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!")
'''
