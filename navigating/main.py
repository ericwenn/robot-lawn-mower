from sensing.sensing import Sensors
import steering.steer as steer
from random import random
from time import sleep
from visualization.printer import print_ultrasound

sensors = Sensors()
steer.setup()

def can_move_forward():
  uss = sensors.get_ultrasound_readings()
  print_ultrasound(uss)

  if uss.freshness() < 0.2:
    print "no fresh"
    return True, 0 # total uncertainty
  
  return uss.verdict() == 1, uss.certainty()

REVOLVE_TIME = 2
def spin():
  time_to_spin = random()*REVOLVE_TIME
  steer.right()
  sleep(time_to_spin)
  steer.stop()

sensors.start()
while(True):
  can_forward, certainty = can_move_forward()

  print "Can move forward", can_forward, "certainty", certainty

  if can_forward:
    if certainty >= .6:
      print "going forward"
      steer.forward()
    else:
      steer.stop()
  else:
    if certainty >= .5:
      spin()
    else:
      steer.stop()
  sleep(.5)
