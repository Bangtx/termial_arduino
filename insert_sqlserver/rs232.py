import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM8',
    baudrate=19200,
    timeout=1,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
ser.isOpen()
# Reading the data from the serial port. This will be running in an infinite loop.

while 1 :
        bytesToRead = ser.inWaiting()
        datat = ser.read(bytesToRead)
        time.sleep(1)
        print(datat)

# import socket
#
# TCP_IP = "192.168.52.10"
# TCP_PORT = 10001
# BUFFER_SIZE = 1024
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# print("connected: ", s)
# data = s.recv(BUFFER_SIZE)
# s.close()
# print("received data: ", data)