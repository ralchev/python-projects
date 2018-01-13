#!/usr/bin/env python -u

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

connection = sqlite.connect('tempy.db')

def tempy_data_write(date, temp):
    with connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO data(time, temperature) VALUES(?, ?)", (date, temp))

def tempyReadRawData():
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def tempyReadData():
    lines = tempyReadRawData()

    while lines[0].strip()[-3:] != 'YES':
      time.sleep(1)
      lines = tempyReadRawData()

    equalsPos = lines[1].find('t=')

    if equalsPos != 1:
        tempString = lines[1][equalsPos+2:]
        tempC = float(tempString) / 1000.0
        return tempC

while True:
    currentTimeUT = time.time()
    currentTimeRT = datetime.datetime.fromtimestamp(currentTimeUT).strftime('%Y-%m-%d %H:%M:%S')
    temp = tempyReadData()

    tempyDataWrite(currentTimeUT, temp)
    time.sleep(899)
