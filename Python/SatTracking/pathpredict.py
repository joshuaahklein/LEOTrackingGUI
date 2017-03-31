# # -*- coding: utf-8 -*-
# """
# Created on Fri Feb 03 16:07:47 2017

# @author: Amber Baurley
# """

from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
from ephem import *
from math import *
from time import time
from datetime import datetime
import sys
import os

# Get user args from GUI
gpsLat = (sys.argv[1])  
gpsLong = (sys.argv[2]) 
TLE = (sys.argv[3]) 

line1 = "sat"
# line2 = "1 25544U 98067A   17041.55333126  .00016717  00000-0  10270-3 0  9008"
# line3 = "2 25544  51.6430 309.5978 0006847 175.5696 184.5519 15.54335653  2056"
TLElines = TLE.split("\n")
print(TLElines)

satellite = twoline2rv(line2, line3, wgs72)
position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)
boston = city('Boston') #add coordinates from GPS    
# iss = readtle(line1, line2, line3)
iss = readtle(line1, TLElines[0], TLElines[1])

#set up variables
start = time() #add time from GPS
az = []
el = []
alpha = []
beta = []
times = []
timestep = 1 #1 is equal to one second
i = 600 #number of steps of path desired

for x in range(0,i): #position matrix
    if x == 0: epoch = start
    else: epoch = epoch    
        
    epoch = epoch + timestep #increase time by time step
    boston.date = datetime.utcfromtimestamp(epoch)
    
    iss.compute(boston) #run computations

    aztemp = degrees(iss.az)
    eltemp = degrees(iss.alt)

    alphatemp = degrees(atan(sin(eltemp)/(cos(eltemp)*cos(aztemp))))
    betatemp = degrees(acos(cos(eltemp)*sin(aztemp)))
    
    az.append(aztemp)
    el.append(eltemp)
    alpha.append(alphatemp)
    beta.append(betatemp)
    
    #Mod for printing
    print("%s, %s, %s, %s, %s" % (aztemp, eltemp, alphatemp, betatemp, epoch))
   
info = boston.next_pass(iss)
print("Rise time: %s azimuth: %s" % (info[0], info[1]))

velalpha = []
velbeta = []

for x in range(0,i-1): #velocity matrix
    velalphatemp = alpha[x+1]-alpha[x]
    velbetatemp = beta[x+1]-beta[x]

    velalpha.append(velalphatemp)
    velbeta.append(velbetatemp)
    
    print("%s, %s" % (velalphatemp, velbetatemp))
    
print("DONE")