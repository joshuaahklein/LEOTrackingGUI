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

x = (sys.argv[1])  
y = (sys.argv[2]) 
z = (sys.argv[3])
w = (sys.argv[4])
print("Args received: " + x + " " + y + " " + z + " " + w)


line1 = ('1 00005U 58002B   00179.78495062 +.00000023 +00000-0 +28098-4 0  4753')
line2 = ('2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667')

satellite = twoline2rv(line1, line2, wgs72)
position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)

#print(satellite.error)    # nonzero on error
#print(satellite.error_message)
#print(position)
#print(velocity)

boston = city('Boston') #add coordinates from GPS            
line = []
 
#print("got this far")

with open ('ISStle.txt') as f:
    for l in f:
        line.append(l.split("\n"))
line1a = str(line[0][0])
line2a = str(line[1][0])
line3a = str(line[2][0])
f.close()

print("got this far")

line1 = "ISS"
line2 = "1 25544U 98067A   17041.55333126  .00016717  00000-0  10270-3 0  9008"
line3 = "2 25544  51.6430 309.5978 0006847 175.5696 184.5519 15.54335653  2056"
iss = readtle(line1a, line2a, line3a)

#set up variables
start = time() #add time from GPS
az = []
el = []
alpha = []
beta = []
times = []
timestep = 1 #1 is equal to one second
i = 600 #number of steps of path desired


print("got this far")

for x in range(0,i): #position matrix
    if x == 0:
        epoch = start
        file = open("ISSpos.txt","w")
    else:
        epoch = epoch    
        file = open("ISSpos.txt","a")
        
    epoch = epoch + timestep #increase time by time step
    boston.date = datetime.utcfromtimestamp(epoch)
    
    iss.compute(boston) #run computations

    #ra = degrees(iss.ra)
    #dec = degrees(iss.dec)

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


    file.write("%s, %s, %s, %s, %s\n" % (aztemp, eltemp, alphatemp, betatemp, epoch))
    file.close()
   
info = boston.next_pass(iss)
print("Rise time: %s azimuth: %s" % (info[0], info[1]))

velalpha = []
velbeta = []

for x in range(0,i-1): #velocity matrix
    if x == 0:
        file = open("ISSvel.txt","w")
    else:
        file = open("ISSvel.txt","a")
#    
#do we need this? check ranges   
#    if alpha[x+1] >= 0 and \
#       alpha[x] >= 0:
#            velalphatemp = alpha[x+1]-alpha[x]
#            velbetatemp = beta[x+1]-beta[x]
#    elif alpha[x+1] >= 0 and \
#         alpha[x] <= 0:
#             velalphatemp = 
             
    velalphatemp = alpha[x+1]-alpha[x]
    velbetatemp = beta[x+1]-beta[x]

    velalpha.append(velalphatemp)
    velbeta.append(velbetatemp)
    
    file.write("%s, %s\n" % (velalphatemp, velbetatemp))
    file.close()
    
print("DONE")