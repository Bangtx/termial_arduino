from config_environment import BAUDRATE, PORT
import serial
import sqlite3
from insert_sqlserver.db import DataBase
from itertools import groupby
import time

SERIAL_PORT = "COM3"  # Replace with your Arduino's serial port
BAUD_RATE = 115200


def write_bf(message):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        ser.write(message.encode())  # Send message with newline

        while True:
            ser.write(message.encode())  # Send message with newline
            response = ser.readline().decode().strip()
            if response:
                print(response)
                break  # Exit loop after receiving re


# get value from sql server
sql_server = DataBase(table_name='temperature')
sql_server_data = sql_server.get_list()
sql_server_data = sql_server.get_latest_value(sql_server_data)
# print(sql_server_data)

db = sqlite3.connect("setting.db")
cursor = db.cursor()

data = cursor.execute('select * from alarm_setting').fetchall()
setting_data = []
for row in data:
    machine = row[1]
    low = row[5]
    high = row[6]

    if machine in sql_server_data and sql_server_data[machine] is not None:
        temp = sql_server_data[machine]
        status = 1 if temp > high else 0
        write_bf(f'{machine}={status}')

    time.sleep(2)