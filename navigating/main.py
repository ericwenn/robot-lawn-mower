from random import random
from time import sleep
import httplib
import atexit
import json
from sensing.sensing import Sensors
from sensing.sensor_reading import UltraSoundSensorReading
from configuration.config_listener import ConfigListener
import configuration.commands as cmds
import persistant_readings
from can_move_forward import can_move_forward
import steering.steer as steer
from visualization.printer import create_visualizer

sensors = Sensors()
vis = create_visualizer()
conf = ConfigListener(8085)
atexit.register(vis.cleanup)

# time it takes for the robot under normal conditions
# to spin 360 degrees
REVOLVE_TIME = 2

def spin():
  rand = max(random(), .2)
  time_to_spin = rand*REVOLVE_TIME
  steer.back()
  sleep(2)
  steer.right()
  sleep(time_to_spin)
  steer.stop()

def gps_spin():
  time_to_spin = .5*REVOLVE_TIME
  steer.right()
  sleep(time_to_spin)
  
  iterations = 0
  good_gps_readings_in_row = 0
  while good_gps_readings_in_row < 3 and iterations < 6:
    steer.forward()
    sleep(.5)
    gps_verdict = sensors.get_gps_readings().can_move_forward()
    if gps_verdict > .8:
      good_gps_readings_in_row += 1
    else:
      good_gps_readings_in_row = 0
    iterations += 1
  
  # end with a spin for randomness
  time_to_spin = random()*REVOLVE_TIME
  steer.right()
  sleep(time_to_spin)
  steer.stop()

     

# def main2():

#   steer.setup()
#   sensors.start()
#   conf.start()

#   initialized = False
#   just_spun = False

#   while True:
#     cmd = conf.last_command()

#     uss = sensors.get_ultrasound_readings()
#     css = sensors.get_camera_readings()
#     grs = sensors.get_gps_readings()

#     vis.register_reading('Camera', 'camera', css)
#     vis.register_reading('Ultrasound', 'ultrasound', uss)
#     vis.register_reading('GPS', 'gps', grs)
#     vis.render()

#     if cmd == None:
#       steer.stop()
#       continue
#     if cmd == cmds.STOP:
#       steer.stop()
#       just_spun = False
#       continue

#     if cmd == cmds.FORWARD:
#       persistant_readings.store_reading(uss, css, grs, True)
#       steer.forward()
#       just_spun = False

#     elif cmd == cmds.BACKWARD:
#       if not just_spun:
#         persistant_readings.store_reading(uss, css, grs, False)    
#         spin()
#         just_spun = True
    
#     sleep(0.1)
    

def main():
  '''
  Listens to ultrasound readings and takes navigation decisions based on them.
  The robot can be in configuration mode, which means and external device is controlling the navigation.
  Continiously register data thats used to visualize the progress.
  '''
  steer.setup()
  sensors.start()
  conf.start()
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
      if cmd == cmds.RIGHT:
        steer.right()
      if cmd == cmds.STOP:
        steer.stop()
      if cmd == cmds.FORWARD:
        steer.forward()
      if cmd == cmds.BACKWARD:
        steer.back()



    else:
      gps_verdict = grs.can_move_forward()
      can_forward, _ = can_move_forward(uss, css, grs)
      vis.register_reading('Can move forward', 'can_move_forward', (can_forward, 1.0))
      vis.render()

      if gps_verdict < .8:
        gps_spin()
      if can_forward:
        steer.forward()
      else:
        spin()
      
    sleep(.001)

if __name__ == "__main__":
  main()
