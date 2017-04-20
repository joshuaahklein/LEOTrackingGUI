# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to grab encoder data!

AUTHOR: Zachary Chapasko

NOTE: Must have pySerial installed. Using pip, do "pip install pyserial" in a
command shell.

USE:
gps = poll()

gps will contain a list where element 0 is UTC time, element 1 is lat in degrees,
element 2 is long in degrees, and element 3 is altitude in meters
"""

from time import sleep    # may not be necessary, only used for lazy sleep
import serial

def encoderRead():
    # define seral connection particular to the BU-353S4 GPS Receiver
    ser = serial.Serial(
            port='COM6',	# change to appropriate COM port on your machine!
            baudrate=110,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            rtscts=False
	)
    

    firstStart = int('11111111', 2)
    clock = int('10101010', 2)
    stop = int('10101111', 2)
    #clock = int('01010101', 2)
    #stop = int('11110101', 2)

    # check if connection is open (throws exception otherwise)
    if not ser.isOpen():
        return 'error!'
           
    tempString = ''

    ser.setRTS(True)
    ser.write(firstStart)
    ser.write(clock)
    ser.write(clock)
    ser.write(clock)
    ser.write(stop)
    ser.setRTS(False)
    sleep(1)
    while ser.inWaiting() > 0:          # if buffer has available data
        tempString += ser.read(1) + ' ' # add 3 bytes
        print('here')
    ser.close()
    return tempString
        
pos = encoderRead()
print('Encoder position: ' + pos)


# GPGGA message format:
#$GPGGA,UTC time,lat,direction,long,direction,fix,#sats,
#horizontal dilution of pos,alt above sea level, units,
#mean sea level at location, units,blank,checksum