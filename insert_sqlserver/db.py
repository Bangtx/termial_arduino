import pyodbc
from dotenv import dotenv_values

config = dotenv_values(".env")

DRIVER = config['DRIVER']
SERVER = config['SERVER']
DATABASE = config['DATABASE']
UID = config['UID']
PWD = config['PWD']
print(config)


class DataBase:
    # get driver
    # driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    # print(driver_names)
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD}')
        self.cursor = self.conn.cursor()

    def get_list(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = self.cursor.fetchall()
        return rows

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
