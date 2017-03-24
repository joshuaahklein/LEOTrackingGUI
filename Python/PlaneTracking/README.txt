How to use the plane tracking module

FIRST TIME USAGE:

1. Plug in the RTL-SDR and antenna into the computer into a USB that you particularly like
2. DO NOT install any drivers that Windows suggests for the RTL
3. Run zadig_2.2.exe, select the RTL from the drop-down menu, and install the driver

Somwhat optional (for NTP time protocol, supposedly more accurate than Windows):
4. Run ntp-4.2.8p8-win32-setup.exe and follow the instructions
5. Restart device, probably (will allow zadig/RTL stuff to take effect as well as NTP stuff)
6. Open Task Manager, go to Services tab, stop the W32Time service, start the NTP service


SUBSEQUENT USAGE:

1. Plug in RTL-SDR into the USB port that you originally used
2. Verify in script.py that the path is correct (if using absolute path, change to current directory)
3. Run script.py
4. Enjoy!