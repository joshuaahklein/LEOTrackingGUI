#temp.py
# # -*- coding: utf-8 -*-
# """
# Created on Fri Feb 03 16:07:47 2017

# @author: Amber Baurley
# """
# For Path Prediction
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
from ephem import *
from math import *
import time
from datetime import datetime
import sys
import os

# For GPS Stuff
from gps import poll

# For Phidgets
from pprint import pprint
import numpy as np
import thread
from ctypes import *
from time import sleep
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper
from Phidgets.Phidget import PhidgetLogLevel



# Get user args from GUI
#gpsLat = (sys.argv[1])  
#gpsLong = (sys.argv[2]) 
#TLE = (sys.argv[3]) 

line1 = "sat"
line2 = "1 37820U 11053A   17108.75840766  .00019738  00000-0  12544-3 0  9997"
line3 = "2 37820  42.7593 203.1960 0018230  12.5951 125.9337 15.75851115318584"
#TLElines = TLE.split("\n")
#print(TLElines)

# satellite = twoline2rv(line2, line3, wgs72)
# position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)
#boston = city('Boston') #add coordinates from GPS    
iss = readtle(line1, line2, line3)
#iss = readtle(line1, TLElines[0], TLElines[1])

#GPS Coordinates
#Need to adapt this to call Zach's code
# i.e. bos.lon = gps.poll.long
#replace V


bos = Observer()
bos.lon = '-71.038887'
bos.lat = '42.364506'
bos.elevation = 0

#This is hard-coded, and will be replaced with RT code
date_time = '19.04.2017 05:04:33'
pattern = '%d.%m.%Y %H:%M:%S'
epoch1 = int(time.mktime(time.strptime(date_time, pattern)))

#time
#Start will = Now()
start = epoch1 

#satellite = twoline2rv(line2, line3, wgs72)
#position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)
#boston = city('Boston') #add coordinates from GPS    

#set up variables
az = []
el = []
alpha = []
beta = []
velalpha = []
velbeta = []
accelalpha = []
accelbeta = []
times = []
#epoch = []
#these two lines are hardcoded and will change
timestep = 0.05 #1 is equal to one second
i = 6000 #number of steps of path desired

print("The satellite has to pass over in the next two hours\n")

#Amber will randomly pick three stars (North and two others) and Kyle will have 
#the mount point at them first
for x in range(0,i): #position matrix
    if x == 0: epoch = start
    else: epoch = epoch    
        
    epoch = epoch + timestep #increase time by time step
    bos.date = datetime.utcfromtimestamp(epoch)
    
    iss.compute(bos) #run computations

    aztemp = degrees(iss.az)
    eltemp = degrees(iss.alt)

    azrad = radians(aztemp)
    elrad = radians(eltemp)

    alphatemp = (degrees(atan((sin(elrad))/((cos(elrad))*(cos(azrad))))))
    # if alphatemp < 0:
    #     alphatemp = alphatemp + 180
                                            
    betatemp = degrees(acos((cos(elrad))*(sin(azrad))))

    az.append(aztemp)
    el.append(eltemp)
    alpha.append(alphatemp)
    beta.append(betatemp)
    
    #Mod for printing
    #print("%s, %s, %s, %s, %s" % (aztemp, eltemp, alphatemp, betatemp, epoch))
 
# ^ will run for two full hours
# From that, there wil be another for loop of selecting values of alpha 
# above zero (where the sat is above the horizon)

#The first point of ahAlph (above-horizon +/- 5 degrees) will indicate the motor start point
#ahAlpha, ahBeta, and ahEpoch will be separate arrays.  Kyle will use these numbers 
# as the actual path for the motors to point the telescope, starting 5 degrees below
#the starting horizon, and ending 5 degrees below the ending horizon.

for x in range(0,i-1): #velocity matrix
    velalphatemp = alpha[x+1]-alpha[x]
    velalphatemp = velalphatemp/timestep
    
    velbetatemp = beta[x+1]-beta[x]
    velbetatemp = velbetatemp/timestep

    velalpha.append(velalphatemp)
    velbeta.append(velbetatemp)
    
    #print("%s, %s" % (velalphatemp, velbetatemp))
for x in range(0,i-2): #acceleration matrix
    accelalphatemp = velalpha[x+1]-velalpha[x]
    accelalphatemp = accelalphatemp/timestep
    
    accelbetatemp = velbeta[x+1]-velbeta[x]
    accelbetatemp = accelbetatemp/timestep

    accelalpha.append(accelalphatemp)
    accelbeta.append(accelbetatemp)
    
    #print("%s, %s" % (accelalphatemp, accelbetatemp))

print("PREDICTION DONE")




##########################################################################################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################


# Control Loop
# Author- Kyle Hughes

#Conversion factor: 1 step = .018 degrees.  With this I can convert Amber's track into motor code that actualy uses her data.
conversionFactor = 0.018

#Convert alphatemp and betatemp to float arrays so they can be converted to steps and 
velAlphaConv = np.array(velalpha, dtype=int)
accelAlphaConv = np.array(accelalpha, dtype=int)
#pprint(alphaConv)
velBetaConv = np.array(velbeta, dtype=int)
accelBetaConv = np.array(accelbeta, dtype=int)
#pprint(velBetaConv)

#Convert to steps
#Use ahAlpha and ahBeta instead once RT is implemented
for x in range(1,(i)):
    ans = (velAlphaConv[x]/conversionFactor)*16
    velAlphaConv[x]=ans

    ans2 = (velBetaConv[x]/conversionFactor)*16
    velBetaConv[x] = ans2

for x in range(2,(i)):
    ans = (accelAlphaConv[x]/conversionFactor)*16
    accelAlphaConv[x]=ans3

    ans4 = (accelBetaConv[x]/conversionFactor)*16
    accelBetaConv[x] = ans4

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

#pprint(alphaConv)
#pprint(betaConv)

#def alphaAxis(threadName):

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (stepper.isAttached(), stepper.getDeviceName(), stepper.getSerialNum(), stepper.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Motors: %i" % (stepper.getMotorCount()))

#Event Handler Callback Functions
def StepperAttached(e):
    attached = e.device
    print("Stepper %i Attached!" % (attached.getSerialNum()))

def StepperDetached(e):
    detached = e.device
    print("Stepper %i Detached!" % (detached.getSerialNum()))

def StepperError(e):
    try:
        source = e.device
        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def StepperCurrentChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))

def StepperInputChanged(e):
    source = e.device
    print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))

def StepperPositionChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))

def StepperVelocityChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

############################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################################################

# #Time code: need to ensure that absolute time is consistent between pathPredict
# # gps, and motors

# absTime = poll()
# print(absTime)
# #completely BS and arbitrary: replace later with real shit from Amber's RT code
# startTime = 835983465019384705927
# #completely BS and arbitrary: replace later with real shit that you figure out
# buffTime = 100
# compTime = startTime - buffTime


#taking into account the separation of the telescope from the x-y plane,
# and the lens from the z axis
#offsetSteps = 1370.889


#This is where the motors will point the telescope at stars first

#startTime = ahEpoch(0)? (the first one, 0 or 1, whatever)



# while compTime > absTime:
#     sleep(1)




# primaryTargetPosition = -50000

#INITIAL PRIMARY AXIS MOVEMENT
#Main Program Code
#Create a stepper object
try:
    stepper = Stepper()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

try:
    #logging example, uncomment to generate a log file
    #stepper.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")

    stepper.setOnAttachHandler(StepperAttached)
    stepper.setOnDetachHandler(StepperDetached)
    stepper.setOnErrorhandler(StepperError)
    stepper.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper.setOnInputChangeHandler(StepperInputChanged)
    stepper.setOnPositionChangeHandler(StepperPositionChanged)
    stepper.setOnVelocityChangeHandler(StepperVelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    stepper.openPhidget(423486)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    stepper.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        stepper.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    #The code that actually tells the motors where to go

    print("Set the current position as start position...")

    stepper.setCurrentPosition(0, 0)

    sleep(0.1)

    

    print("Set the motor as engaged...")

    stepper.setEngaged(0, True)

    sleep(0.1)

    

    print("The motor will run until it reaches the set goal position...")

    

    stepper.setAcceleration(0, 1000000)

    stepper.setVelocityLimit(0, 6200)

    stepper.setCurrentLimit(0, 0.26)

    sleep(0.2)

    # Rachet AF continuous mode
    #maxPos = stepper.getPositionMax(0)
    stepper.setTargetPosition(0, 999999999)
    for x in range(2,i):
        timer = time.clock()
        while timer < timestep:
            stepper.setVelocityLimit(0, velAlphaConv[x])
            stepper.setAcceleration(0, accelAlphaConv[x])


    print("Will now move back to positon 0...")

    stepper.setTargetPosition(0, 0)

    while stepper.getCurrentPosition(0) != 0:

        pass

    try:
        stepper.setEngaged(0, False)
        sleep(0.1)
        stepper.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
#threadName.exit()
#############################################################################################################################################################################################################################################################################
#####################################################################################################################################################################################################################################################################################################################################################
#def betaAxis(threadName):
#Information Display Function
# def DisplayDeviceInfo():
#     print("|------------|----------------------------------|--------------|------------|")
#     print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
#     print("|------------|----------------------------------|--------------|------------|")
#     print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (stepper.isAttached(), stepper.getDeviceName(), stepper.getSerialNum(), stepper.getDeviceVersion()))
#     print("|------------|----------------------------------|--------------|------------|")
#     print("Number of Motors: %i" % (stepper.getMotorCount()))

# #Event Handler Callback Functions
# def StepperAttached(e):
#     attached = e.device
#     print("Stepper %i Attached!" % (attached.getSerialNum()))

# def StepperDetached(e):
#     detached = e.device
#     print("Stepper %i Detached!" % (detached.getSerialNum()))

# def StepperError(e):
#     try:
#         source = e.device
#         print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
#     except PhidgetException as e:
#         print("Phidget Exception %i: %s" % (e.code, e.details))

# def StepperCurrentChanged(e):
#     source = e.device
#     print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))

# def StepperInputChanged(e):
#     source = e.device
#     print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))

# def StepperPositionChanged(e):
#     source = e.device
#     print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))

# def StepperVelocityChanged(e):
#     source = e.device
#     print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

######################################################################################################
######################################################################################################

# #Time code: need to ensure that absolute time is consistent between pathPredict
# # gps, and motors

# absTime = poll()
# print(absTime)
# #completely BS and arbitrary: replace later with real shit from Amber's RT code
# startTime = 835983465019384705927
# #completely BS and arbitrary: replace later with real shit that you figure out
# buffTime = 100
# compTime = startTime - buffTime


#taking into account the separation of the telescope from the x-y plane,
# and the lens from the z axis

#SECONDARY AXIS MOVEMENT
#Create a stepper object
try:
    stepper = Stepper()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

try:
    #logging example, uncomment to generate a log file
    #stepper.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")

    stepper.setOnAttachHandler(StepperAttached)
    stepper.setOnDetachHandler(StepperDetached)
    stepper.setOnErrorhandler(StepperError)
    stepper.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper.setOnInputChangeHandler(StepperInputChanged)
    stepper.setOnPositionChangeHandler(StepperPositionChanged)
    stepper.setOnVelocityChangeHandler(StepperVelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    # stepper.openPhidget(423486)
    stepper.openPhidget(423840)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    stepper.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        stepper.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Set the current position as start position...")

    stepper.setCurrentPosition(0, 0)

    sleep(0.1)
    

    print("Set the motor as engaged...")

    stepper.setEngaged(0, True)

    sleep(0.1)
    

    print("The motor will run until it reaches the set goal position...")

    stepper.setAcceleration(0, 87543)

    stepper.setVelocityLimit(0, 1600)

    stepper.setCurrentLimit(0, 0.26)

    sleep(0.2)

    

    print("Will now move to goal position ...")

    stepper.setTargetPosition(0, 999999999)
    for x in range(2,i):
    timer = time.clock()
    while timer < timestep:
        stepper.setVelocityLimit(0, velBetaConv[x])
        stepper.setAcceleration(0, accelBetaConv[x])
    sleep(0.2)

    stepper.setVelocityLimit(0, 7200)

    
    print("Will now move back to positon 0...")

    stepper.setTargetPosition(0, 0)

    while stepper.getCurrentPosition(0) != 0:

        pass
    
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        stepper.setEngaged(0, False)
        sleep(0.1)
        stepper.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    # threadName.exit()
########################################################################
########################################################################
# try:
#     thread.start_new_thread( alphaAxis, ("alphaThread", 0))
#     thread.start_new_thread( betaAxis, ("betaThread", 0))
exit(0)