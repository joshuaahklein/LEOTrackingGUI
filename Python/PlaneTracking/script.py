# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to track some planes!
"""

from __future__ import print_function # Only Python 2.x
import subprocess
import re

# function to extract output of process while it is running
# found at http://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
# all credit to original author
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield str(stdout_line) 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# set up regular expression to filter command line output
pattern = re.compile('^[0-9A-F]{6} ') # might not need final space

# initialize dictionary
planes = {}

# make the magic happen
for line in execute(
        r"C:\Users\zchap_000\Documents\BU_Fall_2016\EC463\RTL-SDR\dump1090-win.1.10.3010.14\dump1090.exe --aggressive --interactive"):
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
        flag = True
        for item in line_l[4:9]:
            if item == '':
                flag = False
        
        # update dictionary
        if flag:
            planes[line_l[0]] = line_l[1:]
        
        # print dictionary
        for plane, parameters in planes.iteritems():
            print("Plane ", plane, " with parameters: ", parameters)
