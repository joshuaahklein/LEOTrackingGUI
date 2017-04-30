# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to grab GPS data!

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

def poll():
    # define seral connection particular to the BU-353S4 GPS Receiver
    ser = serial.Serial(
            port='COM9',	# change to appropriate COM port on your machine!
            baudrate=4800,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
	)

    # check if connection is open (throws exception otherwise)
    ser.isOpen()
    
    # prepare two strings for message parsing
    gpsString = ''
    tempString = ''
    
    #dictionary to check if GPS string is valid
    matches = {}
    matches['$'] = 1
    matches['$G'] = 2
    matches['$GP'] = 3
    matches['$GPG'] = 4
    matches['$GPGG'] = 5
    matches['$GPGGA'] = 6
           
    # flag to kick us out of loop if match is met (if GPGGA is used)
    flag = True

    while(flag):
        #sleep(0.01)    # can implement lazy sleep here, may save CPU cycles
        while ser.inWaiting() > 0:          # if buffer has available data
            tempString += ser.read(1)       # add single char to temp
            if tempString not in matches:   # if temp is no longer matching, clear
                tempString = ''
            elif matches[tempString] == 6:  # if temp matched successfully to the end
                flag = False                # kick us out of loop, we have GPGGA
                break
            
    # initialize GPS string with GPGGA
    gpsString = tempString
    
    # new flag condition is if newline is met; then the message is over
    flag = True
    
    while(flag):
        #sleep(0.01)    # can implement lazy sleep here, may save CPU cycles
        while ser.inWaiting() > 0:          # if buffer has available data
            char = ser.read(1)              # get char without appending
            if char == '\n':                # if char is newline, message is over
                flag = False
                break
            gpsString += char               # if char is not newline, append

    # close serial connection
    ser.close()
    
    # split gpsString on comma as fields are comma separated
    tokens = gpsString.split(',')

    # prepare list, will send as final result
    gps = []

    # if we don't have a GPS fix, return all -1.0 to indicate error
    if tokens[1] == '':
    	gps.append(-1.0)
    	gps.append(-1.0)
    	gps.append(-1.0)
    	gps.append(-1.0)
    	return gps
    
    # add UTC time as float
    gps.append(float(tokens[1]))
    
    # convert latitude to degrees only
    decimal = tokens[2].find('.');
    degrees = tokens[2][:(decimal - 2)]
    minutes = tokens[2][(decimal - 2):]
    degrees = float(degrees) + float(minutes)/60.0
    if(tokens[3] == 'S'):
        degrees *= -1
        
    # add latitude as float
    gps.append(degrees)
    
    # convert longitude to degrees only
    decimal = tokens[4].find('.');
    degrees = tokens[4][:(decimal - 2)]
    minutes = tokens[4][(decimal - 2):]
    degrees = float(degrees) + float(minutes)/60.0
    if(tokens[5] == 'W'):
        degrees *= -1
        
    # add longitude as float
    gps.append(degrees)
    
    # add altitude as float (units are meters)
    gps.append(float(tokens[9]))
    
    # return result
    return gps

gps = poll()
print('UTC time: ' + str(gps[0]))
print('Latitude: ' + str(gps[1]))
print('Longitude: ' + str(gps[2]))
print('Altitude: ' + str(gps[3]))


# GPGGA message format:
#$GPGGA,UTC time,lat,direction,long,direction,fix,#sats,
#horizontal dilution of pos,alt above sea level, units,
#mean sea level at location, units,blank,checksum