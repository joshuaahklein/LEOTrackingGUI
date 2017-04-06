# # -*- coding: utf-8 -*-
# """
# Created on Fri Feb 03 16:07:47 2017

# @author: Amber Baurley
# """

# For Phidgets
from ctypes import *
from time import sleep
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper
from Phidgets.Phidget import PhidgetLogLevel

# For Path Prediction
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
line2 = "1 25544U 98067A   17041.55333126  .00016717  00000-0  10270-3 0  9008"
line3 = "2 25544  51.6430 309.5978 0006847 175.5696 184.5519 15.54335653  2056"
TLElines = TLE.split("\n")
#print(TLElines)

satellite = twoline2rv(line2, line3, wgs72)
position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)
boston = city('Boston') #add coordinates from GPS    
# iss = readtle(line1, line2, line3)
iss = readtle(line1, TLElines[0], TLElines[1])

#GPS Coordinates
bos = Observer()
bos.lon = '-71.038887'
bos.lat = '42.364506'
bos.elevation = 0

#time
start = time() 

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
timestep = 1 #1 is equal to one second
i = 600 #number of steps of path desired

for x in range(0,i): #position matrix
    if x == 0: epoch = start
    else: epoch = epoch    
        
    epoch = epoch + timestep #increase time by time step
    bos.date = datetime.utcfromtimestamp(epoch)
    
    iss.compute(bos) #run computations

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
 
for x in range(0,i-1): #velocity matrix
    velalphatemp = alpha[x+1]-alpha[x]
    velalphatemp = velalphatemp/timestep
    
    velbetatemp = beta[x+1]-beta[x]
    velbetatemp = velbetatemp/timestep

    velalpha.append(velalphatemp)
    velbeta.append(velbetatemp)
    
    print("%s, %s" % (velalphatemp, velbetatemp))
 
for x in range(0,i-2): #acceleration matrix
    accelalphatemp = velalpha[x+1]-velalpha[x]
    accelalphatemp = accelalphatemp/timestep
    
    accelbetatemp = velbeta[x+1]-velbeta[x]
    accelbetatemp = accelbetatemp/timestep

    accelalpha.append(accelalphatemp)
    accelbeta.append(accelbetatemp)
    
    print("%s, %s" % (accelalphatemp, accelbetatemp))

print("PREDICTION DONE")
























# Open Control Loop

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
    #stepper.openPhidget(423840)
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
    stepper.setVelocityLimit(0, 6200)
    stepper.setCurrentLimit(0, 0.26)
    sleep(0.2)
    
    print("Will now move to position 20000...")
    stepper.setTargetPosition(0, 20000)
    while stepper.getCurrentPosition(0) != 20000:
        pass
    
    sleep(0.2)
    
    print("Will now move back to positon 0...")
    stepper.setTargetPosition(0, 0)
    while stepper.getCurrentPosition(0) != 0:
        pass
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

# print("Press Enter to quit....")

# chr = sys.stdin.read(1)

# print("Closing...")

try:
    stepper.setEngaged(0, False)
    sleep(0.1)
    stepper.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")















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
    stepper.setVelocityLimit(0, 6200)
    stepper.setCurrentLimit(0, 0.26)
    sleep(0.2)
    
    print("Will now move to position 20000...")
    stepper.setTargetPosition(0, 20000)
    while stepper.getCurrentPosition(0) != 20000:
        pass
    
    sleep(0.2)
    
    print("Will now move back to positon 0...")
    stepper.setTargetPosition(0, 0)
    while stepper.getCurrentPosition(0) != 0:
        pass
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

# print("Press Enter to quit....")

# chr = sys.stdin.read(1)

# print("Closing...")

try:
    stepper.setEngaged(0, False)
    sleep(0.1)
    stepper.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")











exit(0)









