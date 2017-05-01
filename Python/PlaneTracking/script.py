# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to track some planes!
"""

from __future__ import print_function # Only Python 2.x
import subprocess
import re

planeProcess = 0

# function to extract output of process while it is running
# found at http://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
# all credit to original author
def execute(cmd):
    global planeProcess
    planeProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(planeProcess.stdout.readline, ""):
        yield str(stdout_line) 
    planeProcess.stdout.close()
    return_code = planeProcess.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# set up regular expression to filter command line output
pattern = re.compile('^[0-9A-F]{6} ') # might not need final space

# initialize dictionary
planes = {}

path = str(os.getcwd)
path += "dump1090.exe --aggressive --interactive"

# prediction lists
alt = []
spd = []
hdg = []
lat = []
lon = []

# total values for calculating delta
altTotal = 0
spdTotal = 0
hdgTotal = 0
latTotal = 0
lonTotal = 0

# temp values
altTemp = -1
spdTemp = -1
hdgTemp = -1
latTemp = -1
lonTemp = -1

# iterator
it = 0

# how many prior frames are taken into account in prediction
lockOnFrames = 40
predictionFrames = 20
divisor = float(predictionFrames)

# if we have selected a particular plane
lockOn = False

# make the magic happen
for line in execute(
            #r"C:\Users\zchap_000\Documents\BU_Fall_2016\EC463\RTL-SDR\dump1090-win.1.10.3010.14\dump1090.exe --aggressive --interactive"
            path
            ):
    
    # if we haven't locked on, search all planes
    if not lockOn:
        # check if we have a line that contains plane info
        match = re.match(pattern, line)
        
        # if the line contains plane info, move on
        if match:
            
            # format plane info into human- and computer-readable format
            line_l = list(line)
            line_l[6] = ','
            line_l[12] = ','
            line_l[18] = ','
            line_l[28] = ','
            line_l[35] = ','
            line_l[40] = ','
            line_l[45] = ','
            line_l[54] = ','
            line_l[63] = ','
            line_l[68] = ','
            line_l[75] = ','
            line = ''.join(line_l)
            line_l = line.split(',')
            for i, s in enumerate(line_l):
                line_l[i] = s.strip()
            
            # line_l contains a list of strings that correspond to ADS-B fields
            # if certain fields are blank, we don't care about the plane at all
            reqFields = True
            for item in line_l[4:9]:
                if item == '':
                    reqFields = False
            
            # update dictionary
            if reqFields:
                if (int(line_l[10]) >= lockOnFrames):
                    lockOn = True
                    lockedPlane = line_l[0]
                    print('Lock-on acquired with ' + line_l[10] + ' frames!')
                
                
                '''
                planes[line_l[0]] = line_l[1:]
            
            # print dictionary
            for plane, parameters in planes.iteritems():
                print("Plane ", plane, " with parameters: ", parameters)
                
                # if we have been seeing plane for a while (10 secs), lock on
                if (int(parameters[9]) >= lockOnFrames):
                    lockOn = True
                    lockedPlane = plane
                    print('Lock-on acquired with ' + parameters[9] + ' frames!')
                    break'''
                    
    else:
        # check if we have a line that contains plane info
        match = line[0:6]
    
        # if the line contains plane info, move on
        if match == lockedPlane:
            # format plane info into human- and computer-readable format
            line_l = list(line)
            line_l[6] = ','
            line_l[12] = ','
            line_l[18] = ','
            line_l[28] = ','
            line_l[35] = ','
            line_l[40] = ','
            line_l[45] = ','
            line_l[54] = ','
            line_l[63] = ','
            line_l[68] = ','
            line_l[75] = ','
            line = ''.join(line_l)
            line_l = line.split(',')
            for i, s in enumerate(line_l):
                line_l[i] = s.strip()
            
            # line_l contains a list of strings that correspond to ADS-B fields
            # if certain fields are blank, we don't care about the plane at all
            reqFields = True
            for item in line_l[4:9]:
                if item == '':
                    reqFields = False
                    
            if reqFields:
                if len(alt) < predictionFrames:
                    if altTemp != -1:
                        altTemp = int(line_l[4]) - altTemp
                        spdTemp = int(line_l[5]) - spdTemp
                        hdgTemp = int(line_l[6]) - hdgTemp
                        latTemp = float(line_l[7]) - latTemp
                        lonTemp = float(line_l[8]) - lonTemp
                        
                        alt.append(altTemp)
                        spd.append(spdTemp)
                        hdg.append(hdgTemp)
                        lat.append(latTemp)
                        lon.append(lonTemp)
                    
                        altTotal += altTemp
                        spdTotal += spdTemp
                        hdgTotal += hdgTemp
                        latTotal += latTemp
                        lonTotal += lonTemp
                        
                    altTemp = int(line_l[4])
                    spdTemp = int(line_l[5])
                    hdgTemp = int(line_l[6])
                    latTemp = float(line_l[7])
                    lonTemp = float(line_l[8])
                else:
                    altTotal -= alt[it]
                    spdTotal -= spd[it]
                    hdgTotal -= hdg[it]
                    latTotal -= lat[it]
                    lonTotal -= lon[it]
                    
                    altTemp = int(line_l[4]) - altTemp
                    spdTemp = int(line_l[5]) - spdTemp
                    hdgTemp = int(line_l[6]) - hdgTemp
                    latTemp = float(line_l[7]) - latTemp
                    lonTemp = float(line_l[8]) - lonTemp
                                   
                    altTotal += altTemp
                    spdTotal += spdTemp
                    hdgTotal += hdgTemp
                    latTotal += latTemp
                    lonTotal += lonTemp
                    
                    alt[it] = altTemp
                    spd[it] = spdTemp
                    hdg[it] = hdgTemp
                    lat[it] = latTemp
                    lon[it] = lonTemp
                    '''
                    print('Delta values for frame ' + str(it) + ':')
                    print('Alt: ' + str(alt[it]) + ' Spd: ' + str(spd[it]) +
                          ' Hdg: ' + str(hdg[it]) + ' Lat: ' + str(lat[it]) +
                          ' Lon: ' + str(lon[it]))
                    print()
                       
                    '''
                    
                    print('Actual values for frame ' + str(it) + ':')
                    print('Alt: ' + line_l[4])
                    print('Spd: ' + line_l[5])
                    print('Hdg: ' + str(int(line_l[6])))
                    print('Lat: ' + line_l[7])
                    print('Lon: ' + line_l[8])
                    print()
                    
                    it += 1
                    if it == predictionFrames:
                        it = 0
                    
                    if it == 0:
                        for pos in range(predictionFrames):
                            # '{:<30}'.format('left aligned')
                            print('Frame ' + '{:>2}'.format(str(pos)) + ' |' +
                                  ' Alt: ' + str((float(line_l[4]) + (pos + 1)*(float(altTotal) / divisor))) + 
                                  ', Spd: ' + str((float(line_l[5]) + (pos + 1)*(float(spdTotal) / divisor))) +
                                  ', Hdg: ' + str((float(line_l[6]) + (pos + 1)*(float(hdgTotal) / divisor))) +
                                  ', Lat: ' + str((float(line_l[7]) + (pos + 1)*(float(latTotal) / divisor))) +
                                  ', Lon: ' + str((float(line_l[8]) + (pos + 1)*(float(lonTotal) / divisor))))
                    
                    print()
                    
                    altTemp = int(line_l[4])
                    spdTemp = int(line_l[5])
                    hdgTemp = int(line_l[6])
                    latTemp = float(line_l[7])
                    lonTemp = float(line_l[8])
