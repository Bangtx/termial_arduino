import time
# from noisuytt import noisuy
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Defaults
from threading import Thread
Defaults.RetryOnEmpty = True
Defaults.Timeout = 5.0
Defaults.Retries = 5.0
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer

# client = ModbusTcpClient("192.168.1.254", port=8880, framer=ModbusFramer)
# success = client.connect()
unit = 1
def read_ans_save_one_device():
    client = ModbusTcpClient(host="192.168.52.10", port=1000, framer=ModbusFramer, timeout= 5.0)
    success = client.connect()
    print(success)
    temp = get_data_modbus(client, unit)
    status = 1 if temp else 2
    # insert
    print(temp)
    print(status)
    # temp_model = DataBase(table_name='temperature')
    # temp_model.insert_one(temp=temp, status=status, sensor_id=sensor['sensor_id'])

    return {'temp': temp, 'status': status}
def get_data_modbus(client, unit):
    try:
        read = client.read_holding_registers(address=8, count=1, unit=unit)
        # if unit == 1:
        return read.__dict__['registers'][0] if 'registers' in read.__dict__ else None
        # return float(read.registers[0])/10 if read.registers else None
    except:
        return None
read_ans_save_one_device()

# f = open("C:\\Users\Admin\Desktop\InformationSQLserver.txt", "r+")
# SQLserver = f.readlines()
# f.close()
# drive = SQLserver[0].lstrip('Drive: \n')
# server = SQLserver[1].lstrip('Server: \n')
# database = SQLserver[2].lstrip('Database: \n')
# uid = SQLserver[3].lstrip('UID: \n')
# pwd = SQLserver[4].lstrip('PWD: \n')
# print('DRIVER={', drive + '};SERVER=', server + ';DATABASE=', database + ';UID=', uid + ';PWD=', pwd)
