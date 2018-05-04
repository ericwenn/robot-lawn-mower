'''
Exposes a consistent interface to all sensors.
This is what should be used from other modules.
'''
from sensor_listener import SensorListener
from sensor_reading import UltraSoundSensorReading, CameraSensorReading, GPSSensorReading
from sound_sensor import SoundSensor
import time 


class Sensors(object):
  def __init__(self):
    self.sensor_listener = SensorListener()
    self.sound_sensor = SoundSensor()
    pass
  
  def start(self):
    self.sensor_listener.start()
    self.sound_sensor.start()

  def get_ultrasound_readings(self):
    events = self.sound_sensor.get_ultrasound_events(10)

    uls = UltraSoundSensorReading(events)
    return uls
  
  def get_camera_readings(self):
    events = self.sensor_listener.get_camera_events(10)
    csr = CameraSensorReading(events)
    return csr
  
  def get_gps_readings(self):
    events = self.sensor_listener.get_gps_events(10)
    gsr = GPSSensorReading(events)
    return gsr
