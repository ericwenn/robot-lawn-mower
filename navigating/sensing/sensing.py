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
    csr = CameraSensorReading([])
    return csr
  
  def get_gps_readings(self):
    gsr = GPSSensorReading([])
    return gsr
