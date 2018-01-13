#!/usr/bin/env python -u
"""
Usage: tempy.py

A simple Python script that periodically 
reads data  from a temperature sensor on
a Raspberry Pi and writes it together with
the current time (in Unix Time Stamp) to
an SQLite database called tempy.db.
"""

import os
import glob
import time
import datetime
import sqlite3 as sqlite
import sys


os.system('modprobe w1-gpio')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

con = sqlite.connect('tempy.db')

def tempy_data_write(date, temp):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO data(time, temperature) VALUES(?, ?)", (date, temp))

def tempy_read_raw_data():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def tempy_read_data():
    lines = tempy_read_raw_data()

    while lines[0].strip()[-3:] != 'YES':
      time.sleep(1)
      lines = tempy_read_raw_data()

    equals_pos = lines[1].find('t=')

    if equals_pos != 1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    current_time_ut = time.time()
    current_time_rt = datetime.datetime.fromtimestamp(current_time_ut).strftime('%Y-%m-%d %H:%M:%S')
    temp = tempy_read_data()
    tempy_data_write(current_time_ut, temp)
    time.sleep(899)

