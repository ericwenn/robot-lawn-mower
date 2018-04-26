from sensing.sensing import Sensors
from sensing.sensor_reading import UltraSoundSensorReading
import steering.steer as steer
from random import random
from time import sleep
from visualization.printer import create_visualizer
from configuration.config_listener import ConfigListener
import configuration.commands as cmds
import atexit
import httplib
import persistant_readings
import json
from can_move_forward import can_move_forward

sensors = Sensors()
vis = create_visualizer()
conf = ConfigListener(8085)
atexit.register(vis.cleanup)


REVOLVE_TIME = 2
def spin():
  # spin atleast .2s
  time_to_spin = random()*REVOLVE_TIME
  steer.back()
  sleep(2)
  steer.right()
  sleep(time_to_spin)
  steer.stop()


def main2():

  steer.setup()
  sensors.start()
  conf.start()

  initialized = False
  just_spun = False

  while True:
    cmd = conf.last_command()

    uss = sensors.get_ultrasound_readings()
    css = sensors.get_camera_readings()
    grs = sensors.get_gps_readings()

    vis.register_reading('Camera', 'camera', css)
    vis.register_reading('Ultrasound', 'ultrasound', uss)
    vis.register_reading('GPS', 'gps', grs)
    vis.render()

    if cmd == None:
      steer.stop()
      continue
    if cmd == cmds.STOP:
      steer.stop()
      just_spun = False
      continue

    if cmd == cmds.FORWARD:
      persistant_readings.store_reading(uss, css, grs, True)
      steer.forward()
      just_spun = False

    elif cmd == cmds.BACKWARD:
      if not just_spun:
        persistant_readings.store_reading(uss, css, grs, False)    
        spin()
        just_spun = True
    
    sleep(0.1)
    

def main():
  steer.setup()
  sensors.start()
  conf.start()
  probed = False
  while(True):
    uss = sensors.get_ultrasound_readings()
    css = sensors.get_camera_readings()
    grs = sensors.get_gps_readings()

    vis.register_reading('Camera', 'camera', css)
    vis.register_reading('Ultrasound', 'ultrasound', uss)
    vis.register_reading('GPS', 'gps', grs)

    if len(grs.raw()) > 0:
      coords = grs.raw()[0]['payload']['coord']
      conf.register_position(coords)

    if conf.is_configuring():
      cmd = conf.last_command()
      if cmd == cmds.LEFT:
        steer.left()
        probed = False
      if cmd == cmds.RIGHT:
        steer.right()
        probed = False
      if cmd == cmds.STOP:
        steer.stop()
        probed = False
      if cmd == cmds.FORWARD:
        steer.forward()
        probed = False
      if cmd == cmds.BACKWARD:
        steer.back()
        probed = False



    else:
      can_forward = can_move_forward(uss, css, grs)
      vis.register_reading('Can move forward', 'can_move_forward', (can_forward, 1.0))
      print grs
      #vis.render()    
      if can_forward:
        steer.forward()
      else:
        spin()
      
    sleep(.001)

if __name__ == "__main__":
  main()
