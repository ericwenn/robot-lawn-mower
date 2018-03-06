from getGPS import *



try:
  setupGPS()
  while True:
    gpsCoords = getGPS()

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
stopGPS()
