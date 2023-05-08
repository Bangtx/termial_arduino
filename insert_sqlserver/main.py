from pymodbus.framer import ModbusFramer
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from db import DataBase
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient, ModbusTcpClient


# client = ModbusClient(
#     method='rtu', port='COM2', timeout=2, stopbits=1, bytesize=8, parity='N', baudrate=19200
# )


def read_ans_save_one_device(sensor):
    unit = sensor['unit']
    host = sensor['host']
    port = sensor['port']
    client = ModbusTcpClient(host=host, port=port, framer=ModbusFramer)
    success = client.connect()
    temp = get_data_modbus(client, unit)
    status = 1 if temp else 2
    # insert
    temp_model = DataBase(table_name='temperature')
    temp_model.insert_one(temp=temp, status=status, sensor_id=sensor['sensor_id'])

    return {'temp': temp, 'status': status}


def read_and_save_all_device(sensors):
    return list(map(read_ans_save_one_device, sensors))


def get_data_modbus(client, unit):
    try:
        read = client.read_holding_registers(address=1, count=1, unit=unit)
        # if unit == 1:
        return read.__dict__['registers'][0] if 'registers' in read.__dict__ else None
        # return float(read.registers[0])/10 if read.registers else None
    except:
        return None


def get_sensor():
    sensor_model = DataBase(table_name='sensor')
    sensor_raw_data = sensor_model.get_list()
    sensors = []
    for sensor in sensor_raw_data:
        sensors.append({
            'sensor_id': sensor[0], 'host': sensor[2], 'port': sensor[3], 'unit': sensor[4]
        })
    return sensors


def init():
    sensors = get_sensor()
    read_and_save_all_device(sensors)


init()
