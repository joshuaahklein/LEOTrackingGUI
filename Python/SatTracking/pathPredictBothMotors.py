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
#from gps import poll

# For Phidgets 
from pprint import pprint
import numpy as np
from ctypes import *
from time import sleep
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper
from Phidgets.Phidget import PhidgetLogLevel
import threading



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
polalpha = []
polbeta = []
alalpha = []
albeta = []
moonalpha = []
moonbeta = []

#epoch = []
#these two lines are hardcoded and will change
timestep = 0.05 #1 is equal to one second
i = 12000 #number of steps of path desired

print("The satellite has to pass over in the next 15 minutes\n")

#Amber will randomly pick three stars (North and two others) and Kyle will have 
#the mount point at them first
for x in range(0,i): #position matrix
    if x == 0: epoch = start
    else: epoch = epoch    
        
    epoch = epoch + timestep #increase time by time step
    bos.date = datetime.utcfromtimestamp(epoch)
    
    #Satellite tracks
    sat.compute(bos) #run computations
    aztemp = degrees(sat.az)
    eltemp = degrees(sat.alt)

    azrad = radians(aztemp)
    elrad = radians(eltemp)

    alphatemp = (degrees(atan((sin(elrad))/((cos(elrad))*(cos(azrad))))))
    if alphatemp > 0:
        if x > 100:
            alphatemp = alphatemp - 180
                                            
    betatemp = degrees(acos((cos(elrad))*(sin(azrad))))

    az.append(aztemp)
    el.append(eltemp)
    alpha.append(alphatemp)
    beta.append(betatemp)
      
    # Star tracks
    # North Star
    polaris = star('Polaris')
    polaris.compute(bos)

    polaztemp = degrees(polaris.az)
    poleltemp = degrees(polaris.alt)

    polazrad = radians(polaztemp)
    polelrad = radians(poleltemp)

    polalphatemp = (degrees(atan((sin(polelrad))/((cos(polelrad))*(cos(polazrad))))))               
    polbetatemp = degrees(acos((cos(polelrad))*(sin(polazrad))))

    polalpha.append(polalphatemp)
    polbeta.append(polbetatemp)
    
    # Orions Belt     
    alnitak = star('Alnitak')
    alnitak.compute(bos)

    alaztemp = degrees(alnitak.az)
    aleltemp = degrees(alnitak.alt)

    alazrad = radians(alaztemp)
    alelrad = radians(aleltemp)

    alalphatemp = (degrees(atan((sin(alelrad))/((cos(alelrad))*(cos(alazrad))))))               
    albetatemp = degrees(acos((cos(alelrad))*(sin(alazrad))))

    alalpha.append(alalphatemp)
    albeta.append(albetatemp)

    # Moon
    moon = Moon()
    moon.compute(bos)

    moonaztemp = degrees(moon.az)
    mooneltemp = degrees(moon.alt)

    moonazrad = radians(moonaztemp)
    moonelrad = radians(mooneltemp)

    moonalphatemp = (degrees(atan((sin(moonelrad))/((cos(moonelrad))*(cos(moonazrad))))))               
    moonbetatemp = degrees(acos((cos(moonelrad))*(sin(moonazrad))))
    
    moonalpha.append(moonalphatemp)
    moonbeta.append(moonbetatemp)


 #   print("%s, %s" % (alphatemp, betatemp))    
    
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
    velalphatemp = alpha[x+1] - alpha[x]
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
#velAlphaConv = np.asarray(velalpha)
#accelAlphaConv = np.asarray(accelalpha)
#velBetaConv = np.asarray(velbeta)
#accelBetaConv = np.asarray(accelbeta)

#Convert to steps
#Use ahAlpha and ahBeta instead once RT is implemented
#for x in range(0,i-1):
#    ans = (velalpha[x]/conversionFactor)*16
#    velAlphaConv[x]=ans
#    ans2 = (velbeta[x]/conversionFactor)*16
#    velBetaConv[x] = ans2


#Future Work: this is currently abs, and has a clunky if statement to change posititon from pos to neg
#Fix this

velAlphaConv =   abs(np.asarray(velalpha, dtype=float)  / conversionFactor*16)
velBetaConv =    abs(np.asarray(velbeta, dtype=float)   / conversionFactor*16)
accelAlphaConv = abs(np.asarray(accelalpha, dtype=float)/ conversionFactor*16)
accelBetaConv =  abs(np.asarray(accelbeta, dtype=float) / conversionFactor*16)

pprint(velAlphaConv)
pprint(accelAlphaConv)
pprint(velBetaConv)
pprint(accelBetaConv)

#exit(1)

#for x in range(0,i-2):
#    ans3 = (accelalpha[x]/conversionFactor)*16
#    accelAlphaConv[x]=ans3

#    ans4 = (accelbeta[x]/conversionFactor)*16
#    accelBetaConv[x] = ans4
#velAlphaConv2 = np.array(velAlphaConv, dtype=int)
#accelAlphaConv2 = np.array(accelAlphaConv, dtype=int)
#velBetaConv2 = np.array(velBetaConv, dtype=int)
#accelBetaConv2 = np.array(accelBetaConv, dtype=int)
########################################################################################################
########################################################################################################
#FUNCTION DEFINITIONS
#Information Display Function
def DisplayDeviceInfo(stepper):
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
    print()

def StepperDetached(e):
    detached = e.device
    print("Stepper %i Detached!" % (detached.getSerialNum()))
    print()

def StepperError(e):
    try:
        source = e.device
        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print()

def StepperCurrentChanged(e):
    # source = e.device
    # print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))
    # print()
    pass
def StepperInputChanged(e):
    source = e.device
    print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))
    print()

def StepperPositionChanged(e):
    # source = e.device
    # print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))
    # print()
    pass

def StepperVelocityChanged(e):
    # source = e.device
    # print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))
    # print()
    pass

def phidgetOpener(stepper, sid):
    try:
        stepper.openPhidget()
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
        DisplayDeviceInfo(stepper)


def  StepperCreate():
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

        # stepper2.setOnAttachHandler(StepperAttached)
        # stepper2.setOnDetachHandler(StepperDetached)
        # stepper2.setOnErrorhandler(StepperError)
        # stepper2.setOnCurrentChangeHandler(StepperCurrentChanged)
        # stepper2.setOnInputChangeHandler(StepperInputChanged)
        # stepper2.setOnPositionChangeHandler(StepperPositionChanged)
        # stepper2.setOnVelocityChangeHandler(StepperVelocityChanged)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Opening phidget object....")

    return stepper



def moveMotors(stepper, velAlphaConv, accelAlphaConv):
    # %% The code that actually tells the motors where to go
    try:

        print("Set the current position as start position...")

        stepper.setCurrentPosition(0, 0)

        sleep(0.1)

        

        print("Set the motor as engaged...")

        stepper.setEngaged(0, True)

        sleep(0.1)

        

        print("The motor will run until it reaches the set goal position...")

        

        stepper.setAcceleration(0, 87543)

        stepper.setVelocityLimit(0, 256)

        stepper.setCurrentLimit(0, 0.26)

        sleep(0.2)

        

        print("Will now move to position primaryTargetPosition...")
        # Sketchy continuous mode
        # maxPos = stepper.getPositionMax(0)
        stepper.setTargetPosition(0, 9999999)
        # if stepper != stepper2:
        #     stepper.setTargetPosition(0, -9999999)
        for x in range(0,i-2):
            #timer = time.clock()
            #while timer < timestep:
            print('vel/accel index',x)
            print(velAlphaConv[x])
            stepper.setVelocityLimit(0, velAlphaConv[x])
            #stepper.setAcceleration(0, accelAlphaConv[x])
            sleep(timestep)
        sleep(0.2)

        print("Will now move back to positon 0...")
        stepper.setVelocityLimit(0, 9999)
        stepper.setTargetPosition(0, 0)

        while stepper.getCurrentPosition(0) != 0:
            sleep(0.01)

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


############################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################################################

#Time code: need to ensure that absolute time is consistent between pathPredict
# gps, and motors

#absTime = poll()
#print(absTime)
#completely BS and arbitrary: replace later with real shit from Amber's RT code
#startTime = 835983465019384705927
#completely BS and arbitrary: replace later with real shit that you figure out
#buffTime = 100
#compTime = startTime - buffTime


#This is where the motors will point the telescope at stars first

#startTime = ahEpoch(0)? (the first one, 0 or 1, whatever)



#Main Program Code
#Create a stepper object

stepper = StepperCreate()
stepper2 = StepperCreate()

#Open each stepper
phidgetOpener(stepper, 423486)
phidgetOpener(stepper2,423840)

#set up multithreading:
threads = []
t = threading.Thread(target=moveMotors, args=(stepper, velAlphaConv, accelAlphaConv))
threads.append(t)
t2 = threading.Thread(target=moveMotors, args=(stepper2, velBetaConv, accelBetaConv))
threads.append(t2)

# Execute motor control code
t.start()
t2.start()

# moveMotors(stepper, velAlphaConv, accelAlphaConv)
# moveMotors(stepper2, velBetaConv, accelBetaConv)

print("Done.")

# ############################################################################################################################################################################################################################################################################
# ####################################################################################################################################################################################################################################################################################################################################################