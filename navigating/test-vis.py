from sensing.sensor_reading import UltraSoundSensorReading
from visualization.printer import create_visualizer
import time
import atexit

if __name__ == "__main__":
  vis = create_visualizer()
  atexit.register(vis.cleanup)
  mock_us = UltraSoundSensorReading([{
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [False, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [False, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [True, True, True]
  }, {
    'timestamp': time.time(),
    'can_move': [False, True, True]
  }])
  vis.register_reading('Ultrasound', 'ultrasound', mock_us)
  vis.register_reading('Can move forward', 'can_move_forward', (True, .9))  

  while(True):
    vis.render()
    time.sleep(.2)