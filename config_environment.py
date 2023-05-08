from dotenv import dotenv_values

config = dotenv_values(".env")

PORT = config['PORT']
BAUDRATE = config['BAUDRATE']
