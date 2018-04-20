from sensing.sensing import Sensors
from sensing.sensor_reading import UltraSoundSensorReading
import steering.steer as steer
from random import random
from time import sleep
from visualization.printer import create_visualizer
from configuration.config_listener import ConfigListener
import atexit

sensors = Sensors()
vis = create_visualizer()
conf = ConfigListener(8085)
atexit.register(vis.cleanup)

def can_move_forward():
  uss = sensors.get_ultrasound_readings()
  css = sensors.get_camera_readings()
  grs = sensors.get_gps_readings()

  #if len(grs.raw()) > 0:
    #print grs.raw()
    #conf.register_position(grs.raw()[0]['payload']['coords'])
  
  vis.register_reading('Camera', 'camera', css)
  vis.register_reading('Ultrasound', 'ultrasound', uss)
  vis.register_reading('GPS', 'gps', grs)


  if uss.freshness() < 0.2:
    return True, 0 # total uncertainty
  
  can_forward = uss.verdict() == 1
  certainty = uss.certainty()

  vis.register_reading('Can move forward', 'can_move_forward', (can_forward, certainty))
  return can_forward, certainty

REVOLVE_TIME = 2
def spin():
  # spin atleast .2s
  time_to_spin = random()*REVOLVE_TIME
  steer.back()
  sleep(2)
  steer.right()
  sleep(time_to_spin)
  steer.stop()


def main():
  steer.setup()
  sensors.start()
  while(True):
    can_forward, certainty = can_move_forward()

    vis.render()    
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
