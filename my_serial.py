from config_environment import BAUDRATE, PORT
from serial import Serial


class AppSerial(Serial):
    ser = Serial(port=PORT, baudrate=BAUDRATE)
    ser.open()

    def write(self, data: dict):
        if not self.ser.is_open:
            self.ser.open()
        else:
            write_data = ''
            for key, value in data.items():
                write_data += f'{key}={value}'
            return super().write(write_data)
        return None
