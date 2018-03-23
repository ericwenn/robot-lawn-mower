from sensing.sensing import Sensors
import steering.steer as steer
from random import random
from time import sleep

sensors = Sensors()
steer.setup()

def can_move_forward():
  uss = sensors.get_ultrasound_readings()
  if not uss.freshness() < 0.2:
    return True, 0 # total uncertainty
  
  return uss.verdict() == 1, uss.certainty()

REVOLVE_TIME = 2
def spin():
  time_to_spin = random()*REVOLVE_TIME
  steer.right()
  sleep(time_to_spin)
  steer.stop()

while(True):
  can_forward, certainty = can_move_forward()

  if can_forward:
    if certainty >= .6:
      steer.forward()
    else:
      steer.stop()
  else:
    if certainty >= .5:
      spin()
    else:
      steer.stop()
