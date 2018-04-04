from sensing.sensing import Sensors
from sensing.sensor_reading import UltraSoundSensorReading
import steering.steer as steer
from random import random
from time import sleep
from visualization.printer import create_visualizer
import atexit

sensors = Sensors()

vis = create_visualizer()
atexit.register(vis.cleanup)

def can_move_forward():
  uss = sensors.get_ultrasound_readings()
  
  vis.register_reading('Ultrasound', 'ultrasound', uss)
  vis.render()
  if uss.freshness() < 0.2:
    return True, 0 # total uncertainty
  
  return uss.verdict() == 1, uss.certainty()

REVOLVE_TIME = 2
def spin():
  time_to_spin = random()*REVOLVE_TIME
  steer.back()
  sleep(1)
  steer.right()
  sleep(time_to_spin)
  steer.stop()


def main():
  steer.setup()
  sensors.start()
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
    sleep(.001)

if __name__ == "__main__":
  main()