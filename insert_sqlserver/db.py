import pyodbc
from dotenv import dotenv_values
from itertools import groupby


config = dotenv_values(".env")
#
# DRIVER = config['DRIVER']
# SERVER = config['SERVER']
# DATABASE = config['DATABASE']
# UID = config['UID']
# PWD = config['PWD']
DRIVER = 'SQL Server Native Client 11.0'
SERVER = '(local)\SQLEXPRESS08'
DATABASE = 'YDCHeater'
UID = 'sa'
PWD = 'Ydc@2022'
print(config)


class DataBase:
    # get driver
    # driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    # print(driver_names)
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD}')
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_latest_value(sensor_values):
        # make sure the data have sorted
        sorted_data = sorted(sensor_values, key=lambda x: x['machine'])
        # group by sensor id
        result = dict()

        for key, value in groupby(sorted_data, key=lambda x: x['machine']):
            # we have to sorted by id (high to low)
            value = sorted(list(value), key=lambda x: x['id'], reverse=True)
            result[f'machine_{key}'] = value[0]['temp'] if value else None
        return result

    def get_list(self, limit=200):
        # select top 16 * from temperature   order by id desc
        self.cursor.execute(f'select top {limit} * from temperature   order by id desc')
        # self.cursor.execute(f'SELECT * FROM {self.table_name} order by id desc limit {limit}')
        rows = self.cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'temp': row[1],
                'machine': row[2]
            })

        return result

    def insert_one(self, **kwargs):
        # if not kwargs['temp']
        sql = f"""
            insert into {self.table_name} (temp, sensor_id, status) values 
            (
                {kwargs['temp'] if kwargs['temp'] else 'null'},
                {kwargs['sensor_id']},
                {kwargs['status']}
            )
        """
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    """
    see data in table
    """
    db = DataBase(table_name='temperature')
    print(db.get_list())
    """
    to get driver: remove comment and run this code
    """
    # driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    # print(driver_names)

# driver_names = pyodbc.drivers()
# print(driver_names)
