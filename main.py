import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

wd = tk.Tk()
wd.title('Setting Alarm')
wd.geometry("500x150")
wd.minsize(500, 150)
wd.maxsize(500, 150)

machines = ('Machine1',
            'Machine2',
            'Machine3',
            'Machine4',
            'Machine5',
            'Machine6',
            'Machine7',
            'Machine8',
            'Machine9',
            'Machine10',
            'Machine11',
            'Machine12',
            'Machine13',
            'Machine14',
            'Machine15',
            'Machine16'
            )
default_value_combobox = 0


def get_all_value(cursor):
    result = []
    sql = "SELECT * FROM alarm_setting WHERE 1"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        id, machine, host, port, unit, low, high = i
        result.append({
            'id': id,
            'machine': machine,
            'host': host,
            'port': port,
            'unit': unit,
            'low': low,
            'high': high
        })
    return result


def get_old_value(cursor, machine):
    sql = f"SELECT * FROM alarm_setting WHERE machine = '{machine}'"
    cursor.execute(sql)
    data = cursor.fetchall()  # only one
    if not data:
        return
    id, machine, host, port, unit, low, high = data[0]
    return {
        'id': id,
        'machine': machine,
        'host': host,
        'port': port,
        'unit': unit,
        'low': low,
        'high': high
    }


def insert_default_value(connect, cursor):
    cursor.execute("""INSERT INTO alarm_setting(id, machine, low, high)
        VALUES (1,'Machine1', 400, 700),
                (2,'Machine2', 400, 700),
                (3,'Machine3', 400, 700),
                (4,'Machine4', 400, 700),
                (5,'Machine5', 400, 700),
                (6,'Machine6', 400, 700),
                (7,'Machine7', 400, 700),
                (8,'Machine8', 400, 700),
                (9,'Machine9', 400, 700),
                (10,'Machine10', 400, 700),
                (11,'Machine11', 400, 700),
                (12,'Machine12', 400, 700),
                (13,'Machine13', 400, 700),
                (14,'Machine14', 400, 700),
                (15,'Machine15', 400, 700),
                (16,'Machine16',400, 700)
    """)
    connect.commit()


class window:
    def __init__(self, master1):
        self.conn = sqlite3.connect('setting.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS alarm_setting (
                    id integer PRIMARY KEY,
                    machine text NOT NULL,
                    host text,
                    port integer,
                    unit integer,
                    low integer,
                    high integer
                );
                
        """)
        self.conn.commit()
        # get old value
        old_setup_value = get_old_value(self.c, machines[default_value_combobox])
        if not old_setup_value:  # appear at the first time
            # insert default
            insert_default_value(self.conn, self.c)
            old_setup_value = get_old_value(self.c, machines[default_value_combobox])
        print(old_setup_value)
        self.n = tk.StringVar()
        self.panel2 = tk.Frame(master1)
        self.panel2.pack(fill="both", expand=True, padx=20, pady=20)
        self.machineLabel = tk.Label(self.panel2, text="Machine:")
        self.machineLabel.grid(column=1, row=0)
        self.low_alarmLabel = tk.Label(self.panel2, text="Low:")
        self.low_alarmLabel.grid(column=2, row=0)
        self.high_alarmLabel = tk.Label(self.panel2, text="High:")
        self.high_alarmLabel.grid(column=3, row=0)
        self.saveButton = tk.Button(self.panel2, text="Save", command=self.save)
        self.saveButton.grid(column=2, row=2)

        self.machineCombobox = ttk.Combobox(self.panel2, width=27, textvariable=self.n)
        self.machineCombobox['values'] = machines
        self.machineCombobox.grid(column=1, row=1)
        self.machineCombobox.current(default_value_combobox)
        self.machineCombobox.bind('<<ComboboxSelected>>', self.on_select_combobox)

        vcmd = (master1.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.low_alarmEntry = tk.Entry(self.panel2, validate='key', validatecommand=vcmd)
        self.low_alarmEntry.insert(0, old_setup_value['low'])
        self.low_alarmEntry.grid(column=2, row=1)
        self.low_alarmEntry.focus()

        self.high_alarmEntry = tk.Entry(self.panel2, validate='key', validatecommand=vcmd)
        self.high_alarmEntry.insert(0, old_setup_value['high'])
        self.high_alarmEntry.grid(column=3, row=1)
        self.high_alarmEntry.focus()

    def on_select_combobox(self, event):
        # get old value of this machine
        old_value = get_old_value(self.c, self.machineCombobox.get())
        # remove old value
        self.low_alarmEntry.delete(0, len(self.low_alarmEntry.get()))
        self.high_alarmEntry.delete(0, len(self.high_alarmEntry.get()))
        # update new value
        self.low_alarmEntry.insert(0, old_value['low'])
        self.high_alarmEntry.insert(0, old_value['high'])

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed == '':
            return True
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def save(self):
        # validate input
        if self.high_alarmEntry.get() == '' or self.low_alarmEntry.get() == '':
            messagebox.showerror('Error', 'please input enough')
            return
        get_machine = self.machineCombobox.get()
        print(get_machine)
        get_low_alarm = self.low_alarmEntry.get()
        get_high_alarm = self.high_alarmEntry.get()
        self.conn = sqlite3.connect('setting.db')
        self.c = self.conn.cursor()
        sql_Query = "SELECT low, high FROM alarm_setting WHERE machine = %s"
        self.c.execute(sql_Query, (get_machine,))
        a = self.c.fetchall()
        print(a)

        self.low_alarmEntry.delete(0, 'end')
        self.high_alarmEntry.delete(0, 'end')


window(wd)
wd.mainloop()